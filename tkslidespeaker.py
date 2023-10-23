from tkinter import *
from tkinter.font import Font
import os
from PIL import ImageTk, Image
import json
from playsound import playsound
from threading import Timer
import config as cfg
import readData as rd
import ui as ui
from tkinter.ttk import Combobox

cfg.baseFolder = os.path.join('C:\\', 'Users', 'vgvnv', 'Documents', "tkinter-apps", cfg.baseFolderTail)

def playCallback():
    presoName = cfg.txtPresoName.get()
    cfg.root_folder = os.path.join(cfg.baseFolder, presoName)
    if os.path.exists(cfg.root_folder) == False:
        #ui.modal(cfg.rootWin, path, "Would you like to download this presentation?", yes, no)
        ui.modalWithOk(cfg.rootWin, "Presentation not found!", ui.okCallback)
    else:       
        cfg.txtPresoName.config(state=DISABLED)
        rd.readPresentation(presoName)
        ui.setupGotoPageCombo()
        #print("PlayCallback: Length of preso {}".format(len(cfg.presentation["pages"])))
        ui.showFirst()

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
actionBtn = Button(actionFrame, text = "Play", fg ='white', bg = cfg.innerButtonBgColor, command=lambda:playCallback())
actionBtn.pack(side = TOP, pady = 10)

canvasFrame = Frame(cfg.rootWin)
#canvasFrame.pack(side = TOP)
canvasFrame.grid(row = 2, column = 0)

cfg.can = Canvas(canvasFrame, width=cfg.canvasWidth, height=cfg.canvasHeight) 
cfg.can.pack(padx = cfg.canvasPadX) 

cfg.can_image_container = cfg.can.create_image(0,0, anchor="nw",image=None)
#print("Rendered 1st image")

buttonsFrame = Frame(cfg.rootWin) 
#buttonsFrame.pack( side = BOTTOM ) 
buttonsFrame.grid(row = 3, column = 0)

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
fillerFrame.grid(row = 4, column = 0)
fillerLabel = Label(fillerFrame, text = " ", font=Font(size=cfg.fillerFontSize))
fillerLabel.pack(side = LEFT, fill=BOTH, expand=True)

gotoPageFrame = Frame(cfg.rootWin)
gotoPageFrame.grid(row = 5, column = 0)
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
copyrightFrame.grid(row = 6, column = 0)
copyrightLab = Label(copyrightFrame, text = cfg.copyrightText, fg=cfg.copyrightFgColor, pady = cfg.copyrightPadY)
copyrightLab.pack( side = TOP, fill = BOTH, expand = True)

cfg.rootWin.mainloop() 