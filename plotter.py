import serial
import math
import time
import argparse
from create_rectangle import create_rectangle, plot_rectangle_path
from geometry import cartesian_to_cylindrical
import time

RADIUS = 230  # mm (23 cm)
cmd_up      = 'w'
cmd_down    = 's'
cmd_left    = 'a'
cmd_right   = 'd'
min_angle   = 1 #degree
min_radius  = 5 #mm

def main(args):
    SERIAL_PORT = args.port
    # Connect
    ser = serial.Serial(SERIAL_PORT, 9600)
    # ser.open()
    ser.flush()
    
    path = create_rectangle(x = 50, y = 70, step = 1, y_offset = 270)
    # plot_rectangle_path(rect_points = path)
    path = cartesian_to_cylindrical(cartesian_points = path)
    # print(path)
    r_prev      = path[0][0]
    theta_prev  = path[0][1]
    try:
        for r, theta in path:
            delta_r     = round(r - r_prev)
            delta_theta = round(theta - theta_prev)
            
            if abs(delta_r) >= min_radius:
                print(delta_r)
                
                #TODO move actual number of steps
                if delta_r > 0:
                    # for step in delta_r%min_radius
                    # assuming it's just one step
                    ser.write(cmd_up.encode()) 
                    time.sleep(0.1)
                    
                elif delta_r < 0:
                    ser.write(cmd_down.encode())
                    time.sleep(0.1)
                
                r_prev = r

            if abs(delta_theta) >= min_angle:
                if delta_theta > 0:
                    ser.write(cmd_right.encode()) 
                    time.sleep(0.1)
                elif delta_theta < 0:
                    ser.write(cmd_left.encode())
                    time.sleep(0.1)
                print(delta_theta)
                theta_prev = theta
                #TODO move number of steps


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