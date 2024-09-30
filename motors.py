import serial
import time

def sendCommandNTimes(serial, command, repetitions = 1, sleep_time = 0.1):
    for n in range(repetitions):
        serial.write(command)
        time.sleep(sleep_time)