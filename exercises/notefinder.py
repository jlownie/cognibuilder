import random
from random import randint
from enum import auto
import comms.logger
from comms.logger import logMsg

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

def getQuestion():	
	return QuestionNoteByName()
