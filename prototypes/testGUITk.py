# python3 version of the code
import tkinter
from tkinter import *
import tkinter.ttk
from tkinter.ttk import *

class Application(Frame):
    def say_hi(self):
        #print "hi there, everyone!"
        self.outputBox["text"] = "hi there, everyone!"

    def createWidgets(self):
        self.outputBox = Label(self)
        self.outputBox["text"] = "Output goes here"
        self.outputBox.pack({"side": "top"})
        
        self.QUIT = tkinter.ttk.Button(self)
        self.QUIT["text"] = "QUIT"
        #print("Style: " + self.QUIT["style"])
        self.QUIT['style'] = "TButton"
        #print("Style: " + self.QUIT["style"])
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

# Define styles
style = Style()
print("Background is " + style.lookup("TButton", 'background'))
#style.configure("TButton", borderwidth='6', background="green", relief='true', padding='30', space='30', text='nothing', foreground='#FFF')
style.configure("TButton", foreground="green")
print("Background is " + style.lookup("TButton", 'background'))
print("Layout is " + str(style.layout("TButton")))
print("Options are " + str(style.element_options("TButton.border")))
print("Options are " + str(style.element_options("TButton.padding")))
print("Options are " + str(style.element_options("TButton.label")))
#style.configure('blah.Button', padding="6", size="20", background="#CCC", font='helvetica 24')
root = Tk()
app = Application(master=root)


app.mainloop()
root.destroy()
