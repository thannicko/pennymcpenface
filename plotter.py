import serial
import math
import time
import argparse
from create_rectangle import create_rectangle, plot_rectangle_path
from geometry import cartesian_to_cylindrical, convert_radius_coordinates_to_mm
from motors import sendCommandNTimes, readPosition, readRadiusPositionMM

# RADIUS      = 285  # mm (23 cm)
cmd_up      = 'w'
cmd_down    = 's'
cmd_left    = 'a'
cmd_right   = 'd'
min_angle   = 0.2 #degree
min_radius  = 2 #mm

theta_position_conversion = 2840

# calibration shows the linear motor moves differently up and down
min_radius_up =  4.8#mm
min_radius_down = 4.5

min_radius_up =  2#mm
min_radius_down = 2


def plot(ser, path, r_0, theta_0, sleep_time=0.1):
    # r_prev      = path[0][0]
    # theta_prev  = path[0][1]
    theta_offset   = path[0][1]
    theta_prev     = theta_0 + theta_offset
    
    r_prev      = r_0
    # theta_prev  = 0
    
    
    try:
        for r, theta in path:
            print(f"Current position: r: {r_prev}mm, theta: {round(theta_prev)}")
            delta_r     = round(r - r_prev,1)
            delta_theta = round(theta - theta_prev,1)
            
            
            if abs(delta_r) >= min_radius:
                if delta_r > 0:
                    r_steps = abs(round(delta_r/min_radius_up)) # how many steps to move
                    print(f"Moving {delta_r}mm in {r_steps} steps")
                    
                    sendCommandNTimes(serial=ser,
                                        command = cmd_up.encode(),
                                        repetitions=r_steps,
                                        sleep_time=sleep_time*2)
                    
                elif delta_r < 0:
                    r_steps = abs(round(delta_r/min_radius_down)) # how many steps to move
                    print(f"Moving {delta_r}mm in {r_steps} steps")
                    sendCommandNTimes(serial=ser,
                                        command = cmd_down.encode(),
                                        repetitions=r_steps,
                                        sleep_time=sleep_time*2)
                
                r_prev = r - (delta_r%min_radius)
                r_prev = readRadiusPositionMM(serial=ser)
                # r_prev = r

            if abs(delta_theta) >= min_angle:
                theta_steps = abs(round(delta_theta/min_angle)) # how many steps to move
                print(f"Moving {delta_theta} degrees in {theta_steps} steps")
                if delta_theta > 0:
                    sendCommandNTimes(serial=ser,
                                        command = cmd_right.encode(),
                                        repetitions=theta_steps,
                                        sleep_time=sleep_time)
                elif delta_theta < 0:
                    sendCommandNTimes(serial=ser,
                                        command = cmd_left.encode(),
                                        repetitions=theta_steps,
                                        sleep_time=sleep_time)
                # print(delta_theta)
                theta_prev = theta - (delta_theta%min_angle)
                rg, theta_prev = readPosition(serial=ser)
                theta_prev = theta_prev + theta_offset
                # theta_prev = theta
    
    except(KeyboardInterrupt):
        print("... interrupted!")
        ser.close()

def main(args):
    SERIAL_PORT = args.port
    # Connect
    ser = serial.Serial(SERIAL_PORT, 9600)
    ser.flush()
    
    path = create_rectangle(x = 60, y = 60, step = 1, y_offset = 290)
    plot_rectangle_path(rect_points = path)
    path = cartesian_to_cylindrical(cartesian_points = path)
    # plot_cylindrical_path(cylindrical_points=path)
    # print(path)
    
    r_0, theta_0 = readPosition(ser)
    # r_0_mm = convert_radius_coordinates_to_mm(radius=r_0)
    r_0_mm = readRadiusPositionMM(serial=ser)
    r_prev      = path[0][0]
    theta_prev  = path[0][1]
    print(f"Current postion: \n         r0: {r_0_mm}\n         t0: {0}")
    print(f"Start position: \n         r: {r_prev}\n         t0: {theta_prev}")
    
    plot(ser=ser, path=path, r_0=r_0_mm, theta_0=theta_0)
    
    
    ser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Penny McPenface Plotter <3")
    parser.add_argument("-p", "--port", default="/dev/cu.usbmodem101", type=str, required=False, help="Serial port")

    args = parser.parse_args()
    main(args)