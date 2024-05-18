from tkinter import*
import random
import threading
import time
import os

#region TK

root = Tk()
root.title("UAV SIM")
root.geometry("320x260")
root.configure(border=0)
root.configure(bg="black")
root.update()

GRAY = "#383737"
RED = "#FF0000"
LIGHT_GRAY = "#787878"
DAHALIGHT_GRAY = "#828282"
GREEN = "#00ff1a"
WHITE = "#FFFFFF"

#endregion

#region params

# Constants
CL = 0.290
CD_horizontal = 0.113
CD_vertical = 0.300

rho = 1.225 # rooo
S = 0.180 # m^2

# Initial values
uav_trust = 0 # newton
uav_weight = 50 # Newton
uav_horizontal_speed = 0 # m/s
uav_veritcal_speed = 0
uav_climb_accel = 0 #newton
uav_accel = 0 # newton

uav_roll = 0 #degres
uav_yaw = 0 #degres
uav_pitch = 0 #degres

MAX_SPEED = 30

loc_lat = 0
loc_lon = 0
loc_alt = 0

#pwm
chanel_trust = 0
chanel_roll = 0 
chanel_pitch = 0
chanel_yaw = 0

# Simulation duration in seconds
simulasyon_suresi = 100

# Simulation step in seconds
dt = 0.1

#endregion

def lift(speed):
    return 0.5 * CL * rho * S * (speed ** 2)


def drag(speed,CD):
    return 0.5 * CD * rho * S * (speed ** 2)

def update():
    global uav_trust

    uav_trust = input_trust.get()
    uav_input_roll = input_roll.get()
    uav_input_yaw = input_yaw.get()
    uav_input_pitch = input_pitch.get()
    #print(uav_input_trust,uav_input_roll,uav_input_yaw,uav_input_pitch)

    return [uav_trust,uav_input_roll,uav_input_yaw,uav_input_pitch]


def loop():
    global uav_roll, uav_pitch, uav_yaw, uav_horizontal_speed, uav_veritcal_speed, uav_climb_accel, loc_alt
    for t in range(int(simulasyon_suresi/dt)):
        # Update thrust

        uav_trust = update()[0]


        # Calculate acceleration, velocity, lift
        uav_lift = lift(uav_horizontal_speed)

        uav_accel = (uav_trust - drag(uav_horizontal_speed, CD_horizontal)) / (uav_weight/9.81)
        uav_horizontal_speed += (uav_accel * dt)
    
        # Dikey hız için maksimum ve minimum sınırların uygulanması
        uav_veritcal_accel = (uav_lift - (drag(uav_veritcal_speed, CD_vertical)+uav_weight)) / (uav_weight/9.81)
        uav_veritcal_speed += uav_veritcal_accel * dt


        """uav_horizontal_speed = max(min(uav_horizontal_speed, MAX_SPEED), -MAX_SPEED)
        uav_veritcal_speed = max(min(uav_veritcal_speed, MAX_SPEED), -MAX_SPEED)"""
        
        # Print current state
        print("Time: ", t*dt)
       
        # Based on the above assumption, update roll, pitch, yaw
        """uav_roll += uav_roll_rate * dt
        uav_pitch += uav_pitch_rate * dt
        uav_yaw += uav_yaw_rate * dt"""

        loc_alt += uav_veritcal_speed * dt

        if loc_alt < 0:
            loc_alt = 0
            uav_veritcal_speed = 0

        os.system("cls")

        # Print current state
        print("Time: ", t*dt)
        print("Thrust: ", uav_trust)
        print("Roll: ", uav_roll)
        print("Pitch: ", uav_pitch)
        print("Yaw: ", uav_yaw)
        print("Speed-veritcal: ", uav_veritcal_speed)
        print("Speed-horizontal: ", uav_horizontal_speed)
        print("Drag:-vertical ", drag(uav_veritcal_speed,uav_veritcal_speed))
        print("Drag:-horizontal ", drag(uav_horizontal_speed,uav_horizontal_speed))
        print("Lift: ", uav_lift)
        print("Position: Lat {}, Lon {}, Alt {}".format(loc_lat, loc_lon, loc_alt))
        print("------")

        telemetry = {
            "Time":t*dt

        }

        # Sleep for a while to match the real-time speed
        time.sleep(dt)
            
        

#region slider
input_trust = Scale(root, from_=0, to=30, length=200, orient=VERTICAL)
input_trust.place(x=25,y=50)

input_roll = Scale(root, from_=0, to=360, length=200, orient=VERTICAL)
input_roll.place(x=100,y=50)

input_yaw = Scale(root, from_=0, to=360, length=200, orient=VERTICAL)
input_yaw.place(x=175,y=50)

input_pitch = Scale(root, from_=0, to=180, length=200, orient=VERTICAL)
input_pitch.place(x=250,y=50)

#endregion

#region text
trust_text = Label(root, text="trust", font=("Arial", 9))
trust_text.place(x=40,y=30)

roll_text = Label(root, text="roll", font=("Arial", 9))
roll_text.place(x=115,y=30)

yaw_text = Label(root, text="yaw", font=("Arial", 9))
yaw_text.place(x=190,y=30)

yaw_pitch = Label(root, text="pitch", font=("Arial", 9))
yaw_pitch.place(x=265,y=30)

#endregion

loop_thread = threading.Thread(target=loop)
loop_thread.start()

root.mainloop()


    