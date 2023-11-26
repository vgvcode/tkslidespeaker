import requests
import json
import os
import shutil
import threading
import config as cfg
import ppt2converted as ppt2conv
from tkinter import messagebox
import platform
from datetime import datetime
import ui as ui

def downloadPresoFile(url, filename):
    r = requests.get(url, allow_redirects=True)
    f = open(filename, 'wb')
    f.write(r.content)
    f.close()
    return True
    #print("Downloaded: {}".format(filename))

def createPresoFolder(folder, forceDelete = False):
    if forceDelete:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        else:
            os.makedirs(folder)
    else:
        if not os.path.exists(folder):
            os.makedirs(folder)
    #print("Created folder: {}".format(folder))

def getClientId(username, password):
    #sign In, get_user and get client_id from user attributes
    apiurl = "https://aecwdu6fhe.execute-api.ap-south-1.amazonaws.com/dev/get-clientid"

    payload = json.dumps({
        "username": username,
        "password": password
    })
    headers = {
        'authorizationHeader': cfg.apiKey,
        'Content-Type': 'application/json'
    }

    #print("apiurl:{}".format(apiurl))
    response = requests.request("POST", apiurl, headers=headers, data=payload)
    r = response.text
    #print("r:{}".format(r))
    rj = json.loads(r)
    #print("rj:{}".format(rj))
    if "body" not in rj:
        messagebox.showerror("error", "Login failed!")
        return None

    body = rj["body"]
    if body is not None:
        return body
    else:
        messagebox.showerror("error", "Invalid client id!")
        return None

def getUsage(idToken, clientId, email):
    #get the usage for this month
    #this is modeled as a GET method, so supply query params
    apiurl = "https://mw238rzarl.execute-api.ap-south-1.amazonaws.com/dev/slidespeaker/tenant-usage"
    params = "client_id="+clientId+"&email="+email    
    apiurlWithParams = apiurl + "?" + params
    print("apiurlWithParams:{}".format(apiurlWithParams))
    headers = {
        'Authorization': idToken
    }

    response = requests.request("GET", apiurlWithParams,headers=headers)
    r = response.text
    #print("r:{}".format(r))
    rj = json.loads(r)
    #print("rj:{}".format(rj))
    
    if "errorMessage" in rj:
        print("Error: {}".format(rj))
        messagebox.showerror("Error", rj["errorMessage"])
        return None 
    
    body = rj["body"]
    if body is not None:
        return body
    else:
        print("No usage for {}".format(email))
        messagebox.showerror("Error", "No usage for {}".format(email))
        return None

def updateUsage(idToken, clientId, email, operation, delta):
    #get the usage for this month
    apiurl = "https://mw238rzarl.execute-api.ap-south-1.amazonaws.com/dev/slidespeaker/tenant-usage"

    payload = json.dumps({
        "client_id": clientId,
        "email": email,
        "operation": operation, 
        "delta": delta
    })
    headers = {
        'Authorization': idToken
    }

    response = requests.request("POST", apiurl, headers=headers, data=payload)
    r = response.text
    #print("r:{}".format(r))
    rj = json.loads(r)
    #print("rj:{}".format(rj))
    body = rj["body"]
    if body is not None:
        return body
    else:
        messagebox.showerror("Error", "Usage update failed for {}".format(email))
        return None

def downloadPresentation(username, password, presoWithoutExt):
    print("Signing in...")
    result = getClientId(username, password)
    if result is None:
        return False
    clientId, accessToken, idToken = result
    print("Client Id: {}".format(clientId))
    
    ui.updateProgressBar(5)

    # print("Signed in, getting usage")
    # today = date.today()
    # mmyyyy = today.strftime("%m%Y")

    #username is the email
    email = username  
    usage = getUsage(idToken, clientId, email)
    print("Usage: {}".format(usage))
    if usage is None:
        return False

    ui.updateProgressBar(5)

    print("Checking subscription end date")
    end_date_str = usage["subscription_end_date"]
    end_date =  datetime.strptime(end_date_str, '%d%m%Y')
    today = datetime.now()
    if end_date < today:
        messagebox.showerror("Error", "Your subscription has expired! Your subscription end date: {}".format(end_date_str))
        return False

    print("Checking download value")
    downloads_remaining = usage["downloads_remaining"]
    if downloads_remaining <= 0:
        messagebox.showerror("Error", "You have exceeded your download limit! Downloads left: {}".format(downloads_remaining))
        return False

    print("Your downloads:{}".format(downloads_remaining))

    prefix = clientId + "/" + presoWithoutExt
    print("Prefix: {}".format(prefix))

    payload = json.dumps({
        "prefix": prefix
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': idToken
    }
    apiurl = "https://mw238rzarl.execute-api.ap-south-1.amazonaws.com/dev/slidespeaker/get-download-urls"

    print("Fetching URLs...")
    response = requests.request("GET", apiurl, headers=headers, data=payload)
    print("Completed.")

    ui.updateProgressBar(5)

    #if download url failed exit here

    r = response.text
    rj = json.loads(r)
    body = rj["body"]

    if len(body) == 0:
        messagebox.showerror("Error", "No data present for: {}".format(presoWithoutExt))
        return False

    print("Downloading files...")
    threads = []
    ix = 0

    for elem in body:
        path = elem["object"]  #456/ai-teacher-converted/916d5ecb-0a0d-49e2-b2c1-75f78a70df88/speechmarks.txt
        psurl = elem["presigned_url"]
        if ix == 0:
            presoName = path.split("/")[1] #ai-teacher-converted
            presoNamePath = os.path.join(cfg.outputFolder, presoName) #~/tkslidespeaker/output/ai-teacher-converted
            createPresoFolder(presoNamePath, forceDelete=True)
            ix = ix + 1

        pathElements = os.path.split(path)
        pathPrefix = pathElements[0] #456/ai-teacher-converted/916d5ecb-0a0d-49e2-b2c1-75f78a70df88
        pathPrefixElements = os.path.split(pathPrefix)
        #this happens for manifest.json and speaker.json
        if pathPrefixElements[1] == presoName:
            slideFolder = presoNamePath
        else:
            slideFolder = os.path.join(presoNamePath, pathPrefixElements[1]) #~/tkslidespeaker/output/ai-teacher-converted/916d5ecb-0a0d-49e2-b2c1-75f78a70df88
        createPresoFolder(slideFolder)
        file = os.path.join(slideFolder, pathElements[1]) #~/tkslidespeaker/output/ai-teacher-converted/916d5ecb-0a0d-49e2-b2c1-75f78a70df88/speechmarks.txt
        #print("Preso: {} Folder: {}, file: {}".format(presoNamePath, slideFolder, file))
        x = threading.Thread(target=downloadPresoFile, args=(psurl, file))
        x.start()
        threads.append(x)
        ui.updateProgressBar(0.05)

    ui.updateProgressBar(5)

    print("Waiting for all threads to finish")
    for t in threads:
        t.join()
    print("All threads finished")

    ui.updateProgressBar(5)

    print("Updating usage")
    result = updateUsage(idToken, clientId, email, "download", 1)
    if result is None:
        return False
    
    print("Updated usage")
    return True

def uploadPresentation(username, password, preso, speaker, languageCode = ""):
    #return (upload result, size of file) -- eg (True, 12345), (False, 0)
    print("Signing in...")
    result = getClientId(username, password)
    if result is None:
        return (False, 0, 0)
    
    clientId, accessToken, idToken = result
    print("Client Id: {}".format(clientId)) 

    ui.updateProgressBar(10)
    # today = date.today()
    # mmyyyy = today.strftime("%m%Y") 
    #username is the email
    email = username  
    usage = getUsage(idToken, clientId, email)
    if usage is None:
        return (False, 0, 0)

    ui.updateProgressBar(10)

    print("Checking subscription end date")
    end_date_str = usage["subscription_end_date"]
    end_date =  datetime.strptime(end_date_str, '%d%m%Y')
    today = datetime.now()
    if end_date < today:
        messagebox.showerror("Error", "Your subscription has expired! Your subscription end date: {}".format(end_date_str))
        return (False, 0, 0)

    print("Checking upload value")
    uploads_remaining = usage["uploads_remaining"]
    if uploads_remaining <= 0:
        messagebox.showerror("Error", "You have exceeded your upload limit! Uploads left: {}".format(uploads_remaining))
        return (False, 0, 0)

    print("Your uploads:{}".format(uploads_remaining))

    print("Converting presentation")
    presoFilePath, numSlides = ppt2conv.convert(preso)
    #if conversion failed, exit here
    if numSlides > cfg.maxSlides:
        messagebox.showerror('Error', 'Your presentation has {} slides. Please reduce the number of slides to 300 or less.'.format(numSlides))
        return (False, 0, 0)

    print("Converted presentation: {}".format(presoFilePath))
    ui.updateProgressBar(30)

    #Create a local speaker.json file
    presentationElements = preso.split(".")
    presoWithoutExt = presentationElements[0]
    #use the presoWithoutExt as a prefix with a - to distinguish from multiple speaker.json files
    longSpeakerFileName = presoWithoutExt + "-" + "speaker.json"
    speakerFilePath = os.path.join(cfg.stagingFolder, longSpeakerFileName)
    f = open(speakerFilePath, "w")
    data = {"speaker": speaker, "languageCode": languageCode}
    f.write(json.dumps(data))
    f.close()

    #upload speaker.json to s3
    #use presoWithoutExt as a folder prefix in S3
    speakerFileName = "speaker.json"
    key = clientId + "/" + presoWithoutExt + "/" + speakerFileName
    result, size = uploadFileToPresignedUrl(idToken, key, localFilePath=speakerFilePath)
    if result is False:
        messagebox.showerror("Error", "Upload of speaker data to S3 failed")
        return (False, 0, 0)
    ui.updateProgressBar(10)

    #Upload presentation to s3
    key = clientId + "/" + preso
    result, size = uploadFileToPresignedUrl(idToken, key, localFilePath=presoFilePath)
    if result is False:
        return (False, 0, 0)
    ui.updateProgressBar(10)

    print("Result: {}, size: {}, numSlides:{}".format(result, size, numSlides))

    #username is the email
    email = username
    result = updateUsage(idToken, clientId, email, "upload", 1)
    if result is None:
        return (False, 0, 0)
    ui.updateProgressBar(10)
    
    print("Updated usage")
    return (True, size, numSlides)

def uploadFileToPresignedUrl(idToken, key, localFilePath):
    #return (upload result, size of file) -- eg (True, 12345), (False, 0)
    print("Obtaining upload url")
    url = "https://mw238rzarl.execute-api.ap-south-1.amazonaws.com/dev/slidespeaker/get-upload-url"
    payload = json.dumps({"key": key})
    headers = {
        'Content-Type': 'application/json',
        'Authorization': idToken
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    #if url was not obtained, exit here

    r = response.text
    #print("Response: {}".format(r))

    rj = json.loads(r)
    psurl = rj["response"]["url"]
    fields = rj["response"]["fields"]

    if localFilePath is not None:
        #Upload file to S3 using presigned URL
        print("Uploading file to S3")
        files = {'file': open(localFilePath, 'rb')}
        r = requests.post(psurl, data=fields, files=files)
        if (r.status_code != 204):
            return (False, 0)
        else:
            print("Uploaded file: {}".format(key))
            size = os.path.getsize(localFilePath)
            return (True, size)
    else:
        messagebox.showerror("Error", "Upload of {} to S3 failed".format(localFilePath))
        return (False, 0)