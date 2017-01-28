import serial, time, datetime

# Configure serial ports for the devices
U1241A_serialPortName = 'COM18'
DMMSwitchBoard_serialPortName = 'COM3'

# Open both serial ports
serial_U1241A = serial.Serial(U1241A_serialPortName, 9600)
serial_DMMSwitch = serial.Serial(DMMSwitchBoard_serialPortName)

# Set meter to 10V range
serial_U1241A.write("CONF:VOLT:DC 10\r\n".encode());

def GetU1241A_reading():
	serial_U1241A.write("FETC?\r\n".encode())
	reading = serial_U1241A.readline()
	return float(reading.decode('utf-8'))


def SwitchRelayAndWait(relay):
	serial_DMMSwitch.write((relay).to_bytes(1, 'big'))
	time.sleep(0.5)

try:
	print("Datetime, \t\t\tChannel 1, \tChannel 2")
	while(True):
		SwitchRelayAndWait(1)
		reading_ch1 = GetU1241A_reading()
		SwitchRelayAndWait(2)
		reading_ch2 = GetU1241A_reading()
		print(str(datetime.datetime.now()) + ", \t" +str(reading_ch1) + ", \t\t" + str(reading_ch2))

except (KeyboardInterrupt, SystemExit):
	serial_DMMSwitch.close()
	serial_U1241A.close()