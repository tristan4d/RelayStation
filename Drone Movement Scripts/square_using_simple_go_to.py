import dronekit
import dronekit_sitl
import time
from arm_and_takeoff import arm_and_takeoff

# Altitude the drone will fly in a square at.
altitude = 20

x1 = -35.361354
x2 = -35.363244
y1 = 149.165218
y2 = 149.168801

# The four points of the square.
point1 = dronekit.LocationGlobalRelative(x1, y1, altitude)
point2 = dronekit.LocationGlobalRelative(x2, y1, altitude)
point3 = dronekit.LocationGlobalRelative(x2, y2, altitude)
point4 = dronekit.LocationGlobalRelative(x1, y2, altitude)

# The below code starts the SITL simulation of a copter.
sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()

# Connect to the Vehicle using dronekit.
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = dronekit.connect(connection_string, wait_ready=True)

# Arms the vehicle and takes of the specified altitude.
arm_and_takeoff(altitude, vehicle)

# Go to first point (x1, y1)
print "Going towards first point for 30 seconds (groundspeed set to 12 m/s) ..."
vehicle.simple_goto(point1, groundspeed=12)

# sleep so we can see the change in map
time.sleep(30)

# Go to second point (x2, y1)
print "Going towards second point for 30 seconds (groundspeed set to 10 m/s) ..."
vehicle.simple_goto(point2, groundspeed=10)

# sleep so we can see the change in map
time.sleep(30)

# Go to third point (x2, y2)
print "Going towards third point for 30 seconds (groundspeed set to 11 m/s) ..."
vehicle.simple_goto(point3, groundspeed=11)

# sleep so we can see the change in map
time.sleep(30)

# Go to fourth point (x1, y2)
print "Going towards fourth point for 30 seconds (groundspeed set to 11 m/s) ..."
vehicle.simple_goto(point4, groundspeed=11)

# sleep so we can see the change in map
time.sleep(30)

print "Returning to Launch"
vehicle.mode = dronekit.VehicleMode("RTL")

# Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()