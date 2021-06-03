# LiDAR_Turret - Automatic Pan & Tilt

Python Code for our LiDAR Turret, Version 1.

The above code is a Python script that enables us to control our LiDAR Turret. 
In its current form,  when you begin the Python Script the turret will automatically reset its position to begin at the MINIMUM POSITION VALUE. This is a number between 0-4095 that correpesonds to the motor position. For reference, for the Tilt Motors (DXL_ID = 1 , 2), if we want the motor at 180 degrees, parrallell to the floor, the position value corresponds to 2030. 
From here it will add values to its PRESENT POSITION until it reaches its GOAL POSITION. The default goal position at the begining is the MAXIMMUM POSITION VALUE
For this script, any positional changes to our motor must be made in the code before the script is started. More detail for what values must be changed are available in the comments of the code itself.



It consists of three Dynamixel motors. 

