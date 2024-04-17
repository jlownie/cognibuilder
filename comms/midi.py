# Import parent module
import comms.logger
from comms.logger import logMsg

# Midi imports
import rtmidi
from enum import Enum, auto

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
