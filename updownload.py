import requests
import json
import os
import shutil
import threading
import config as cfg
import ppt2converted as ppt2conv

def downloadPresoFile(url, filename):
    r = requests.get(url, allow_redirects=True)
    f = open(filename, 'wb').write(r.content)
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
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", apiurl, headers=headers, data=payload)
    r = response.text
    #print("r:{}".format(r))
    rj = json.loads(r)
    #print("rj:{}".format(rj))
    body = rj["body"]
    if body is not None:
        return body
    #else:
    #   return None
    return "234"

def downloadPresentation(username, password, preso):
    print("Signing in...")
    clientId = getClientId(username, password)
    if clientId is None:
        return False

    prefix = clientId + "/" + preso

    payload = json.dumps({
        "prefix": prefix
    })
    headers = {
        'Content-Type': 'application/json'
    }
    apiurl = "https://mw238rzarl.execute-api.ap-south-1.amazonaws.com/dev/slidespeaker/get-download-urls"

    print("Fetching URLs...")
    response = requests.request("GET", apiurl, headers=headers, data=payload)
    print("Completed.")

    #if download url failed exit here

    r = response.text
    rj = json.loads(r)
    body = rj["body"]

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

    print("Waiting for all threads to finish")
    for t in threads:
        t.join()
    print("All threads finished")
    return True

def uploadPresentation(username, password, preso, speaker):
    print("Signing in...")
    clientId = getClientId(username, password)
    #if sign in failed, exit here

    print("Converting presentation")
    presoFilePath = ppt2conv.convert(preso)
    #if conversion failed, exit here
    print("Converted presentation: {}".format(presoFilePath))

    key = clientId + "/" + preso
    result = uploadFileOrDataToPresignedUrl(key, localFilePath=presoFilePath, contents = None)
    if result is False:
        print("Upload failed")
        return False

    #Upload speaker.json
    presentationElements = preso.split(".")
    presoWithoutExt = presentationElements[0]
    speakerFileName = presoWithoutExt + "-" + "speaker.json"
    speakerFilePath = os.path.join(cfg.stagingFolder, speakerFileName)
    f = open(speakerFilePath, "a")
    data = {"speaker": speaker}
    f.write(json.dumps(data))
    f.close()

    key = clientId + "/" + presoWithoutExt + "/" + speakerFileName
    result = uploadFileOrDataToPresignedUrl(key, localFilePath=speakerFilePath, contents = None)
    return result    

def uploadFileOrDataToPresignedUrl(key, localFilePath, contents):
    print("Obtaining upload url")
    url = "https://mw238rzarl.execute-api.ap-south-1.amazonaws.com/dev/slidespeaker/get-upload-url"
    payload = json.dumps({"key": key})
    headers = {'Content-Type': 'application/json'}
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
            return False
        else:
            print("Uploaded file: {}".format(key))
            return True
    elif contents is not None:
        #headers = {'Authorization' : ‘(some auth code)’, 'Accept' : 'application/json', 'Content-Type' : 'application/json'}
        headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}

        #Upload file to S3 using presigned URL
        print("Uploading file to S3")
        r = requests.post(psurl, data=contents, headers=headers)
        if (r.status_code != 204):
            return False
        else:
            print("Uploaded file: {}".format(key))
            return True
    else:
        return False