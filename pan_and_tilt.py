## Code to control the Robotis Turret
#fu
## Iteration 1
## Written by David McGuire & David Siegel for Atolla Tech
## June 2nd 2021


import os
import time

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



# Control table address
if MY_DXL == 'X_SERIES' or MY_DXL == 'MX_SERIES':
    ADDR_TORQUE_ENABLE          = 64
    ADDR_GOAL_POSITION          = 116    #refers to the microcontroller address, can be found in the DYNAMIXEL Wizard Software
    ADDR_PRESENT_POSITION       = 132
    STEP_TILT_VALUE             = 2030      #where our tilt motor begins
    DXL_MINIMUM_POSITION_VALUE  = 1536       # Refer to the Minimum Position Limit
    DXL_MAXIMUM_POSITION_VALUE  = 2595      # Refer to the Maximum Position Limit
    BAUDRATE                    = 1000000




elif MY_DXL == 'XL320':             #### doesnt apply to us either but I left it in for now due to an elif statement later
    ADDR_TORQUE_ENABLE          = 24
    ADDR_GOAL_POSITION          = 30
    ADDR_PRESENT_POSITION       = 37
    DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the CW Angle Limit of product eManual
    DXL_MAXIMUM_POSITION_VALUE  = 1023      # Refer to the CCW Angle Limit of product eManual
    BAUDRATE                    = 1000000   # Default Baudrate of XL-320 is 1Mbps

# DYNAMIXEL Protocol Version (1.0 / 2.0)
# https://emanual.robotis.com/docs/en/dxl/protocol2/
PROTOCOL_VERSION            = 2.0

# Factory default ID of all DYNAMIXEL is 1     #DXL_ID = 1 (1 refers to Motor ID 1 which is the pan)
DXL_ID                      = 1                 #DXL_ID = 1 (2 & 3 refer to Motor ID 2 & 3 which is the tilt motors)


# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
DEVICENAME                  = 'COM7'

TORQUE_ENABLE               = 1     # Value for enabling the torque
TORQUE_DISABLE              = 0     # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 3    # Dynamixel moving status threshold

index = 0
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE,STEP_TILT_VALUE, DXL_MAXIMUM_POSITION_VALUE, STEP_TILT_VALUE]         # Goal position


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
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
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
    print("Dynamixel has been successfully connected")

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 2, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully connected")

while 1:

    #print("Press any key to continue! (or press ESC to quit!)")
    #if getch() == chr(0x1b):
    #    break
    if STEP_TILT_VALUE > 2200:     #When should the tilt motor end     - tilt goes from 101 degrees to 255 degrees... 101 = 1151, 255 = 2887
        #print("STEP TILT VALUE HAS REACHED:%03d Press any key to reset! (or press ESC to quit!)" % (STEP_TILT_VALUE))
        STEP_TILT_VALUE = 2030      #where our tilt motor resets




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
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID, dxl_goal_position[index], dxl_present_position))

        if not abs(dxl_goal_position[index] - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
            break

    # Change goal position   ; This code loops the turret back and forth
    if index == 0:
        index = 1
        STEP_TILT_VALUE = STEP_TILT_VALUE + 10 #This increases the tilt by approximately one degree
        #print("[DXL GOAL POSITION:%03d] GoalPos:%03d  PresPos:%03d" % (dxl_goal_position[], dxl_goal_position[index], dxl_present_position))
        dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE,STEP_TILT_VALUE, DXL_MAXIMUM_POSITION_VALUE, STEP_TILT_VALUE]         # Goal position
        print(dxl_goal_position)
        DXL_ID = 2
    elif index == 1:
        index = 2
        DXL_ID = 1
    elif index == 2:
        index = 3
        STEP_TILT_VALUE = STEP_TILT_VALUE + 10
        dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE,STEP_TILT_VALUE, DXL_MAXIMUM_POSITION_VALUE, STEP_TILT_VALUE]         # Goal position
        DXL_ID = 2
    elif index == 3:
        index = 0
        DXL_ID = 1



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
