import Command_API
from arm_and_takeoff import arm_and_takeoff
import dronekit_sitl
import dronekit
import serial

class Receiver_API(object):
    __OUTPUT_PINS = -1

    sitl = 0
    connection_string = 0
    vehicle = 0

    def __init__(self, port, baudrate=9600):
        self.serial = serial.Serial(port, baudrate, timeout=1)

        # The below code starts the SITL simulation of a copter.
        self.sitl = dronekit_sitl.start_default()
        self.connection_string = self.sitl.connection_string()

        # Connect to the Vehicle using dronekit.
        print("Connecting to vehicle on: %s" % (self.connection_string,))
        self.vehicle = dronekit.connect(self.connection_string, wait_ready=True)

    # ------------------------------------------------------------------------------------------------------------------
    # This method is for checking if the sender side of the API has sent anything over to the receiver side. Executes
    # commands given based on the serial data received.
    # ------------------------------------------------------------------------------------------------------------------
    def check_commands(self):
        serial_info = self.getData()

        if serial_info == '':
            return False
        elif serial_info == '1':
            return self.vehicle_arm_and_takeoff()
        elif serial_info == '2':
            return self.vehicle_condition_yaw()
        elif serial_info == '3':
            return self.vehicle_get_location_metres()
        elif serial_info == '4':
            return self.vehicle_goto_position_target_local_ned()

    # ------------------------------------------------------------------------------------------------------------------
    # Response the the arm and takeoff command from the sender side.
    # Before arming and having the drone takeoff, this method asks for the altitude from the sender.
    # ------------------------------------------------------------------------------------------------------------------
    def vehicle_arm_and_takeoff(self):

        data_wait = True

        self.__sendData('altitude')

        while data_wait:
            serial_ack = self.getData()
            if serial_ack != '':
                arm_and_takeoff(float(serial_ack), self.vehicle)
                return self.__sendData(serial_ack)

    # ------------------------------------------------------------------------------------------------------------------
    # Send MAV_CMD_CONDITION_YAW message to point vehicle at a specified heading (in degrees).
    #
    # This method sets an absolute heading by default, but you can set the `relative` parameter
    # to `True` to set yaw relative to the current yaw heading.
    #
    # By default the yaw of the vehicle will follow the direction of travel. After setting
    # the yaw using this function there is no way to return to the default yaw "follow direction
    # of travel" behaviour (https://github.com/diydrones/ardupilot/issues/2427)
    # ------------------------------------------------------------------------------------------------------------------
    def vehicle_condition_yaw(self):

        data_wait = True
        heading = ''
        relative_str = ''

        self.__sendData('heading')

        while data_wait:
            serial_ack = self.getData()
            if serial_ack != '':
                data_wait = False
                heading = serial_ack

        data_wait = True
        self.__sendData('relative_str')

        while data_wait:
            serial_ack = self.getData()
            if serial_ack != '':
                relative_str = serial_ack
                Command_API.condition_yaw(self.vehicle, heading, relative_str)
                return self.__sendData('done')


    # ------------------------------------------------------------------------------------------------------------------
    # Send MAV_CMD_DO_SET_ROI message to point camera gimbal at a
    # specified region of interest (LocationGlobal).
    # The vehicle may also turn to face the ROI.
    #
    # For more information see:
    # http://copter.ardupilot.com/common-mavlink-mission-command-messages-mav_cmd/#mav_cmd_do_set_roi
    # ------------------------------------------------------------------------------------------------------------------
    def vehicle_get_location_metres(self):

        original_location, dNorth, dEast = ''

        data_wait = True

        self.__sendData('original_location')

        while data_wait:
            serial_ack = self.getData()
            if serial_ack != '':
                data_wait = False
                original_location = serial_ack

        data_wait = True

        self.__sendData('dNorth')

        while data_wait:
            serial_ack = self.getData()
            if serial_ack != '':
                data_wait = False
                dNorth = serial_ack

        data_wait = True

        self.__sendData('dEast')

        while data_wait:
            serial_ack = self.getData()
            if serial_ack != '':
                data_wait = False
                dEast = serial_ack
                return str(Command_API.get_location_metres(original_location, float(dNorth), float(dEast)))

    # ------------------------------------------------------------------------------------------------------------------
    # Method for telling the drone where to go.
    # ------------------------------------------------------------------------------------------------------------------
    def vehicle_goto_position_target_local_ned(self):

        north, east, down = 0

        data_wait = True

        while data_wait:
            serial_ack = self.getData()
            if serial_ack != '':
                data_wait = False
                north = float(serial_ack)

        data_wait = True

        while data_wait:
            serial_ack = self.getData()
            if serial_ack != '':
                data_wait = False
                east = float(serial_ack)

        data_wait = True

        while data_wait:
            serial_ack = self.getData()
            if serial_ack != '':
                data_wait = False
                down = float(serial_ack)
                Command_API.goto_position_target_local_ned(self.vehicle, north, east, down)
                return self.__sendData('done')

    # ------------------------------------------------------------------------------------------------------------------
    # Method for receiving data from counter part of telemetry set. Returns '' if there is nothing in the received
    # buffer. Reads a single line and returns that line.
    # ------------------------------------------------------------------------------------------------------------------
    def getData(self):
        line = ''
        try:
            line = self.serial.readline().replace("\r\n", "")
        except Exception, e:
            return ''
        if line:
            return line
        else:
            return ''

    # ------------------------------------------------------------------------------------------------------------------
    # Method for sending data from counter part of telemetry set. Sends a single line in string format. Returns True if
    # sending the data was successful and False if sending the data was unsuccessful.
    # ------------------------------------------------------------------------------------------------------------------
    def __sendData(self, serial_data):
        if self.serial.write(str(serial_data)) == 1:
            return True
        else:
            return False

if __name__ == "__main__":

    # Initiating the receiver.
    receiver = Receiver_API('COM3')

    while True:
        receiver.check_commands()

