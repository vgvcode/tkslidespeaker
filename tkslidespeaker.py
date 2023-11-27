from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
from tkinter.ttk import Progressbar
import os
from playsound import playsound
from tkinter.ttk import Combobox
from tkinter import Checkbutton
from tkinter import IntVar
import updownload as updown
from pathlib import Path
import config as cfg
import readData as rd
import ui as ui
import threading
import time

cfg.home = Path.home()
cfg.appFolder = os.path.join(cfg.home, "." + cfg.appName)  #C:\users\vgvnv\.tkslidespeaker 
cfg.stagingFolder = os.path.join(cfg.appFolder, "staging") #C:\users\vgvnv\tkslidespeaker\staging
cfg.tmpFolder = os.path.join(cfg.appFolder, "tmp") #C:\users\vgvnv\tkslidespeaker\tmp
cfg.outputFolder = os.path.join(cfg.appFolder, "output") #C:\users\vgvnv\tkslidespeaker\output

def playCallback():
    presoName = cfg.txtPresoName.get()
    if rd.validatePresentationName(presoName) == False:
        messagebox.showerror('Error', 'Make sure that\n1. Your file ends in ppt or pptx.\n2. Your file name has only lower-case alphabets, numbers, - or .')
        return False

    presoWithoutExt = presoName.split(".")[0]
    presoRootFolder = os.path.join(cfg.outputFolder, presoWithoutExt)
    if os.path.exists(presoRootFolder) == False:
        messagebox.showerror('Error', 'Presentation not found!')
    else:       
        ui.playIt(presoWithoutExt)

def downloadCallback():
    presoName = cfg.txtPresoName.get()
    if rd.validatePresentationName(presoName) == False:
        messagebox.showerror('Error', 'Make sure that\n1. Your file ends in ppt or pptx.\n2. Your file name has only lower-case alphabets, numbers, - or .')
        cfg.txtPresoName.delete(0, END)        
        return False

    presoWithoutExt = presoName.split(".")[0]
    presoRootFolder = os.path.join(cfg.outputFolder, presoWithoutExt)
    if os.path.exists(presoRootFolder) == True:
        result = messagebox.askquestion('Action', 'Presentation already exists. Overwrite?')
        if result == "no":
            return False

    result = ui.showLoginDialog()
    if result is None:
        return False
    
    username, password = result

    result = updown.downloadPresentation(username, password, presoWithoutExt)
    ui.clearProgressBar()
    if result is False:
        return False

    messagebox.showinfo('Information', 'Downloaded voice enabled presentation!')
    return True

def uploadCallback():
    presoName = cfg.txtPresoName.get()
    if rd.validatePresentationName(presoName) == False:
        messagebox.showerror('Error', 'Make sure that\n1. Your file ends in ppt or pptx.\n2. Your file name has only lower-case alphabets, numbers, - or .')
        return False
    
    uploadPath = os.path.join(cfg.stagingFolder, presoName)
    if not os.path.exists(uploadPath):
        messagebox.showerror('Error', 'Presentation not found in {}'.format(cfg.stagingFolder))
        return False
    
    print("presoName: {}".format(presoName))

    #get the speaker
    result = ui.showSpeakerDialog()
    if result is not None:
        speaker, languageCode = result
    else:
        print("Speaker not selected")
        return False
    
    print("Speaker, languageCode: {}, {}".format(speaker, languageCode))

    result = ui.showLoginDialog()
    if result is None:
        return False

    username, password = result
        
    uploadResult, size, numSlides = updown.uploadPresentation(username, password, presoName, speaker, languageCode)
    ui.clearProgressBar()
    #if upload failed exit
    if uploadResult is False:
        return False

    #prevent user from clicking any play controls till upload is done
    ui.setUploadDownloadPlayControls(nextState = "disabled")
    ui.setPlayControls(nextState = "disabled")

    #min 30, then add 3 seconds delay for every slide
    delay = int(30 + numSlides * 3)
    step = 100/delay
    print("Delay: {}, Interval: {}".format(delay, step))
    cbargs = {"presentation" : presoName, "username" : username, "password" : password}
    threading.Timer(1, ui.showProgress, args = (step, cbargs)).start()
    return True
    
    #cfg.txtPresoName.config(state=DISABLED)
    #rd.readPresentation(presoWithoutExt)
    #i.setUploadDownloadPlayControls("disabled")
    #ui.setupGotoPageCombo()
    #ui.showFirst()

def createFolders():
    #create folders needed. It will not raise error if it already exists
    os.makedirs(cfg.appFolder, exist_ok=True)
    os.makedirs(cfg.stagingFolder, exist_ok=True)
    os.makedirs(cfg.tmpFolder, exist_ok=True)
    os.makedirs(cfg.outputFolder, exist_ok=True)

#################################################################################
createFolders()

cfg.rootWin = Tk()
cfg.rootWin.title(cfg.friendlyAppName) 

topMostFrame = Frame(cfg.rootWin)
topMostFrame.grid(row = 0, column = 0)
# adding a label to the root window
lblPresoName = Label(topMostFrame, text = "Enter the name of the presentation", padx=5)
lblPresoName.pack(side = LEFT, fill=BOTH, expand=True)
 
# adding Entry Field
cfg.txtPresoName = Entry(topMostFrame, width=50)
cfg.txtPresoName.pack(side = LEFT, fill=BOTH, expand=True)

actionFrame = Frame(cfg.rootWin)
actionFrame.grid(row = 1, column = 0)

# Set Button with callback
cfg.uploadButton = Button(actionFrame, text = "1. Upload a Powerpoint presentation.", fg ='white', bg = cfg.innerButtonBgColor, disabledforeground=cfg.disabledForegroundColor, command=lambda:uploadCallback())
cfg.uploadButton.pack(side = LEFT, fill=BOTH, padx=10, pady = 10)

cfg.downloadButton = Button(actionFrame, text = "2. Download an AI voice enabled presentation.", fg ='white', bg = cfg.innerButtonBgColor, disabledforeground=cfg.disabledForegroundColor, command=lambda:downloadCallback())
cfg.downloadButton.pack(side = LEFT, fill=BOTH, padx=10, pady = 10)

cfg.playButton = Button(actionFrame, text = "3. Play it!", fg ='white', bg = cfg.innerButtonBgColor, disabledforeground=cfg.disabledForegroundColor, command=lambda:playCallback())
cfg.playButton.pack(side = LEFT, fill=BOTH, padx = 10, pady = 10)

progressFrame = Frame(cfg.rootWin)
progressFrame.grid(row = 2, column = 0)
cfg.progressBar = Progressbar(progressFrame, orient=HORIZONTAL, length=500)
cfg.progressBar.pack()
#bar_indet = Progressbar(progressFrame, orient=HORIZONTAL, length=500, mode = "indeterminate")
#bar_indet.pack()

canvasFrame = Frame(cfg.rootWin)
#canvasFrame.pack(side = TOP)
canvasFrame.grid(row = 3, column = 0)

cfg.can = Canvas(canvasFrame, width=cfg.canvasWidth, height=cfg.canvasHeight) 
cfg.can.pack(padx = cfg.canvasPadX) 
cfg.can_image_container = cfg.can.create_image(0,0, anchor="nw",image=None)

pageNumFrame = Frame(cfg.rootWin)
pageNumFrame.grid(row = 4, column = 0)
cfg.lblPageNum = Label(pageNumFrame, text = "", font=Font(size=cfg.pageNumFontSize))
cfg.lblPageNum.pack(side = LEFT, fill=BOTH, expand=True)

buttonsFrame = Frame(cfg.rootWin) 
#buttonsFrame.pack( side = BOTTOM ) 
buttonsFrame.grid(row = 5, column = 0)

fontObj = Font(size=cfg.notesFontSize)
cfg.txtNotes = Text(buttonsFrame, height=cfg.notesHeight, width=cfg.notesWidth, wrap='word', padx = cfg.notesPadX, font=fontObj)
cfg.txtNotes.config(state=DISABLED)
cfg.txtNotes.pack( side = TOP)

cfg.firstButton = Button(buttonsFrame, text ='First', fg ='white', bg = cfg.outerButtonBgColor, disabledforeground=cfg.disabledForegroundColor, command=lambda:ui.showFirst()) 
cfg.firstButton.pack( side = LEFT, fill = BOTH, expand = True)
cfg.firstButton["state"]="disabled"
cfg.replayButton = Button(buttonsFrame, text ='Replay', fg ='white', bg = cfg.innerButtonBgColor, disabledforeground=cfg.disabledForegroundColor, command=lambda:ui.showCurrent()) 
cfg.replayButton.pack( side = LEFT, fill = BOTH, expand = True)
cfg.replayButton["state"]="disabled"
cfg.previousButton = Button(buttonsFrame, text = 'Previous', fg ='white', bg = cfg.innerButtonBgColor, disabledforeground=cfg.disabledForegroundColor, command=lambda:ui.showPrevious()) 
cfg.previousButton.pack( side = LEFT, fill = BOTH, expand = True) 
cfg.previousButton["state"]="disabled"
cfg.nextButton = Button(buttonsFrame, text = 'Next', fg ='white', bg = cfg.innerButtonBgColor, disabledforeground=cfg.disabledForegroundColor, command=lambda:ui.showNext()) 
cfg.nextButton.pack(side = LEFT, fill = BOTH, expand = True) 
cfg.nextButton["state"]="disabled"
cfg.lastButton = Button(buttonsFrame, text ='Last', fg ='white', bg = cfg.outerButtonBgColor, disabledforeground=cfg.disabledForegroundColor, command=lambda:ui.showLast()) 
cfg.lastButton.pack( side = LEFT, fill = BOTH, expand = True)
cfg.lastButton["state"]="disabled"
cfg.stopButton = Button(buttonsFrame, text ='Stop', fg ='white', bg = cfg.errorButtonBgColor, disabledforeground=cfg.disabledForegroundColor, command=lambda:ui.clearPlaying()) 
cfg.stopButton.pack( side = LEFT, fill = BOTH, expand = True)
cfg.stopButton["state"]="disabled"

fillerFrame = Frame(cfg.rootWin)
fillerFrame.grid(row = 6, column = 0)
fillerLabel = Label(fillerFrame, text = " ", font=Font(size=cfg.fillerFontSize))
fillerLabel.pack(side = LEFT, fill=BOTH, expand=True)

gotoPageFrame = Frame(cfg.rootWin)
gotoPageFrame.grid(row = 7, column = 0)

#Auto Advance checkbox
cfg.autoAdvance = IntVar()
cfg.autoAdvanceCheckBox = Checkbutton(gotoPageFrame, variable = cfg.autoAdvance, text="Auto advance", onvalue=1, offvalue=0, command=ui.toggleAutoAdvance)
cfg.autoAdvanceCheckBox.pack(side = LEFT, fill=BOTH, expand=True)

# Label creation
goToPageLabel = Label(gotoPageFrame, text = "Go to page:")
goToPageLabel.pack(side = LEFT, fill=BOTH, expand=True)

# Combobox creation 
pg = StringVar() 
cfg.goToPageCombo = Combobox(gotoPageFrame, width = 10, height = 10, textvariable = pg)
cfg.goToPageCombo.pack(side = LEFT, fill=BOTH, expand=True)
cfg.goToPageCombo.config(state = "readonly")
cfg.goToPageCombo.current()
cfg.goToPageCombo.bind("<<ComboboxSelected>>", ui.goToPage)

copyrightFrame = Frame(cfg.rootWin)
copyrightFrame.grid(row = 8, column = 0)
copyrightLab = Label(copyrightFrame, text = cfg.copyrightText, fg=cfg.copyrightFgColor, pady = cfg.copyrightPadY)
copyrightLab.pack( side = TOP, fill = BOTH, expand = True)

cfg.rootWin.protocol("WM_DELETE_WINDOW", ui.onClosing)

cfg.rootWin.update_idletasks()

cfg.rootWin.mainloop() 
