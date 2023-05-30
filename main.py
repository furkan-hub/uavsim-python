import time
import os
import threading
from tkinter import *


# Constants
CL = 0.320
CD_horizontal = 0.013
CD_vertical = 0.300

rho = 1.225 # rooo
S = 0.180 # m^2

# Initial values
uav_trust = 0 # newton
uav_weight = 35 # Newton
uav_horizontal_speed = 0 # m/s
uav_veritcal_speed = 0
uav_climb_accel = 0 #newton
uav_accel = 0 # newton

uav_roll = 0 #degres
uav_yaw = 0 #degres
uav_pitch = 0 #degres

MAX_SPEED = 50

loc_lat = 0
loc_lon = 0
loc_alt = 0

#pwm
chanel_trust = 37
chanel_roll = 0 
chanel_pitch = 0
chanel_yaw = 0

# Simulation duration in seconds
simulasyon_suresi = 100

# Simulation step in seconds
dt = 0.1

# Calculate lift and drag


def lift(speed):
    return 0.5 * CL * rho * S * (speed ** 2)


def drag(speed,CD):
    return 0.5 * CD * rho * S * (speed ** 2)


# Simulation loop
for t in range(int(simulasyon_suresi/dt)):
    # Update thrust

    uav_trust = chanel_trust


    # Calculate acceleration, velocity, lift
    uav_lift = lift(uav_horizontal_speed)


    uav_accel = (uav_trust - drag(uav_horizontal_speed,CD_horizontal)) / (uav_weight/9.81)
    uav_horizontal_speed += (uav_accel * dt)

    uav_veritcal_speed += uav_climb_accel *dt
    uav_climb_accel = ((uav_lift-uav_weight-drag(uav_veritcal_speed,CD_vertical))) / (uav_weight/9.81)

    uav_horizontal_speed = max(min(uav_horizontal_speed, MAX_SPEED), -MAX_SPEED)
    uav_veritcal_speed = max(min(uav_veritcal_speed, MAX_SPEED), -MAX_SPEED)

    # Print current state
    print("Time: ", t*dt)
    # Update roll, pitch, yaw based on current channel inputs
    # NOTE: Here, we might assume the channel inputs directly correspond to the roll, pitch and yaw rates
    uav_roll_rate = chanel_roll
    uav_pitch_rate = chanel_pitch
    uav_yaw_rate = chanel_yaw

    # Based on the above assumption, update roll, pitch, yaw
    uav_roll += uav_roll_rate * dt
    uav_pitch += uav_pitch_rate * dt
    uav_yaw += uav_yaw_rate * dt

    loc_alt += uav_veritcal_speed * dt

    if loc_alt < 0:
        loc_alt = 0

    os.system("cls")

    # Print current state
    print("Time: ", t*dt)
    print("Thrust: ", uav_trust)
    print("Roll: ", uav_roll)
    print("Pitch: ", uav_pitch)
    print("Yaw: ", uav_yaw)
    print("Speed-veritcal: ", uav_veritcal_speed)
    print("Speed-horizontal: ", uav_horizontal_speed)
    # print("Drag:-vertical ", drag(uav_veritcal_speed,uav_veritcal_speed))
    # print("Drag:-horizontal ", drag(uav_horizontal_speed,uav_horizontal_speed))
    print("Lift: ", lift(uav_horizontal_speed))
    print("Position: Lat {}, Lon {}, Alt {}".format(loc_lat, loc_lon, loc_alt))
    print("------")

    # Sleep for a while to match the real-time speed
    time.sleep(dt)
