
##Simulate a radar on a self-driving vehicle: Build a circuit with 5 IR sensors 
# pointed in a 360-degree fashion to mimic the range and obstacle detectors on a self-driving car. 
# Store data on obstacle detection of the four sensors by measuring the voltage output of the sensors 
# and the distance of the obstacles. Using Python, analyze this data about each IR sensor and 
# visualize the readings in a graph.

from pyfirmata2 import Arduino, INPUT
import time as clock
import csv
import matplotlib.pyplot as plt
 
PORT = "COM3" #what the ardunio usb port is
NUM_SENSORS = 5 
NUM_SAMPLES = 150 
SAMPLE_INTERVAL = 0.1 # collecting every 100ms for 100 samples = 10s test time total
 
SENSOR_PINS = [2, 3, 4, 5, 6]
set_distance = 5
board = Arduino(PORT)
board.samplingOn(100)
for n in range(NUM_SENSORS):
    board.digital[SENSOR_PINS[n]].mode = INPUT #setting the arduino to be the input for data
    board.digital[SENSOR_PINS[n]].enable_reporting() #make sure arduino collects data

wait_start = clock.time() #timer 
ready = False
while ready == False:
    ready = True
    for n in range(NUM_SENSORS):
        if board.digital[SENSOR_PINS[n]].value is None: #going throughj the pin numbers 
            ready = False #checking if values are being sent 
 
    if ready == False: #if the csv collects no data for over 3s tell user might be an error
        if clock.time() - wait_start > 3:
            raise RuntimeError("No data from sensors - check wiring and that StandardFirmata is uploaded")
        clock.sleep(0.05)#5ms delay
 
R_data = open("sensor_data.csv", "w", newline="") #setting up csv file in vs code
R_data.write("time,s1,s2,s3,s4,s5\n") #columns of csv file
 
print("Sampling for", NUM_SAMPLES * SAMPLE_INTERVAL, "seconds") #timer amount calculation
 
start = clock.time() #begin data collection
for i in range(NUM_SAMPLES):
    line = str(round(clock.time() - start, 3)) #start at 3s
 
    for n in range(NUM_SENSORS):
        value = board.digital[SENSOR_PINS[n]].value #creating values from arduino

        if value is None:
            raise RuntimeError(f"No reading received from sensor {n+1}") 
            # raise = execute, runtime error if theres no data collection 

        # low means an obstacle was detected, so 1 = triggered
        if value:
            line = line + ",0" 
        else:
            line = line + ",1"
 
    R_data.write(line + "\n")
    clock.sleep(SAMPLE_INTERVAL)
 
R_data.close()
 
R = open("sensor_data.csv")
reader = csv.reader(R) # getting all of the lists ready
next(reader)    # skip the header row
 
time = [0.0] * NUM_SAMPLES # multiple by num_samples gives that amount of slots in list
 
sensor1_trig = [0] * NUM_SAMPLES
 
sensor2_trig = [0] * NUM_SAMPLES
 
sensor3_trig = [0] * NUM_SAMPLES
 
sensor4_trig = [0] * NUM_SAMPLES
 
sensor5_trig = [0] * NUM_SAMPLES
 
 
i = 0
for row in reader: # one row at a time
    time[i] = float(row[0])
 
    for n in range(NUM_SENSORS):
        v = int(row[n + 1]) #creates a numerical value of the ir output (1 or 0)
 
        if n == 0:
            sensor1_trig[i] = v #for i in range of samples give that i row value to that sensor at that row
 
        elif n == 1:
            sensor2_trig[i] = v
 
        elif n == 2:
            sensor3_trig[i] = v
 
        elif n == 3:
            sensor4_trig[i] = v
 
        else:
            sensor5_trig[i] = v
 
    i = i + 1 #move to the next row 
R.close()
board.exit()

while True: # question loop, like to see data and what sensor

    answer = input("Would you like to view the data of an IR Sensor? ")

    if answer == "No" or answer == "no":
        break

    elif answer == "Yes" or answer == "yes":

        sensor = input("Which sensor would you like to choose? ")
    
        if sensor == "1":

            plt.plot(time, sensor1_trig) #creating the physical graph

            plt.xlabel("Time (Seconds)")
            plt.ylabel("Sensor triggered(2cm)")
            plt.title("IR Sensor 1 Trigger range vs time")

            plt.show()

            print("Here is the Sensor 1 triggered vs Time Graph")


        elif sensor == "2":

            plt.plot(time, sensor2_trig)
                
            plt.xlabel("Time (Seconds)")
            plt.ylabel("Sensor triggered(2cm)")
            plt.title("IR Sensor 2 Trigger range vs time")
                
            plt.show()
            print("Here is the Sensor 2 triggered vs Time Graph")
        elif sensor == "3":

            plt.plot(time, sensor3_trig)
            
            plt.xlabel("Time (Seconds)")
            plt.ylabel("Sensor triggered(2cm)")
            plt.title("IR Sensor 3 Trigger range vs time")
            
            plt.show()

            print("Here is the Sensor 3 triggered vs Time Graph")

        elif sensor == "4":

            plt.plot(time, sensor4_trig)
                        
            plt.xlabel("Time (Seconds)")
            plt.ylabel("Sensor triggered(2cm)")
            plt.title("IR Sensor 4 Trigger range vs time")
                        
            plt.show()
            
            print("Here is the Sensor 4 triggered vs Time Graph")
        elif sensor == "5":

            plt.plot(time, sensor5_trig)
                        
            plt.xlabel("Time (Seconds)")
            plt.ylabel("Sensor triggered(2cm)")
            plt.title("IR Sensor 5 Trigger range vs time")
                        
            plt.show()
            
            print("Here is the Sensor 5 triggered vs Time Graph")
        else:
            print("Please type a number for sensors 1 through 5")
    else:

        print("Please enter yes or no")

