from tkinter import *
from tkinter.font import Font
import os
from typing import Any
from PIL import ImageTk, Image
import json
from threading import Timer
import config as cfg
import readData as rd
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Progressbar
import time

def readImage(path):
    img = Image.open(path).resize((cfg.canvasWidth, cfg.canvasHeight))
    return ImageTk.PhotoImage(img)
    #return PhotoImage(file=path)

def show():
    #print("Opening {}".format(cfg.presentation["pages"][cfg.pageNum]["pic0.PNG"]))
    lg = len(cfg.presentation["pages"])-1 #example: a 5 page book will have pages 0,1,2,3,4,5. So len = 6. 0th page is not counted

    #if there was an error in conversion or platform was not windows, pic0 will not be there
    if "pic0.PNG" in cfg.presentation["pages"][cfg.pageNum]:
        img = cfg.presentation["pages"][cfg.pageNum]["pic0.PNG"]
        cfg.can.itemconfig(cfg.can_image_container, image=img)
        #print("Rendered image")
    else:
        img = None

    txt = rd.getText(cfg.presentation, cfg.pageNum)
    if txt is None:
        txt = ""
    cfg.lblPageNum.config(text="Page {} of {}".format(cfg.pageNum, lg))
    cfg.txtNotes.config(state=NORMAL)
    cfg.txtNotes.delete("1.0", END)
    cfg.txtNotes.insert(END, txt.replace("\n", " "))
    cfg.txtNotes.config(state=DISABLED)
    #print("Rendered text")
    sound = cfg.presentation["pages"][cfg.pageNum]["speech.mp3"]
    #check if sound file is empty. It can cause problems with playsound
    file_stats = os.stat(sound)
    if file_stats.st_size == 0:
        sound = None
    #set the highlight timerstime
    highlightTimers = setTimersForSentenceHighlighting()
    #start the sound timer
    if sound is not None:
        soundTimer = Timer(0, rd.readSound, [sound])
        soundTimer.start()
    #start the highlight timers
    for timer in highlightTimers:
        timer.start()

def showNext():
    if not cfg.isPlaying:
        #print("ShowNext: PageNum: {}, Presentation Length:{}".format(cfg.pageNum, len(cfg.presentation["pages"])))
        if cfg.pageNum < len(cfg.presentation["pages"])-1:
            cfg.pageNum = cfg.pageNum + 1
            show()

def showPrevious():
    if not cfg.isPlaying:
        #print("ShowPrevious: PageNum: {}, Presentation Length:{}".format(cfg.pageNum, len(cfg.presentation["pages"])))
        if cfg.pageNum > 1:
            cfg.pageNum = cfg.pageNum - 1
            show()
        
def showFirst():
    if not cfg.isPlaying:
        cfg.firstButton["state"]="normal"
        cfg.lastButton["state"]="normal"
        cfg.nextButton["state"]="normal"
        cfg.previousButton["state"]="normal"
        cfg.pageNum = 1
        #print("ShowFirst: PageNum: {}, Presentation Length:{}".format(cfg.pageNum, len(cfg.presentation["pages"])))
        show()

def showLast():
    if not cfg.isPlaying:
        cfg.pageNum = len(cfg.presentation["pages"]) - 1
        #print("ShowLast: PageNum: {}, Presentation Length:{}".format(cfg.pageNum, len(cfg.presentation["pages"])))
        show()

def showCurrent():
    if not cfg.isPlaying:
        show()

def clearPlaying():
    if cfg.isPlaying:
        return False
    
    result = messagebox.askquestion('Stop?', 'Stop playing current presentation?')
    if result == "no":
        return False
    
    setUploadDownloadPlayControls(nextState = "normal")
    setPlayControls(nextState = "disabled")
    clearScreen()
    
def clearScreen():
    cfg.can.delete("all")
    cfg.txtPresoName.delete("0", END)
    cfg.txtNotes.config(state=NORMAL)
    cfg.txtNotes.delete("1.0", END)
    cfg.lblPageNum.config(text="")
    cfg.rootWin.update_idletasks()

def choiceYesNo(pop, option, path, yesCallback, noCallback):
   pop.destroy()
   if option == "yes":
       yesCallback(path)
   else:
       noCallback()

def setTimersForSentenceHighlighting():
    #if no speechmarks are present return an empty array of timers
    if "speechmarks.txt" not in cfg.presentation["pages"][cfg.pageNum]:
        return []

    #loop through speechmarks, set timers to highlight sentences
    speechmarksStr = cfg.presentation["pages"][cfg.pageNum]["speechmarks.txt"]
    delimiter = "}"
    speechmarks = [x + delimiter for x in speechmarksStr.split(delimiter)]
    #remove the last element (delimiter) in the array
    speechmarks.pop()
    timers = []
    ix = 0
    lastix = len(speechmarks)-1
    pSpeechmark = {}
    for speechmarkStr in speechmarks:
        speechmark = json.loads(speechmarkStr)

        if ix > 0:
            pStart = pSpeechmark["start"]-1  #offset starts at 0
            pEnd = pSpeechmark["end"]-1
            pValue = pSpeechmark["value"]
            offset = 500 if speechmark["time"] > 500 else 0
            pStartTime = (speechmark["time"] - offset) / 1000  #convert msec to sec - note this is offset 500 ms before the time of current speechmark
            pValue = pSpeechmark["value"]
            pTag = "sentence-" + str(ix-1) + "-off"
            pt = Timer(pStartTime, unHighlightText, [cfg.txtNotes, pTag, pStart, pEnd, pValue, False])
            timers.append(pt)

        start = speechmark["start"]-1  #offset starts at 0
        end = speechmark["end"]-1
        value = speechmark["value"]
        startTime = speechmark["time"] / 1000  #convert msec to sec
        tag = "sentence-" + str(ix) + "-on"

        #on the last ix, set the flag to True
        if ix == lastix:
            t = Timer(startTime, highlightText, [cfg.txtNotes, tag, start, end, value, True])
        else:
            t = Timer(startTime, highlightText, [cfg.txtNotes, tag, start, end, value, False])

        timers.append(t)
        pSpeechmark = speechmark
        ix = ix + 1
    return timers

def highlightText(textWidget, tag, start, end, value, isLastSentence):
    hStart = "1." + str(start)
    hEnd = "1." + str(end)

    #print("Inside highlightText {} {} {} {}".format(tag, hStart, hEnd, value))
    textWidget.tag_add(tag, hStart, hEnd)
    textWidget.tag_configure(tag, background=cfg.textHightlightColor, foreground="black")

    if isLastSentence:
        #print("At last sentence")
        pass

def unHighlightText(textWidget, tag, start, end, value, isLastSentence):
    hStart = "1." + str(start)
    hEnd = "1." + str(end)

    #print("Inside unHighlightText {} {} {} {}".format(tag, hStart, hEnd, value))
    textWidget.tag_add(tag, hStart, hEnd)
    textWidget.tag_configure(tag, background="white", foreground="black")

def setupGotoPageCombo():
    cfg.goToPageCombo.delete(0, END)
    lov = ()
    for i in range(1, len(cfg.presentation["pages"])):
        elem = (str(i),)
        lov += elem
    cfg.goToPageCombo["values"] = lov

def goToPage(event):
    cfg.pageNum = int(event.widget.get())
    #print("Selected page: {}".format(cfg.pageNum))
    show()

def toggleAutoAdvance():
    #print("Auto advance toggled: {}".format(cfg.autoAdvance.get()))
    pass

def onClosing():
    if cfg.isPlaying:
        messagebox.showwarning("Warning", "Please wait for the current sound to finish playing")
    else:
        cfg.rootWin.destroy()

class LoginDialog(simpledialog.Dialog):
    def body(self, master):
        Label(master, text="Username:").grid(row=0)
        Label(master, text="Password:").grid(row=1)

        self.username_entry = Entry(master)
        self.password_entry = Entry(master, show="*")

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        return self.username_entry  # Focus on the username entry initially

    def apply(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.result = (username, password)

def show_login_dialog():
    dialog = LoginDialog(cfg.rootWin, title="Login")
    return dialog.result

class ComboBoxModalBox(simpledialog.Dialog):
    def body(self, master):
        self.combo_var = StringVar()
        self.combo_box = ttk.Combobox(master, textvariable=self.combo_var, values=cfg.speakerList)
        self.combo_box.grid(row=0, column=0, padx=10, pady=10)

        return self.combo_box  # Focus on the combo box initially

    def apply(self):
        self.result = self.combo_var.get()

def show_speaker_dialog():
    dialog = ComboBoxModalBox(cfg.rootWin, title="Select your speaker")
    return dialog.result

def show_progress_sync(seconds, bar):
    step = 100/seconds
    clearProgressBar(bar)
    for t in range(seconds):
        time.sleep(3)
        updateProgressBar(bar, 3 * step)

def show_progress_async(x, step, delay, bar):
    bar["value"] = 0
    while x.is_alive():
        bar["value"] = bar["value"] + step
        if bar["value"] > 100:
            bar["value"] = 0
        cfg.rootWin.update_idletasks()
        time.sleep(delay)
    bar["value"] = 100

def updateProgressBar(bar, value):
    bar["value"] = (bar["value"] + value) % 100
    cfg.rootWin.update_idletasks()

def clearProgressBar(bar):
    bar["value"] = 0
    cfg.rootWin.update_idletasks()

def setUploadDownloadPlayControls(nextState):
    cfg.txtPresoName["state"] = nextState
    cfg.uploadButton["state"] = nextState
    cfg.downloadButton["state"] = nextState
    cfg.playButton["state"] = nextState

def setPlayControls(nextState):
    cfg.firstButton["state"] = nextState
    cfg.lastButton["state"] = nextState
    cfg.nextButton["state"] = nextState
    cfg.previousButton["state"] = nextState
    cfg.goToPageCombo["state"] = nextState
    cfg.replayButton["state"] = nextState
    cfg.stopButton["state"] = nextState

