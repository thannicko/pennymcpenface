import serial
import math
import time
import argparse
from create_rectangle import create_rectangle, plot_rectangle_path
from geometry import cartesian_to_cylindrical
from motors import sendCommandNTimes

RADIUS = 230  # mm (23 cm)
cmd_up      = 'w'
cmd_down    = 's'
cmd_left    = 'a'
cmd_right   = 'd'
min_angle   = 0.2 #degree
min_radius  = 5 #mm




def main(args):
    SERIAL_PORT = args.port
    # Connect
    ser = serial.Serial(SERIAL_PORT, 9600)
    # ser.open()
    ser.flush()
    
    path = create_rectangle(x = 50, y = 70, step = 1, y_offset = 270)
    plot_rectangle_path(rect_points = path)
    path = cartesian_to_cylindrical(cartesian_points = path)
    # print(path)
    r_prev      = path[0][0]
    theta_prev  = path[0][1]
    try:
        for r, theta in path:
            delta_r     = round(r - r_prev)
            delta_theta = round(theta - theta_prev)
            
            if abs(delta_r) >= min_radius:
                r_steps = abs(round(delta_r/min_radius)) # how many steps to move
                print(f"Moving {delta_r}mm in {r_steps} steps")
                
                #TODO move actual number of steps
                if delta_r > 0:
                    # for step in delta_r%min_radius
                    # assuming it's just one step
                    # ser.write(cmd_up.encode()) 
                    # time.sleep(0.1)
                    sendCommandNTimes(serial=ser,
                                        command = cmd_up.encode(),
                                        repetitions=r_steps)
                    
                elif delta_r < 0:
                    sendCommandNTimes(serial=ser,
                                        command = cmd_down.encode(),
                                        repetitions=r_steps)
                
                r_prev = r - (delta_r%min_radius)

            if abs(delta_theta) >= min_angle:
                theta_steps = abs(round(delta_theta/min_angle)) # how many steps to move
                print(f"Moving {delta_theta} degrees in {theta_steps} steps")
                if delta_theta > 0:
                    sendCommandNTimes(serial=ser,
                                        command = cmd_right.encode(),
                                        repetitions=theta_steps)
                elif delta_theta < 0:
                    sendCommandNTimes(serial=ser,
                                        command = cmd_left.encode(),
                                        repetitions=theta_steps)
                print(delta_theta)
                theta_prev = theta - (delta_theta%min_angle)


    except(KeyboardInterrupt):
        print("... interrupted!")
        ser.close()
        
        # print(f"R: {round(r)}, theta: {round(theta)}")

    

    
    # try:
    #     for x in range(0,42):
    #         ser.write(cmd_up.encode())  
            
    # except(KeyboardInterrupt):
    #     print("... interrupted!")
    #     ser.close()
    
    ser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Penny McPenface Plotter <3")
    parser.add_argument("-p", "--port", default="/dev/cu.usbmodem101", type=str, required=False, help="Serial port")

    args = parser.parse_args()
    main(args)