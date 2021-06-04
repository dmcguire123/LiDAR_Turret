## Code to control the Robotis Turret
##
## Written by David McGuire & David Siegel for Atolla Tech
## June 4th 2021


import os
import time
import keyboard
import sys

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import * # Uses Dynamixel SDK library



MY_DXL = 'X_SERIES'       # X330 (5.0 V recommended), X430, X540, 2X430

#print("\nWhen you're ready to quit, just hit ESC!...")

# Control table address
if MY_DXL == 'X_SERIES' or MY_DXL == 'MX_SERIES':
    ADDR_TORQUE_ENABLE          = 64
    ADDR_GOAL_POSITION          = 116    #refers to the microcontroller address, can be found in the DYNAMIXEL Wizard Software
    ADDR_PRESENT_POSITION       = 132
    DXL_RESET_VALUE             = 2048
    BAUDRATE                    = 1000000




elif MY_DXL == 'XL320':             #### doesnt apply to us either but I left it in for now due to an elif statement later
    ADDR_TORQUE_ENABLE          = 24


# DYNAMIXEL Protocol Version (1.0 / 2.0)
# https://emanual.robotis.com/docs/en/dxl/protocol2/
PROTOCOL_VERSION            = 2.0

# Factory default ID of all DYNAMIXEL is 1     #DXL_ID = 1 (1 refers to Motor ID 1 which is the pan)
x = int(input("\nEnter '1' to control Pan Motor or '2' to control the Tilt Motor:"))
DXL_ID                      = x                 #DXL_ID = 1 (2 & 3 refer to Motor ID 2 & 3 which is the tilt motors)


# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
#USB_PORT = input("\n\nPlease enter your serial Port.\n (Examples, Windows: COM*, Linux: /dev/ttyUSB*, Mac: /dev/tty.usbserial-*\nENTER HERE:")
# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
DEVICENAME                  = "COM7" #USB_PORT

#DXL_INPUT_POSITION = input("Please enter your desired degrees.\n \nENTER HERE:")  #Takes in a target angle i.e 180 degrees

#INPUT_POS = (float(DXL_INPUT_POSITION) * 11.3777777778)  #converts the target angle to a usuable number for dynamixel
#GOAL_POS = round(INPUT_POS) # converts to a whole number for dynamixel
#print(GOAL_POS)

TORQUE_ENABLE               = 1     # Value for enabling the torque
TORQUE_DISABLE              = 0     # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 5    # Dynamixel moving status threshold

index = 0
#dxl_goal_position = [GOAL_POS, DXL_RESET_VALUE]         # Goal position


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 1, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel Motor has been successfully connected")

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 2, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("\n")


    while 1:
        print("\nPress any key to change your desired angle! (or press ESC to quit!)")
        if getch() == chr(0x1b):
            break
        DXL_INPUT_POSITION = input("\n\nPlease enter your desired degrees(i.e '180' for 180 degrees).\nENTER HERE:")  #Takes in a target angle i.e 180 degrees

        INPUT_POS = (float(DXL_INPUT_POSITION) * 11.3777777778)  #converts the target angle to a usuable number for dynamixel
        GOAL_POS = round(INPUT_POS) # converts to a whole number for dynamixel
        dxl_goal_position = [GOAL_POS, DXL_RESET_VALUE]         # Goal position



        # Write goal position
        if (MY_DXL == 'XL320'): # XL320 uses 2 byte Position Data, Check the size of data in your DYNAMIXEL's control table
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, dxl_goal_position[index])
        else:
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, dxl_goal_position[index])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        while 1:
            # Read present position


            if (MY_DXL == 'XL320'): # XL320 uses 2 byte Position Data, Check the size of data in your DYNAMIXEL's control table
                dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
            else:
                dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
                if keyboard.is_pressed('Esc'):
                    print("\nYou pressed Esc, so exiting...")
                    sys.exit(0)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))

            #print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID, dxl_goal_position[index], dxl_present_position))

            if not abs(dxl_goal_position[index] - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
                break






# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 1, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 2, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()
