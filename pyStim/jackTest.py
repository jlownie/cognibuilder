import jack
import time


print('Setting up JACK clients')

client = jack.Client('MyGreatClient')
client.inports.register('input_1')
jack.OwnPort('MyGreatClient:input_1', client)
client.outports.register('output_1')
jack.OwnPort('MyGreatClient:output_1', client)

while 1:
	time.sleep(1)
