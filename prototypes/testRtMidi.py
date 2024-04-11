import time
import rtmidi
from rtmidi.midiutil import open_midiinput

def sendNotes():
	midiout = rtmidi.MidiOut()
	available_ports = midiout.get_ports()

	if available_ports:
		midiout.open_port(0)
	else:
		midiout.open_virtual_port("My virtual output")
	
	note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
	note_off = [0x80, 60, 0]
	while 1:
		try:
			print('Sending note')
			time.sleep(3)
			midiout.send_message(note_on)
			time.sleep(0.5)
			midiout.send_message(note_off)
		except (KeyboardInterrupt):
			print('Exiting')
			del midiout
			quit()

def showNotes():
	try:
		midiin, port_name = open_midiinput('28:0')
	except (EOFError, KeyboardInterrupt):
		print('Failed to open port')
		quit()
	print('Opened port successfully')

	# Poll for notes
	print("Entering main loop. Press Control-C to exit.")
	try:
		timer = time.time()
		while True:
			msg = midiin.get_message()

			if msg:
				message, deltatime = msg
				timer += deltatime
				print("[%s] @%0.6f %r" % (port_name, timer, message))

			time.sleep(0.01)
	except KeyboardInterrupt:
		print('')
	finally:
		print("Exit.")
		midiin.close_port()
		del midiin

def showNotesJack():
	try:
		midiIn=rtmidi.MidiIn(rtmidi.API_UNIX_JACK, 'testRtMidi Client')
		midiIn.open_port(0)
		port_name=midiIn.get_port_name(0)
	except (EOFError, KeyboardInterrupt):
		print('Failed to open port')
		quit()
	print('Opened port successfully')

	# Poll for notes
	print("Entering main loop. Press Control-C to exit.")
	try:
		timer = time.time()
		while True:
			msg = midiIn.get_message()

			if msg:
				message, deltatime = msg
				timer += deltatime
				print("[%s] @%0.6f %r" % (port_name, timer, message))

			time.sleep(0.01)
	except KeyboardInterrupt:
		print('')
	finally:
		print("Exit.")
		midiIn.close_port()
		del midiIn

#sendNotes()
#showNotes()
showNotesJack()


