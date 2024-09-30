import serial
import time
from geometry import convert_radius_coordinates_to_mm

def sendCommandNTimes(serial, command, repetitions = 1, sleep_time = 0.1):
    for n in range(repetitions):
        serial.flushInput()
        serial.reset_output_buffer()
        serial.reset_input_buffer()
        serial.write(command)
        time.sleep(sleep_time)
        
        
def readPosition(serial):
    # serial.flushInput()
    while(1):
        try:
            serial.reset_output_buffer()
            serial.reset_input_buffer()
            # serial.read()
            serial.readline()
            raw_data = serial.readline()
            decoded_data = raw_data.strip().decode()
            decoded_data = [value for value in decoded_data.split(',')]
            # print(decoded_data)
            if len(decoded_data) == 4:
                r = int(decoded_data[1])       
                theta = int(decoded_data[3])
                # print(f"r: {r}, theta: {theta}")
                theta_degree = theta/2840
                return r, theta_degree
            print("Could not read position")
        
        except(KeyboardInterrupt):
            print("... interrupted!")
            serial.close()
        
        except:
            print("Error reading postion")
            break


def readRadiusPositionMM(serial):
    r, theta = readPosition(serial) 
    return convert_radius_coordinates_to_mm(radius = r)
