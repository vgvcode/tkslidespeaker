from threading import Timer

def highlightText(txtWidget, tag, start, end):
    txtWidget.tag_add(tag, start, end)
    txtWidget.tag_configure(tag, background="OliveDrab1", foreground="black")

def unHighlightText(txtWidget, tag, start, end):
    txtWidget.tag_add(tag, start, end)
    txtWidget.tag_configure(tag, background="white", foreground="black")


# Import the required library
from tkinter import *

# Create an instance of tkinter frame
win=Tk()

# Set the geometry
win.geometry("700x350")

# Add a text widget
text=Text(win, width=80, height=15, font=('Calibri 12'))

# Set default text for text widget
text.insert(END, "Tkinter is a Python Library to create GUI-based applications.Learning Tkinter is Awesome!!")
#text.insert(END, "Learning Tkinter is Awesome!!")
text.pack()

# Select Text by adding tags
#text.tag_add("start", "1.0","1.7")
#text.tag_configure("start", background="OliveDrab1", foreground="black")
#text.pack()

t1 = Timer(1.2, highlightText, [text, "start1-on", "1.0", "1.7"])

t2 = Timer(3.1, unHighlightText, [text, "start1-off", "1.0", "1.7"])
t3 = Timer(3.2, highlightText, [text, "start2-on", "1.80", "1.85"])

t4 = Timer(5.0, unHighlightText, [text, "start2-off", "1.80", "1.85"])

t1.start()
t2.start()
t3.start()
t4.start()

#highlightText(text, "start", "1.0", "1.7")"])
#highlightText(text, "start", "1.0", "1.7")


win.mainloop()