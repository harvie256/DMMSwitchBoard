#
# This example has the scanning card setup to measure the efficency across a small DC-DC converter.
# Setup is as follows:
# CH1 - Input Voltage
# CH2 - Input Current (voltage across known sense resistor)
# CH3 - Output Voltage
# CH4 - Output Current (voltage across known sense resistor)
#
# Each time Enter is pressed it takes a scan of the inputs and records in a file
# this allows manually changing the load on the PSU and taking recordings.  This
# could be replaced by a PC controlled load to fully automate.


import serial, time, datetime

# Configure serial ports for the devices
U1241A_serialPortName = 'COM18'
DMMSwitchBoard_serialPortName = 'COM3'

_InputISenseResistor = 1.2
_OutputISenseResistor = 1.2


# Open both serial ports
serial_U1241A = serial.Serial(U1241A_serialPortName, 9600)
serial_DMMSwitch = serial.Serial(DMMSwitchBoard_serialPortName)


def GetU1241A_reading():
	serial_U1241A.write("FETC?\r\n".encode())
	reading = serial_U1241A.readline()
	return float(reading.decode('utf-8'))


def SwitchRelayAndWait(relay):
	serial_DMMSwitch.write((relay).to_bytes(1, 'big'))
	time.sleep(0.5)

def PrintAndWriteWithoutTabs(ioFile, stringToWrite):
	print(stringToWrite)
	ioFile.write(stringToWrite.replace('\t', '') + "\n")

try:
	recFile = open('c:\\temp\\output.csv', 'w');

	print("Press enter to scan all channels and record, x + enter to finish")

	PrintAndWriteWithoutTabs(recFile, "Datetime, \t\tInput (V), \tInput (I), \tOutput (V), \tOutput (I), \tInput (P), \tOutput (P), \tEfficency (%)");

	while(True):
		if(input().strip() == "x"):
			serial_DMMSwitch.close()
			serial_U1241A.close()
			recFile.close()
			break

		# Measure on the 10V range
		serial_U1241A.write("CONF:VOLT:DC 10\r\n".encode());
		SwitchRelayAndWait(1)
		reading_ch1 = GetU1241A_reading()
		SwitchRelayAndWait(3)
		reading_ch3 = GetU1241A_reading()

		# Measure the currents on the 1V range
		serial_U1241A.write("CONF:VOLT:DC 1\r\n".encode());
		SwitchRelayAndWait(2) 
		reading_ch2 = GetU1241A_reading() / _InputISenseResistor
		SwitchRelayAndWait(4)
		reading_ch4 = GetU1241A_reading() / _OutputISenseResistor

		OutputPower = reading_ch3 * reading_ch4
		InputPower = reading_ch1 * reading_ch2
		PrintAndWriteWithoutTabs(recFile, str(datetime.datetime.now()) + ", \t" +str(reading_ch1) + ", \t\t" + str(reading_ch2)
						   + ", \t" +str(reading_ch3) + ", \t" + str(reading_ch4) + ", \t" + str(InputPower) + ", \t" + str(OutputPower)
						   + ", \t" + str(100 * OutputPower / InputPower));


except:
	serial_DMMSwitch.close()
	serial_U1241A.close()
	recFile.close()
	raise




