import os
import json
from playsound import playsound
import config as cfg
import ui as ui
from threading import Timer

def readFile(path):
    f = open(path, "r")
    txt = f.read()
    f.close()
    return txt

def readSound(path):
    #prevent goto page selection
    cfg.goToPageCombo.config(state = "disabled")
    cfg.isPlaying = True
    playsound(path)
    cfg.isPlaying = False
    #print("Finished playing sound")
    cfg.goToPageCombo.config(state = "readonly")
    if cfg.autoAdvance.get() == 1:
        #print("Auto advance is on")
        timerShowNext = Timer(cfg.autoAdvanceDelay, ui.showNext)
        timerShowNext.start()

def getText(preso, pg):
    if "presentation.txt" in preso["pages"][pg]:
        return preso["pages"][pg]["presentation.txt"]
    elif "presentation.notes" in preso["pages"][pg]:
        return preso["pages"][pg]["presentation.notes"]

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

def checkPresentation(path):
    cfg.root_folder = os.path.join(cfg.baseFolder, path)

    if os.path.exists(cfg.root_folder) == False:
        #ui.modal(cfg.rootWin, path, "Would you like to download this presentation?", yes, no)
        ui.modalWithOk(cfg.rootWin, "Presentation not found!", ui.okCallback)
    else:       
        readPresentation(path)

def readPresentation(path):
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
    preso = {"title" : path}

    #read the manifest file
    manifest_path = os.path.join(cfg.root_folder, "manifest.json")
    manifest = json.loads(readFile(manifest_path))
    #print("Manifest:{}".format(manifest))
    preso["manifest.json"] = manifest

    #assign the number of pages as per the manifest; one more than length; 0 is unused
    preso["pages"] = []
    for i in range(len(manifest)+1):
        preso["pages"].append({})

    #read the speaker file
    speaker_path = os.path.join(cfg.root_folder, "speaker.json")
    speaker = json.loads(readFile(speaker_path))
    preso["speaker.json"] = speaker

    lev=0
    for root, dirs, files in os.walk(cfg.root_folder):
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
                preso["pages"][pg][f] = readWrapper(os.path.join(cfg.root_folder, root, f))
    #print("{} preso read".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    cfg.presentation = preso

def validatePresentationName(presoName):
    #if name contains any non alphanumeric character return false
    if not presoName.isalnum():
        return False
    
    #if name contains any uppercase character return false
    res = any(c.isupper() for c in presoName)
    if res == True:
        return False

