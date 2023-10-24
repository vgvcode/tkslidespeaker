from tkinter import *
from tkinter.font import Font
import os
from PIL import ImageTk, Image
import json
from threading import Timer
import config as cfg
import readData as rd

def readImage(path):
    return PhotoImage(file=path)

def show():
    #print("Opening {}".format(cfg.presentation["pages"][cfg.pageNum]["pic0.PNG"]))
    lg = len(cfg.presentation["pages"])-1 #example: a 5 page book will have pages 0,1,2,3,4,5. So len = 6. 0th page is not counted
    img2 = cfg.presentation["pages"][cfg.pageNum]["pic0.PNG"]
    cfg.can.itemconfig(cfg.can_image_container, image=img2)
    #print("Rendered image") 
    text2 = rd.getText(cfg.presentation, cfg.pageNum)
    cfg.lblPageNum.config(text="Page {} of {}".format(cfg.pageNum, lg))
    cfg.txtNotes.config(state=NORMAL)
    cfg.txtNotes.delete("1.0", END)
    cfg.txtNotes.insert(END, text2.replace("\n", " "))
    cfg.txtNotes.config(state=DISABLED)
    #print("Rendered text")
    sound = cfg.presentation["pages"][cfg.pageNum]["speech.mp3"]
    #set the highlight timers
    highlightTimers = setTimersForSentenceHighlighting()
    #start the sound timer
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
        cfg.pageNum = 1
        #print("ShowFirst: PageNum: {}, Presentation Length:{}".format(cfg.pageNum, len(cfg.presentation["pages"])))
        show()

def showLast():
    if not cfg.isPlaying:
        cfg.pageNum = len(cfg.presentation["pages"]) - 1
        #print("ShowLast: PageNum: {}, Presentation Length:{}".format(cfg.pageNum, len(cfg.presentation["pages"])))
        show()

def choiceYesNo(pop, option, path, yesCallback, noCallback):
   pop.destroy()
   if option == "yes":
       yesCallback(path)
   else:
       noCallback()

def modalWithYesNo(win, path, message, yesCallback, noCallback):
   pop = Toplevel(win)
   pop.title("Confirmation")
   pop.geometry("300x150")
   pop.config(bg="white")
   # Create a Label Text
   label = Label(pop, text=message, font=('Aerial', 12))
   label.pack(pady=20)
   # Add a Frame
   frame = Frame(pop, bg="white")
   frame.pack(pady=10)
   # Add Button for making selection
   button1 = Button(frame, text="Yes", command=lambda: choiceYesNo(pop, "yes", path, yesCallback, noCallback), bg="blue", fg="white")
   button1.grid(row=0, column=1)
   button2 = Button(frame, text="No", command=lambda: choiceYesNo(pop, "no", path, yesCallback, noCallback), bg="blue", fg="white")
   button2.grid(row=0, column=2)

def modalWithOk(win, message, okCallback):
   pop = Toplevel(win)
   pop.title("Confirmation")
   geom = str(cfg.modalWidth) + "x" + str(cfg.modalHeight)
   pop.geometry(geom)
   pop.config(bg="white")
   # Create a Label Text
   label = Label(pop, text=message, font=('Aerial', cfg.modalFontSize), bg="white")
   label.pack(pady=20)
   # Add a Frame
   frame = Frame(pop, bg="white")
   frame.pack(pady=10)
   # Add Button for making selection
   button1 = Button(frame, text="OK", command=lambda: okCallback(pop), bg=cfg.errorButtonBgColor, fg="white")
   button1.grid(row=0, column=1)

def okCallback(pop):
    pop.destroy()
    cfg.txtPresoName.delete(0, END)

def setTimersForSentenceHighlighting():
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
        modalWithOk(cfg.rootWin, "Please wait for the current sound to finish playing", okCallback)
    else:
        cfg.rootWin.destroy()

