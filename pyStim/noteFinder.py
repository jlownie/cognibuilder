# GUI imports
import tkinter
from tkinter import *
import tkinter.ttk
from tkinter.ttk import *
from enum import Enum, auto
import random
from random import randint

# Midi import
import rtmidi

# Standard imports
import time
import threading

class NoteQuestion():
	NOTENAMES_SHARPS=('A','A#', 'B', 'C','C#', 'D','D#', 'E', 'F','F#', 'G','G#' )
	NOTENAMES_FLATS=('A', 'Bb', 'B', 'C', 'Db','D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab' )
	SHARPS=auto()
	FLATS=auto()

# Ask for a note by name - any octave
class QuestionNoteByName(NoteQuestion):
	questionText=None
	answer=None
	accidentalType=None
	noteNames=None
	
	def __init__(self):
		self.answer=randint(1, 12)
		logMsg('question init: Answer is ' + str(self.answer))
		sharpOrFlat=randint(1, 2)
		if(sharpOrFlat==1):
			self.accidentalType=self.SHARPS
			self.noteNames=self.NOTENAMES_SHARPS
		else:
			self.accidentalType=self.FLATS
			self.noteNames=self.NOTENAMES_FLATS
		self.questionText='Find the note ' + self.noteNames[self.answer - 1]

# MIDI protocol constants
class MIDI_BITMASK():
	BYTE_TYPE=0b10000000
	CHANNEL=0b00001111
	MESSAGE=0b01110000
	NOTE_ON=0b00010000
	NOTE_OFF=0b00000000

class MIDI_MESSAGE_TYPE(Enum):
	NOTE_ON=auto()
	NOTE_OFF=auto()

# A wrapper for MIDI notes
class MIDINote:
	keyNumber=None # A0=21, A1=33, etc, 108=C8
	channel=None # 0-15
	messageType=None
	messageTypeString=None
	
	# Example notemessage is ([144, 55, 91], 0.0)
	def __init__(self, noteMessage=None):
		if(noteMessage):
			statusByte=noteMessage[0][0]
			if(noteMessage[0][1]):
				firstDataByte=noteMessage[0][1]
			if(noteMessage[0][2]):
				secondDataByte=noteMessage[0][2]

			# Decode the message			
			self.channel=self.getChannel(statusByte)
			thisMessageType=self.getMessageType(statusByte)
			if(thisMessageType - MIDI_BITMASK.NOTE_ON == 0):
				self.messageType=MIDI_MESSAGE_TYPE.NOTE_ON
				self.messageTypeString='Note on'
				self.keyNumber=firstDataByte
			elif(thisMessageType - MIDI_BITMASK.NOTE_OFF == 0):
				self.messageType=MIDI_MESSAGE_TYPE.NOTE_OFF
				self.messageTypeString='Note off'
				self.keyNumber=firstDataByte
	
	def isStatusByte(self, byte):
		typePayload=byte & MIDI_BITMASK.BYTE_TYPE
		if(typePayload == 0b10000000):
			return True
		return False

	def getChannel(self, byte):
		channelPayload=byte & MIDI_BITMASK.CHANNEL
		return channelPayload

	def getMessageType(self, byte):
		typePayload=byte & MIDI_BITMASK.MESSAGE
		return typePayload

# The GUI class
class Application(Frame):
    def showMessage(self, message):
        self.outputBox["text"] = message

    def quitApp(self):
        self.quit()
		
    def createWidgets(self):
        self.outputBox = Label(self)
        self.outputBox["text"] = "Output goes here"
        self.outputBox.pack({"side": "top"})
        
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["command"] = self.quitApp

        self.QUIT.pack({"side": "bottom"})

    def __init__(self, master=None, ):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()        

def logMsg(message):
	print(message)

def getQuestion():	
	return QuestionNoteByName()

# This method gets called by a thread that runs independently of the GUI
def mainLoop(midiIn, guiWindow):
	global keepThreadGoing

	# Loop until the quit button is pressed
	while(keepThreadGoing):
		# Display the question
		thisQuestion=getQuestion()
		guiWindow.showMessage(thisQuestion.questionText)

		note=waitForNoteOn(midiIn)
		if note:
			# Give feedback
			noteArrived(note, guiWindow, thisQuestion) 
			
			# Wait for a keypress
			waitForNoteOn(midiIn)

def waitForNoteOn(midiIn):
	global keepThreadGoing
	note=None

	# Wait for a note-on event
	gotNoteOn=False
	while(not gotNoteOn and keepThreadGoing):
		msg = midiIn.get_message()
		while(not msg and keepThreadGoing):
			time.sleep(0.3)
			msg = midiIn.get_message()
		if(msg):
			note=MIDINote(msg)
			if(note.messageType == MIDI_MESSAGE_TYPE.NOTE_ON):
				gotNoteOn=True
	return note
	
def noteArrived(note, guiWindow, thisQuestion):
	# Convert the note to a number from 1-12
	answer=(note.keyNumber - 21)%12+1
	logMsg('noteArrived: Answer is ' + str(answer))
	logMsg('noteArrived: Correct answer is ' + str(thisQuestion.answer))
	# Compare with correct answer and give feedback
	if(answer==thisQuestion.answer):
		guiWindow.showMessage('Congratulations! You pressed the correct key\n\nPress any note to continue')
	else:
		wrongAnswer=thisQuestion.noteNames[answer-1] # The index of the first array element is 0 but the first note is 1
		rightAnswer=thisQuestion.noteNames[thisQuestion.answer-1]
		guiWindow.showMessage(f'The correct key was {rightAnswer}, the key you pressed was {wrongAnswer}\n\nPress any note to continue')

def initMidi():
	try:
		midiIn=rtmidi.MidiIn(rtmidi.API_UNSPECIFIED, 'NoteFinder')
		midiIn.open_port(0)
		port_name=midiIn.get_port_name(0)
	except (EOFError, KeyboardInterrupt):
		logMsg('Failed to open port')
		quit()
	logMsg('Opened port successfully')
	return midiIn

# Set up the GUI
root = Tk()
app = Application(master=root)

# Set up the thread that responds to input
midiIn = initMidi()
midiListenerThread = threading.Thread(target=mainLoop, args=(midiIn,app))
global keepThreadGoing
keepThreadGoing=True
midiListenerThread.start()

app.mainloop()
root.destroy()
keepThreadGoing=False
