# GUI imports
import tkinter
from tkinter import *
import tkinter.ttk
from tkinter.ttk import *

# Midi import
import rtmidi

# Standard imports
import time
import threading

# Global vars

# Constants
NOTENAMES_SHARPS=('A','A#', 'B', 'C','C#', 'D','D#', 'E', 'F','F#', 'G','G#' )
NOTENAMES_FLATS=('A','Ab', 'B', 'Bb', 'C', 'D','Db', 'E', 'Eb', 'F', 'G','Gb' )

# MIDI potocol constants
TYPE_BITMASK=0b10000000
CHANNEL_BITMASK=0b00001111
MESSAGE_BITMASK=0b01110000

# Helper class for asking questions
class QuestionFindNote:
	questionText=None
	answer=None
	
	def __init__(self):
		pass

# A wrapper for MIDI notes
class MIDINote:
	noteNumber=None # 1 is A, 11 is G#
	
	# Notemessage structure is ([144, 55, 91], 0.0)
	def __init__(self, noteMessage=None):
		if(noteMessage):
			statusByte=noteMessage[0][0]
			logMsg('statusByte is: ' + str(statusByte))
			if(self.isStatusByte(statusByte)):
				logMsg('This is a status byte')
			else:
				logMsg('This is not a status byte')
	
	def isStatusByte(self, byte):
		typePayload=byte & TYPE_BITMASK
		if(typePayload == 0b10000000):
			return True
		return False

# The GUI class
class Application(Frame):
    def showMessage(self, message):
        self.outputBox["text"] = message

    def createWidgets(self):
        self.outputBox = Label(self)
        self.outputBox["text"] = "Output goes here"
        self.outputBox.pack({"side": "top"})
        
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "bottom"})

    def __init__(self, master=None, ):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()        

def logMsg(message):
	print(message)

def getQuestion():
	newQuestion=QuestionFindNote()
	newQuestion.questionText='Find the note D'
	newQuestion.answer=6
	return newQuestion

def listenForMIDI(midiIn, guiWindow):
	global keepThreadGoing

	# Keep asking questions until exit
	while(keepThreadGoing):
		thisQuestion=getQuestion()
		
		# Keep waiting for a MIDI note
		while(keepThreadGoing):
			msg = midiIn.get_message()
			if msg:
				note=MIDINote(msg)
				noteArrived(note, guiWindow)
			time.sleep(0.3)
	
def noteArrived(note, guiWindow):
	fullMessage = 'Note arrived. Pitch: ' + str(note.noteNumber)
	print(fullMessage)
	guiWindow.showMessage(fullMessage)
	#print("[%s] @%0.6f %r" % (port_name, timer, message))

def initMidi():
	try:
		midiIn=rtmidi.MidiIn(rtmidi.API_UNSPECIFIED, 'NoteFinder')
		midiIn.open_port(0)
		port_name=midiIn.get_port_name(0)
	except (EOFError, KeyboardInterrupt):
		print('Failed to open port')
		quit()
	print('Opened port successfully')
	return midiIn

# Set up the GUI
root = Tk()
app = Application(master=root)

# Set up the MIDI listener
midiIn = initMidi()
midiListenerThread = threading.Thread(target=listenForMIDI, args=(midiIn,app))
keepThreadGoing=True
midiListenerThread.start()

app.mainloop()
root.destroy()
keepThreadGoing=False
