import dronekit
import dronekit_sitl
import time
from arm_and_takeoff import arm_and_takeoff

altitude = 20

# The below code starts the SITL simulation of a copter.
sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()

# Connect to the Vehicle using dronekit.
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = dronekit.connect(connection_string, wait_ready=True)

# Arms the vehicle and takes of the specified altitude.
arm_and_takeoff(altitude, vehicle)

# Section for entering commands for test run. 
# ----------------------------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------------------------

print "Returning to Launch"
vehicle.mode = dronekit.VehicleMode("RTL")

# Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()