# Python script to record sensor readings from a Sense HAT for
# BYU-I Rocket Team 2018. Some of these readings will include 
# pressure (atmospheric) as well as gyro readings. All of this
# will be added and put to a .csv file to be examined at a later
# time.
# Author: Joseph Ridgley
# Date: 5/30/18
# TODO
# Add X Y Z AXIS INFORMATION TO CSV FILE
# Update date on raspberry pi
# Calibrate pressure sensor

import time
import datetime
import os

from sense_hat import SenseHat

# Declare a SenseHat instance
sense = SenseHat()

# Turn the LED Matrix off
sense.clear()


# Ask the user how long they would like to run the program
lengthOfTest = int(input("How long is this test? (in Minutes): "))

# Convert the length of the test to seconds
lengthOfTest *= lengthOfTest * 60

# open CSV file
file = open("/home/pi/RocketTeam/SenseHAT/Sensor Readings" + str(datetime.datetime.now()) + ".csv", "a")

# Header of the CSV file
file.write("Test Date: " + str(datetime.datetime.now().date()) + "\n")
file.write("Test Duration (s): " + str(lengthOfTest) + "\n\n")
file.write("Time Stamp, Pressure (PSI),,Time Stamp, X (rads/s), Y (rads/s) , Z (rads/s),,Time Stamp, Pitch (degrees), Roll (degrees), Yaw (degrees)\n")

# Get a start time for the test
start = time.time()

# set lengthOfTest to 1 second just for example
# REMOVE BEFORE ACTUALLY USING
lengthOfTest = 1

# Activate the gyro, disables the compass and accelerometer
sense.set_imu_config(False, True, False)

# Loop to write a bunch of the current pressure readings for the duration
# of the test
while time.time() - start < lengthOfTest:
	# Retrieve the pressure from the SenseHat
	pressure = sense.get_pressure() / 68.9476
	# Retrieve the raw GYRO readings. This function returns a dictionary indexed with strings x, y, z.
	# The values are floats representing rotational intensity of the axis in RADIANS PER SECOND.
	rawGYRO = sense.get_gyroscope_raw()
	gyro = sense.get_gyroscope()

	now = time.time() - start
	file.write(str(now) + "," + str(pressure) + ",," 
		+ str(now) + "," +  str(rawGYRO.get("x")) + "," + str(rawGYRO.get("y")) + "," + str(rawGYRO.get("z")) + ",," +
		str(now) + "," + str(gyro.get("pitch")) + "," + str(gyro.get("roll")) + str(gyro.get("yaw")))

	# force the file to be saved right away, WE DONT WANNA LOOSE DATA
	os.fsync(file)
