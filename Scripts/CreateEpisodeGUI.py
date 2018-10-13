from tkinter import *
from TableTester import *

def show_result():
    resulttext.delete(1.0, END)
    resulttext.insert(INSERT, EpisodeFromShow(e1.get()))

window = Tk()
window.title("Random Episode Generator")
label = Label(window, text="Enter your show:")
label.grid(row=0, sticky=W)
e1 = Entry(window, width=22)
e1.grid(row=0, column=1, sticky=W)
button = Button(window, text="Choose", width=10, command=show_result)
button.grid(row=0, column=2, sticky=E)
#frame = Frame(window)
#frame.grid(row=1)
resulttext = Text(window, width=40, height=3)
resulttext.grid(row=1, columnspan=3)
#resulttext.insert(INSERT, "")

window.mainloop()