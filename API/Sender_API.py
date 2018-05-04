import serial, time

class Sender_API(object):
    __OUTPUT_PINS = -1

    def __init__(self, port, baudrate=9600):
        self.serial = serial.Serial(port, baudrate, timeout=1)

    def __str__(self):
        return "Arduino is on port %s at %d baudrate" % (self.serial.port, self.serial.baudrate)

    # ------------------------------------------------------------------------------------------------------------------
    # This method has str altitude as an input. Arms and causes the drone to takeoff to the specified altitude.
    # ------------------------------------------------------------------------------------------------------------------
    def arm_and_takeoff(self, altitude):

        data_wait = True

        self.__sendData('1')

        while data_wait:
            serial_ack = self.__getData()
            if serial_ack == 'altitude':
                data_wait = False
                self.__sendData(altitude)

        data_wait = True

        while data_wait:
            serial_ack = self.__getData()
            print (serial_ack)
            if (serial_ack == altitude):
                print ('Drone has reached requested altitude: ' + altitude)
                return True


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
    def condition_yaw(self, heading, relative=False):

        data_wait = True
        # The name of the vehicle will be sent.
        # Heading is input in the format of a string.
        if ~relative:
            relative_str = 'F'
        else:
            relative_str = 'T'
            self.__sendData('2')

        while data_wait:
            serial_ack = self.__getData()
            if serial_ack == 'heading':
                data_wait = False
                self.__sendData(heading)

        data_wait = True

        while data_wait:
            serial_ack = self.__getData()
            if serial_ack == 'relative_str':
                data_wait = False
                self.__sendData(relative_str)

        data_wait = True

        while data_wait:
            serial_ack = self.__getData()
            if serial_ack == 'done':
                return True

    # ------------------------------------------------------------------------------------------------------------------
    # Send MAV_CMD_DO_SET_ROI message to point camera gimbal at a
    # specified region of interest (LocationGlobal).
    # The vehicle may also turn to face the ROI.
    #
    # For more information see:
    # http://copter.ardupilot.com/common-mavlink-mission-command-messages-mav_cmd/#mav_cmd_do_set_roi
    # ------------------------------------------------------------------------------------------------------------------
    def get_location_metres(self, original_location, dNorth, dEast):
        self.__sendData('3')

        data_wait = True

        while data_wait:
            serial_ack = self.__getData()
            if serial_ack == 'original_location':
                data_wait = False
                self.__sendData(original_location)

        data_wait = True

        while data_wait:
            serial_ack = self.__getData()
            if serial_ack == 'dNorth':
                data_wait = False
                self.__sendData(dNorth)

        data_wait = True

        while data_wait:
            serial_ack = self.__getData()
            if serial_ack == 'dEast':
                data_wait = False
                self.__sendData(dEast)

        data_wait = True

        while data_wait:
            serial_ack = self.__getData()
            if serial_ack != '':
                return serial_ack

    # ------------------------------------------------------------------------------------------------------------------
    # Method for telling the drone where to go.
    # ------------------------------------------------------------------------------------------------------------------
    def goto_position_target_local_ned(self, north, east, down):
        self.__sendData('4')

        data_wait = True

        while data_wait:
            serial_ack = self.__getData()
            if serial_ack == 'north':
                data_wait = False
                self.__sendData(north)

        data_wait = True

        while data_wait:
            serial_ack = self.__getData()
            if serial_ack == 'east':
                data_wait = False
                self.__sendData(east)

        data_wait = True

        while data_wait:
            serial_ack = self.__getData()
            if serial_ack == 'down':
                data_wait = False
                self.__sendData(down)

        data_wait = True

        while data_wait:
            serial_ack = self.__getData()
            if serial_ack == 'done':
                print('Drone has move to position:\n North: ' + north + '\nEast: ' + east + '\Down: ' + down)
                return True


    # ------------------------------------------------------------------------------------------------------------------
    # Method for sending data from counter part of telemetry set. Sends a single line in string format. Returns True if
    # sending the data was successful and False if sending the data was unsuccessful.
    # ------------------------------------------------------------------------------------------------------------------
    def __sendData(self, serial_data):
        if self.serial.write(str(serial_data)) == 1:
            return True
        else:
            return False

    # ------------------------------------------------------------------------------------------------------------------
    # Method for receiving data from counter part of telemetry set. Returns '' if there is nothing in the received
    # buffer. Reads a single line and returns that line.
    # ------------------------------------------------------------------------------------------------------------------
    def __getData(self):
        line = ''
        try:
            line = self.serial.readline().replace("\r\n", "")
        except Exception, e:
            return ''
        if line:
            return line
        else:
            return ''

    def status(self):
        return self.serial.isOpen()

    def close(self):
        self.serial.close()
        return True


