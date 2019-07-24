import Tkinter
from Tkinter import *
import ttk
from ttk import *

class Application(Frame):
    def say_hi(self):
        #print "hi there, everyone!"
        self.outputBox["text"] = "hi there, everyone!"

    def createWidgets(self):
        self.outputBox = ttk.Label(self)
        self.outputBox["text"] = "Output goes here"
        self.outputBox.pack({"side": "top"})
        
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
#        self.QUIT["style"]   = "BW.redText"
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

root = Tk()
app = Application(master=root)

# Define styles
style = Style()
style.configure("BW.redText", foreground="red", background="white")

app.mainloop()
root.destroy()
