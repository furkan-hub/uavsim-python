from tkinter import*
import random
import threading
import time
import os
from cordinate_sys import *
import math

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

#katsayılar
CL = 0.290
CD_horizontal = 0.113
CD_vertical = 3.8

rho = 1.225 # rooo
S = 0.180 # m^2

#başlangıç değerleri
uav_weight = 50 # Newton
uav_horizontal_speed = 0 # m/s
uav_accel_horizontal = 0 # newton
uav_vertical_speed = 0 # m/s
uav_vertical_accel = 0 #newton

uav_accel = 0 
uav_speed = 0#m/s

uav_lift = 0
distance = 0

uav_trust = 0  # newton
uav_roll = 0 #degres
uav_yaw = 0 #degres
uav_pitch = 0 #degres

loc_lat = 0
loc_lon = 0
loc_alt = 0

# süre
simulasyon_suresi = 100

# saniye başı adım sayısı
t = 0
dt = 0.1
#endregion

def lift(speed):
    lift = (0.5 * CL * rho * S * (speed ** 2))
    return lift

def drag(speed,CD):
    drag = 0.5 * CD * rho * S * (speed ** 2)
    return drag

def update():
    global uav_trust

    uav_trust = input_trust.get()
    uav_input_roll = input_roll.get()
    uav_input_yaw = input_yaw.get()
    uav_input_pitch = input_pitch.get()
    #print(uav_input_trust,uav_input_roll,uav_input_yaw,uav_input_pitch)

    return [uav_trust,uav_input_roll,uav_input_pitch,uav_input_yaw]

def trust_calc(trust,pitch):
    thrust_horizontal = trust * math.cos(pitch)
    thrust_vertical = trust * math.cos(pitch)
    return [thrust_horizontal,thrust_vertical]

def model():
    global uav_roll, uav_pitch, uav_yaw, uav_horizontal_speed, uav_vertical_speed, uav_accel_horizontal, loc_alt, distance, t , uav_lift,uav_speed ,uav_accel ,uav_vertical_accel,loc_lat,loc_lon
    for t in range(int(simulasyon_suresi/dt)):
        # Update thrust
        inputs = update()

        uav_trust = inputs[0]
        uav_pitch = inputs[2]
        uav_yaw = inputs[3]

        forces = trust_calc(uav_trust,uav_pitch)

        # lift (0 derece)
        uav_lift = lift(uav_speed)

        #hız
        uav_accel = (uav_trust - drag(uav_horizontal_speed, CD_horizontal)) / (uav_weight/9.81)
        uav_speed += (uav_accel * dt)
        #distance = uav_accel_horizontal*dt

        #yatay hız
        uav_accel_horizontal = (forces[0] - drag(uav_horizontal_speed, CD_horizontal)) / (uav_weight/9.81)
        uav_horizontal_speed += (uav_accel_horizontal * dt)
        distance = uav_horizontal_speed*dt

        #dikey hız
        uav_vertical_accel = (uav_lift+forces[1] - (drag(uav_vertical_speed, CD_vertical)+uav_weight)) / (uav_weight/9.81)
        uav_vertical_speed += uav_vertical_accel * dt


        #attitude
        loc_alt += uav_vertical_speed * dt
        cords = translate_coordinates([40.799881,30.291096],uav_yaw,distance)
        loc_lat = cords[0]
        loc_lon = cords[1]

        #sinirlar
        if loc_alt < 0:
            loc_alt = 0
            uav_vertical_speed = 0

        # Sleep for a while to match the real-time speed
        time.sleep(dt)
        status()

def status():
    os.system("clear")
    # Print current state
    print("Time: ", t*dt)
    print("Thrust: ", uav_trust)
    print("Roll: ", uav_roll)
    print("Pitch: ", uav_pitch)
    print("Yaw: ", uav_yaw)
    print("Speed-vertical: ", uav_vertical_speed)
    print("accel-vertical: ", uav_vertical_accel)
    print("Speed-horizontal: ", uav_horizontal_speed)
    print("accel-horizontal: ", uav_accel_horizontal)
    print("Drag:-vertical ", drag(uav_vertical_speed,uav_vertical_speed))
    print("Drag:-horizontal ", drag(uav_horizontal_speed,uav_horizontal_speed))
    print("Lift: ", uav_lift)
    print("Position: Lat {}, Lon {}, Alt {}".format(loc_lat, loc_lon, loc_alt))
    print("------")
    print("mesafe: ",distance)#kordinat hesabı
    
def loop():
    model()
            
#region slider
input_trust = Scale(root, from_=0, to=30, length=200, orient=VERTICAL)
input_trust.place(x=25,y=50)

input_roll = Scale(root, from_=0, to=360, length=200, orient=VERTICAL)
input_roll.place(x=100,y=50)

input_yaw = Scale(root, from_=0, to=360, length=200, orient=VERTICAL)
input_yaw.place(x=175,y=50)

input_pitch = Scale(root, from_=-30, to=30, length=200, orient=VERTICAL)
input_pitch.place(x=250, y=50)

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


    