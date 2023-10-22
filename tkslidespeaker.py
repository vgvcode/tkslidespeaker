from tkinter import *
import os
from PIL import ImageTk, Image
import json
import datetime
from playsound import playsound
from threading import Timer

canvasWidth = 650
canvasHeight = 400
baseFolder = os.path.join('C:\\', 'Users', 'vgvnv', 'Documents', 'tkinter-apps')

def readFile(path):
    f = open(path, "r")
    txt = f.read()
    f.close()
    return txt

def readImage(path):
    return PhotoImage(file=path)

def readSound(path):
    playsound(path)

def getText(pageNum, presentation):
    if "presentation.txt" in presentation["pages"][pageNum]:
        return presentation["pages"][pageNum]["presentation.txt"]
    elif "presentation.notes" in presentation["pages"][pageNum]:
        return presentation["pages"][pageNum]["presentation.notes"]

def readWrapper(path):
    if path.endswith(".txt") or path.endswith(".notes") or path.endswith("json"):
        return readFile(path)
    elif path.endswith("PNG"):
        return readImage(path)
    elif path.endswith("mp3"):
        return path
    else:
        return readFile(path)

def findIndexInManifest(manifest, d):
    for i in range(1,len(manifest)+1):
        if manifest[str(i)] == d:
            return i
    return -1

def readPresentation(baseFolder, txtWidget):
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

    global presentation, pageNum
    path = txtWidget.get()
    txtWidget.config(state=DISABLED)

    lev=0
    presentation = {"title" : path}
    root_folder = os.path.join(baseFolder, path)
    #read the manifest file
    manifest_path = os.path.join(root_folder, "manifest.json")
    manifest = json.loads(readFile(manifest_path))
    #print("Manifest:{}".format(manifest))
    presentation["manifest.json"] = manifest

    #assign the number of pages as per the manifest; one more than length; 0 is unused
    presentation["pages"] = []
    for i in range(len(manifest)+1):
        presentation["pages"].append({})

    #read the speaker file
    speaker_path = os.path.join(root_folder, "speaker.json")
    speaker = json.loads(readFile(speaker_path))
    presentation["speaker.json"] = speaker

    for root, dirs, files in os.walk(root_folder):
        #print("Level:{}, root:{}".format(lev, root))
        if lev == 0:
            parent = root
            presentation["parent"] = root
            for d in dirs:
                #print("Level:{}, d:{}".format(lev, d))
                #find the index of d from manifest
                pg = findIndexInManifest(manifest, d)
                if (pg > -1):
                    presentation["pages"][pg] = {"pageRef" : d}
                else:
                    print("Page not found for:{}".format(d))
                    return None 
            #print("Presentation at level 0:{}".format(presentation))
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
                presentation["pages"][pg][f] = readWrapper(os.path.join(root_folder, root, f))
    #print("{} Presentation read".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    showFirst()
    return presentation

def show():
    global pageNum, presentation, can
    #print("Opening {}".format(presentation["pages"][pageNum]["pic0.PNG"]))
    img2 = presentation["pages"][pageNum]["pic0.PNG"]
    can.itemconfig(can_image_container, image=img2)
    #print("Rendered image") 
    text2 = getText(pageNum, presentation)
    lab.config(text = text2)
    #print("Rendered text")
    sound = presentation["pages"][pageNum]["speech.mp3"]
    t = Timer(1, readSound, [sound])
    t.start()

def showNext():
    global pageNum, presentation
    print("ShowNext: PageNum: {}, Presentation Length:{}".format(pageNum, len(presentation["pages"])))
    if pageNum < len(presentation["pages"])-1:
        pageNum = pageNum + 1
        show()

def showPrevious():
    global pageNum, presentation
    print("ShowPrevious: PageNum: {}, Presentation Length:{}".format(pageNum, len(presentation["pages"])))
    if pageNum > 1:
        pageNum = pageNum - 1
        show()
        
def showFirst():
    global pageNum, presentation, can
    pageNum = 1
    #print("ShowFirst: PageNum: {}, Presentation Length:{}".format(pageNum, len(presentation["pages"])))
    show()

def showLast():
    global pageNum, presentation, can
    pageNum = len(presentation["pages"]) - 1
    print("ShowLast: PageNum: {}, Presentation Length:{}".format(pageNum, len(presentation["pages"])))
    show()

root = Tk() 

presentation = {"pages" : []}
pageNum = 1

topMostFrame = Frame(root)
topMostFrame.grid(row = 0, column = 0)
# adding a label to the root window
lbl = Label(topMostFrame, text = "Enter the name of the presentation", padx=5)
lbl.pack(side = LEFT, fill=BOTH, expand=True)
 
# adding Entry Field
txtWidget = Entry(topMostFrame, width=50)
txtWidget.pack(side = LEFT, fill=BOTH, expand=True)

actionFrame = Frame(root)
actionFrame.grid(row = 1, column = 0)

# Set Button with callback
btn = Button(actionFrame, text = "Play", fg ='white', bg = "green", command=lambda:readPresentation(baseFolder=baseFolder, txtWidget=txtWidget))
btn.pack(side = TOP, pady = 10)

canvasFrame = Frame(root)
#canvasFrame.pack(side = TOP)
canvasFrame.grid(row = 2, column = 0)

can = Canvas(canvasFrame, width=canvasWidth, height=canvasHeight) 
can.pack(padx = 25) 

can_image_container = can.create_image(0,0, anchor="nw",image=None)
#print("Rendered 1st image")

buttonsFrame = Frame(root) 
#buttonsFrame.pack( side = BOTTOM ) 
buttonsFrame.grid(row = 3, column = 0)
lab = Label(buttonsFrame, text = None, height=15, width=80, wraplength=300, anchor = "nw", justify=LEFT, padx = 0)
lab.pack( side = TOP)
bluebutton = Button(buttonsFrame, text ='First', fg ='white', bg = "green", command=lambda:showFirst()) 
bluebutton.pack( side = LEFT, fill = BOTH, expand = True) 
redbutton = Button(buttonsFrame, text = 'Previous', fg ='white', bg = "green", command=lambda:showPrevious()) 
redbutton.pack( side = LEFT, fill = BOTH, expand = True) 
greenbutton = Button(buttonsFrame, text = 'Next', fg ='white', bg = "green", command=lambda:showNext()) 
greenbutton.pack(side = LEFT, fill = BOTH, expand = True) 
blackbutton = Button(buttonsFrame, text ='Last', fg ='white', bg = "green", command=lambda:showLast()) 
blackbutton.pack( side = LEFT, fill = BOTH, expand = True)

copyrightFrame = Frame(root)
copyrightFrame.grid(row = 4, column = 0)
copyrightLab = Label(copyrightFrame, text = "(C) ConnectedWorld Technology Solutions    |    http://connectedworldtech.com", fg="blue", pady = 5)
copyrightLab.pack( side = TOP, fill = BOTH, expand = True)

root.mainloop() 