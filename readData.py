import os
import json
from playsound import playsound
import config as cfg
import ui as ui
from threading import Timer
import re

def readFile(path):
    #rb is used to read text in non english.  It is decoded at the end. This works with English text also
    f = open(path, "rb")
    txt = f.read()
    f.close()
    return txt.decode()

def readSound(path):
    #prevent goto page selection
    cfg.goToPageCombo.config(state = "disabled")
    cfg.isPlaying = True
    try:
        playsound(path)
        cfg.isPlaying = False
        #print("Finished playing sound")
        cfg.goToPageCombo.config(state = "readonly")
        if cfg.autoAdvance.get() == 1:
            #print("Auto advance is on")
            timerShowNext = Timer(cfg.autoAdvanceDelay, ui.showNext)
            timerShowNext.start()
    except playsound.PlaysoundException as e:
        print("Error playing sound: {}".format(e))

def getText(preso, pg):
    if "presentation.txt" in preso["pages"][pg]:
        return preso["pages"][pg]["presentation.txt"]
    elif "presentation.notes" in preso["pages"][pg]:
        return preso["pages"][pg]["presentation.notes"]
    else:
        return ""

def readWrapper(path):
    if path.endswith(".txt") or path.endswith(".notes") or path.endswith("json"):
        return readFile(path)
    elif path.endswith("PNG"):
        return ui.readImage(path)
    elif path.endswith("mp3"):
        return path
    else:
        return readFile(path)

def findIndexInManifest(manifest, d):
    for i in range(1,len(manifest)+1):
        if manifest[str(i)] == d:
            return i
    return -1

def readPresentation(presoWithoutExt):
    # # {
    # #     "title" : "shapes-and-pictures",
    # #     "manifest.json" : "",
    # #     "speaker.json" : "",
    # #     "pages" :
    # #     [
    # #         {
    # #           "pageRef"" "xxxx",
    # #           "links.txt" : "",
    # #           "presentation.notes" : "",
    # #           "speechmarks.txt" : "",
    # #           "speech.mp3" : "",
    # #           "pic0.PNG" : "",
    # #           "pic1.PNG" : ""
    # #         },
    # #         {}, 
    # #         {}
    # #     ]
    # # }

    #at this point the folder exists locally
    presoRootFolder = os.path.join(cfg.outputFolder, presoWithoutExt)
    preso = {"title" : presoWithoutExt}

    #read the manifest file
    manifest_path = os.path.join(presoRootFolder, "manifest.json")
    manifest = json.loads(readFile(manifest_path))
    #print("Manifest:{}".format(manifest))
    preso["manifest.json"] = manifest

    #assign the number of pages as per the manifest; one more than length; 0 is unused
    preso["pages"] = []
    for i in range(len(manifest)+1):
        preso["pages"].append({})

    #read the speaker file
    speaker_path = os.path.join(presoRootFolder, "speaker.json")
    #if speaker file is not available, ok to proceed as a default voice was used for synthesis
    if os.path.exists(speaker_path):
        speaker = json.loads(readFile(speaker_path))
        preso["speaker.json"] = speaker
    else:
        #set a default speaker
        preso["speaker.json"] = {"speaker" : "Stephen"}

    lev=0
    for root, dirs, files in os.walk(presoRootFolder):
        #print("Level:{}, root:{}".format(lev, root))
        if lev == 0:
            parent = root
            preso["parent"] = root
            for d in dirs:
                #print("Level:{}, d:{}".format(lev, d))
                #find the index of d from manifest
                pg = findIndexInManifest(manifest, d)
                if (pg > -1):
                    preso["pages"][pg] = {"pageRef" : d}
                else:
                    print("Page not found for:{}".format(d))
                    return None 
            #print("Presentation at level 0:{}".format(preso))
            lev = lev + 1
        elif lev == 1:
            for f in files:
                #print("Level:{}, root:{}, f:{}".format(lev, root, f))
                #extract last part of root
                paths = os.path.split(root)
                dir = paths[1]
                pg = findIndexInManifest(manifest, dir)
                if (pg == -1):
                    print("Page not found for:{}".format(dir))
                    return None 
                preso["pages"][pg][f] = readWrapper(os.path.join(presoRootFolder, root, f))
    #print("{} preso read".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    cfg.presentation = preso

def validatePresentationName(presoName):
    #if name contains any non alphanumeric character other than period, - return false
    match = re.search(r'[^a-zA-Z0-9\.\-]', presoName)
    if match:
        return False
    
    #if name contains any uppercase character return false
    res = any(c.isupper() for c in presoName)
    if res == True:
        return False

    #if name does not end with .ppt or .pptx return false    
    res = presoName.endswith(".ppt") or presoName.endswith(".pptx")
    if res == False:
        return False
    
    return True

# def checkPresentation(path):
#     cfg.root_folder = os.path.join(cfg.baseFolder, path)

#     if os.path.exists(cfg.root_folder) == False:
#         #ui.modal(cfg.rootWin, path, "Would you like to download this presentation?", yes, no)
#         ui.modalWithOk(cfg.rootWin, "Presentation not found!", ui.okCallback)
#     else:       
#         readPresentation(path)


