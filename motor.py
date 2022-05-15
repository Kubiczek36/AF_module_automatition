import serial
from time import sleep


class stage:
    """
    Class for controling of the SmarAct linear piezo stage.
    """

    def __init__(self, baudrate=115200, port="/dev/tty.usbserial-FTXJ1B5V"):
        self.port = port
        self.baudrate = baudrate

    def writeSerial(self, command):
        self.port.write((":" + command + "\n").encode("ascii"))

    def writeSerialAns(self, command):
        self.port.write((":" + command + "\n").encode("ascii"))
        ans = self.port.readline()
        print(ans)
        return ans

    def readSer(self):
        ans = self.port.readline()
        return(ans)

    def init(self, setzero=True, speed = 1):
        """ 
        `speed` - in mm/s
        """
        self.port = serial.Serial(port = "/dev/tty.usbserial-FTXJ1B5V",baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
        writeSerialAns("SCM0")  # set comunication mode
        anse = writeSerialAns("SSE1")  # set sensor enabled
        if anse != b":E-1,0\n":
            print("Sensor not enabled!")
            return
        writeSerialAns("SST0,1")  # se sensor type, one for our sensor
        writeSerialAns("CS0")  # Calibrate Sensor, zero - channel
        if setzero:
            writeSerialAns("MPR0,-16000000,0")
            sleep(2)
        speed  = 1e3  # convert to nm/s
        writeSerAns("SCLS0,1000000")
        anse = writeSerialAns("SSE2")  # set sensor enabled

    def moveRelative(self, distance):
        """
        `distance` - distance to be moved in um
        """
        distance = distance * 1e3  # convert to nm
        text = "MPR0,{:.0f},0".format(distance)
        writeSerialAns(text)

    def moveRelative(self, position):
        """
        `position` - position to be moved in um
        """
        position = position * 1e3  # convert to nm
        text = "MPR0,{:.0f},0".format(distance)
        writeSerialAns(text)

    def getPosition(self):
        """ 
        returns absolute position in um
        """
        writeSerial("GP0")
        pos = int(readSer())
        return(1000*pos)

    def getPosition_mm(self):
        """ 
        returns absolute position in mm
        """
        writeSerial("GP0")
        pos = int(readSer())
        return(1000000 * pos)

    def end(self):
        self.port.close()

