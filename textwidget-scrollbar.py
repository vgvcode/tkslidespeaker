from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Create an instance of tkinter frame
win=Tk()

# Set the geometry
win.geometry("700x350")

# Add a Scrollbar(horizontal)
v=Scrollbar(win, orient='vertical')
v.pack(side=RIGHT, fill='y')

# Add a text widget
text=Text(win, font=("Georgia, 24"), yscrollcommand=v.set)

# Add some text in the text widget
for i in range(10):
   text.insert(END, "Welcome to Tutorialspoint...\n\n")

# Attach the scrollbar with the text widget
v.config(command=text.yview)
text.pack()

win.mainloop()