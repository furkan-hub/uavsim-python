import time
import os

# Constants
CL = 0.440
CD = 0.009
ro = 1.225
S = 0.180

# Initial values
uav_trust = 0
uav_weight = 0
uav_speed = 0
chanel_trust = 37
uav_roll = 0
uav_yaw= 0
uav_pitch = 0
loc_lat= 0
loc_lon = 0
loc_alt = 0

chanel_roll = 0
chanel_pitch = 0
chanel_yaw = 0

# Simulation duration in seconds
simulasyon_suresi = 100

# Simulation step in seconds
dt = 0.1

# Calculate lift and drag
def lift(speed):
    return 0.5 * CL * ro * S * (speed ** 2)

def drag(speed):
    return 0.5 * CD * ro * S * (speed ** 2)

# Simulation loop
for t in range(int(simulasyon_suresi/dt)):
    # Update thrust
    # if chanel_trust > 0:
    #     uav_trust += chanel_trust
    # else:
    #     uav_trust = 0
    uav_trust = chanel_trust
    # Calculate acceleration, velocity, lift
    uav_accel = (uav_trust - drag(uav_speed)) / uav_weight
    uav_speed += uav_accel * dt
    uav_lift = lift(uav_speed)

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

    # Update the position of the UAV based on its current speed and direction (which is determined by roll, pitch and yaw)
    # NOTE: In reality, the relationship between roll, pitch, yaw and the direction of motion is more complex and depends on the specific aerodynamics and control systems of the UAV.
    # However, for this simple simulation, we can assume that the UAV moves in the direction of its roll (x-direction), pitch (y-direction) and yaw (z-direction).

    loc_lat += uav_speed * dt * uav_roll
    loc_lon += uav_speed * dt * uav_pitch
    loc_alt += uav_speed * dt * uav_yaw

    os.system("cls")

    # Print current state
    print("Time: ", t*dt)
    print("Thrust: ", uav_trust)
    print("Roll: ", uav_roll)
    print("Pitch: ", uav_pitch)
    print("Yaw: ", uav_yaw)
    print("Speed: ", uav_speed)
    print("Drag: ", drag(uav_speed))
    print("Lift: ", lift(uav_speed))
    print("Position: Lat {}, Lon {}, Alt {}".format(loc_lat, loc_lon, loc_alt))
    print("------")


    # Sleep for a while to match the real-time speed
    time.sleep(dt)
