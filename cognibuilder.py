import time
import threading

# Import modules
from comms import *
from comms.midi import *
from exercises import *
from exercises.notefinder import *
from gui import *
from gui.tkinter import Application

# Import stuff used by this script


# This method gets called by a thread that runs independently of the GUI
def mainLoop(midiIn, guiWindow):
	global keepThreadGoing

	# Wait for the window thread to start up
	while(True):
		try:
			guiWindow.showMessage("Window initialised")
			break
		except RuntimeError:
			#time.sleep(0.3)
			raise

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
			note=waitForNoteOn(midiIn)


# Define styles
#style = Style()
#style.configure("QuestionerText", size=12)
#style.configure("QuestionerText")

# Set up the GUI
app = Application()

# Set up the thread that responds to input
midiIn = initMidi()
midiListenerThread = threading.Thread(target=mainLoop, args=(midiIn,app))
global keepThreadGoing
keepThreadGoing=True
midiListenerThread.start()

app.root.mainloop()
keepThreadGoing=False