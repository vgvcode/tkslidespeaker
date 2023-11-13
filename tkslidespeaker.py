from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
import os
from PIL import ImageTk, Image
import json
from playsound import playsound
from threading import Timer
from tkinter.ttk import Combobox
from tkinter import Checkbutton
from tkinter import IntVar
import updownload as updown
from pathlib import Path
import config as cfg
import readData as rd
import ui as ui

cfg.home = Path.home()
cfg.appFolder = os.path.join(cfg.home, cfg.appName)  #C:\users\vgvnv\tkslidespeaker 
cfg.stagingFolder = os.path.join(cfg.appFolder, "staging") #C:\users\vgvnv\tkslidespeaker\staging
cfg.tmpFolder = os.path.join(cfg.appFolder, "tmp") #C:\users\vgvnv\tkslidespeaker\tmp
cfg.outputFolder = os.path.join(cfg.appFolder, "output") #C:\users\vgvnv\tkslidespeaker\output

def playCallback():
    presoName = cfg.txtPresoName.get()
    if rd.validatePresentationName(presoName) == False:
        messagebox.showerror('error', 'Only lower case alphabets and numbers allowed!')
        cfg.txtPresoName.delete(0, END)        
        return False

    presoRootFolder = os.path.join(cfg.outputFolder, presoName)
    if os.path.exists(presoRootFolder) == False:
        messagebox.showerror('error', 'Presentation not found!')
    else:       
        cfg.txtPresoName.config(state=DISABLED)
        rd.readPresentation(presoName)
        ui.setupGotoPageCombo()
        #print("PlayCallback: Length of preso {}".format(len(cfg.presentation["pages"])))
        ui.showFirst()

def downloadCallback():
    presoName = cfg.txtPresoName.get()
    if rd.validatePresentationName(presoName) == False:
        messagebox.showerror('error', 'Only lower case alphabets and numbers allowed!')
        cfg.txtPresoName.delete(0, END)        
        return False

    result = ui.show_login_dialog()
    if result is not None:
        username, password = result
        updown.downloadPresentation(username, password, presoName)

def uploadCallback():
    presoName = cfg.txtPresoName.get()
    if rd.validatePresentationName(presoName) == False:
        messagebox.showerror('error', 'Only lower case alphabets and numbers allowed!')
        cfg.txtPresoName.delete(0, END)        
        return False

    print("presoName: {}".format(presoName))

    #get the speaker
    speaker = ui.show_speaker_dialog()
    if speaker is None:
        print("Speaker not selected")
        return False
    
    print("Speaker selected {}".format(speaker))
    result = ui.show_login_dialog()
    if result is None:
        return False

    username, password = result
    uploadResult = updown.uploadPresentation(username, password, presoName, speaker)
    #if upload failed, put a message here
    if uploadResult is False:
        messagebox.showerror('error', 'Upload failed!')
        return False

def createFolders():
    #create folders needed. It will not raise error if it already exists
    os.makedirs(cfg.appFolder, exist_ok=True)
    os.makedirs(cfg.stagingFolder, exist_ok=True)
    os.makedirs(cfg.tmpFolder, exist_ok=True)
    os.makedirs(cfg.outputFolder, exist_ok=True)


createFolders()

cfg.rootWin = Tk() 

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
uploadBtn = Button(actionFrame, text = "Upload", fg ='white', bg = cfg.innerButtonBgColor, command=lambda:uploadCallback())
downloadBtn = Button(actionFrame, text = "Download", fg ='white', bg = cfg.innerButtonBgColor, command=lambda:downloadCallback())
playBtn = Button(actionFrame, text = "Play", fg ='white', bg = cfg.innerButtonBgColor, command=lambda:playCallback())
uploadBtn.pack(side = LEFT, fill=BOTH, padx=10, pady = 10)
downloadBtn.pack(side = LEFT, fill=BOTH, padx=10, pady = 10)
playBtn.pack(side = LEFT, fill=BOTH, padx = 10, pady = 10)

canvasFrame = Frame(cfg.rootWin)
#canvasFrame.pack(side = TOP)
canvasFrame.grid(row = 2, column = 0)

cfg.can = Canvas(canvasFrame, width=cfg.canvasWidth, height=cfg.canvasHeight) 
cfg.can.pack(padx = cfg.canvasPadX) 
cfg.can_image_container = cfg.can.create_image(0,0, anchor="nw",image=None)

pageNumFrame = Frame(cfg.rootWin)
pageNumFrame.grid(row = 3, column = 0)
cfg.lblPageNum = Label(pageNumFrame, text = "", font=Font(size=cfg.pageNumFontSize))
cfg.lblPageNum.pack(side = LEFT, fill=BOTH, expand=True)

buttonsFrame = Frame(cfg.rootWin) 
#buttonsFrame.pack( side = BOTTOM ) 
buttonsFrame.grid(row = 4, column = 0)

fontObj = Font(size=cfg.notesFontSize)
cfg.txtNotes = Text(buttonsFrame, height=cfg.notesHeight, width=cfg.notesWidth, wrap='word', padx = cfg.notesPadX, font=fontObj)
cfg.txtNotes.config(state=DISABLED)
cfg.txtNotes.pack( side = TOP)

firstButton = Button(buttonsFrame, text ='First', fg ='white', bg = cfg.outerButtonBgColor, command=lambda:ui.showFirst()) 
firstButton.pack( side = LEFT, fill = BOTH, expand = True) 
previousButton = Button(buttonsFrame, text = 'Previous', fg ='white', bg = cfg.innerButtonBgColor, command=lambda:ui.showPrevious()) 
previousButton.pack( side = LEFT, fill = BOTH, expand = True) 
nextButton = Button(buttonsFrame, text = 'Next', fg ='white', bg = cfg.innerButtonBgColor, command=lambda:ui.showNext()) 
nextButton.pack(side = LEFT, fill = BOTH, expand = True) 
lastButton = Button(buttonsFrame, text ='Last', fg ='white', bg = cfg.outerButtonBgColor, command=lambda:ui.showLast()) 
lastButton.pack( side = LEFT, fill = BOTH, expand = True)

fillerFrame = Frame(cfg.rootWin)
fillerFrame.grid(row = 5, column = 0)
fillerLabel = Label(fillerFrame, text = " ", font=Font(size=cfg.fillerFontSize))
fillerLabel.pack(side = LEFT, fill=BOTH, expand=True)

gotoPageFrame = Frame(cfg.rootWin)
gotoPageFrame.grid(row = 6, column = 0)

#Auto Advance checkbox
cfg.autoAdvance = IntVar()
autoAdvanceCheckBox = Checkbutton(gotoPageFrame, variable = cfg.autoAdvance, text="Auto advance", onvalue=1, offvalue=0, command=ui.toggleAutoAdvance)
autoAdvanceCheckBox.pack(side = LEFT, fill=BOTH, expand=True)

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
copyrightFrame.grid(row = 7, column = 0)
copyrightLab = Label(copyrightFrame, text = cfg.copyrightText, fg=cfg.copyrightFgColor, pady = cfg.copyrightPadY)
copyrightLab.pack( side = TOP, fill = BOTH, expand = True)

cfg.rootWin.protocol("WM_DELETE_WINDOW", ui.onClosing)

cfg.rootWin.update_idletasks()

cfg.rootWin.mainloop() 
