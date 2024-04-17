# GUI imports
import tkinter
from tkinter import *
import tkinter.ttk
from tkinter.ttk import *

# The class that handles GUI behaviour
class Application(Frame):
    def showMessage(self, message):
        self.outputBox["text"] = message

    def quitApp(self):
        Tk().quit()
		
	# Initialise the main GUI window
    def __init__(self, master=None, ):
        root = Tk()
        self.root = root
        root.title("CogniBuilder")
        super().__init__(root, padding="3 3 12 12")

        #mainframe = Frame(root, padding="3 3 12 12")
        self.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

		# Add widgets to it
        self.outputBox = Label(self)
        self.outputBox["text"] = "Output goes here"
        #self.outputBox["style"] = "QuestionerText"
        self.outputBox.grid(column=1, row=1, sticky=(W, E))
        
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        #self.QUIT["style"] = "QuestionerText"
        self.QUIT["command"] = self.quitApp
        self.QUIT.grid(column=1, row=2, sticky=(W, E))
