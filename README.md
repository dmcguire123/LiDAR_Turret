# LiDAR_Turret - Automatic Pan & Tilt

Python Code for our LiDAR Turret, Version 1.

The above code is a Python script that enables us to control our LiDAR Turret. 
In its current form,  when you begin the Python Script the turret will automatically reset its position to begin at the MINIMUM POSITION VALUE. This is a number between 0-4095 that correpesonds to the motor position. For reference, for the Tilt Motors (DXL_ID = 2 , 3), if we want the motor at 180 degrees, parrallel to the floor, the position value corresponds to 2030. These numbers can be clarified with the Dynamixel Wizard 2.0 software.
From here the microcontroller will add values to its PRESENT POSITION until it reaches its GOAL POSITION. The default goal position at the begining is the MAXIMMUM POSITION VALUE.
When the motor finshes panning from left to right, from MINIMUM POSITION TO MAXIMUM POSITION, it will tilt apprx 1 degree upwards. Then it will set the new GOAL POSITION as the original MINIMUM POSITION and reverse sweep.
This process continues until the tilt motors reach a pretermined angle, established in the code.

All of the above POSITIONS are established in the code before running the Python Script. More detail for what values must be changed are available in the comments of the code itself.


