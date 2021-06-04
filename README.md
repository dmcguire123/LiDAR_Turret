# LiDAR_Turret - Automatic Pan & Tilt

Python Code for our LiDAR Turret, Version 1.


#Pan_and_tilt  
This code is our primary Python script that enables us to scan with our LiDAR Turret. 
In its current form,  when you begin the Python Script the turret will automatically reset its position to begin at the MINIMUM POSITION VALUE. This is a number between 0-4095 that correpesonds to the motor position. For reference, for the Tilt Motors (DXL_ID = 2 , 3), if we want the motor at 180 degrees, parrallel to the floor, the position value corresponds to 2030. These numbers can be clarified with the Dynamixel Wizard 2.0 software.
From here the microcontroller will add values to its PRESENT POSITION until it reaches its GOAL POSITION. The default goal position at the begining is the MAXIMMUM POSITION VALUE.
When the motor finshes panning from left to right, from MINIMUM POSITION TO MAXIMUM POSITION, it will tilt apprx 1 degree upwards. Then it will set the new GOAL POSITION as the original MINIMUM POSITION and reverse sweep.
This process continues until the tilt motors reach a pretermined angle, established in the code.

All of the above POSITIONS are established in the code before running the Python Script. More detail for what values must be changed are available in the comments of the code itself.

Other elements that need to be altered in the code beforehand are the serial USB Port. (For example Windows uses COM7 or something close to it)


#Simple_input
This code is used to set the turret to aim at a particular angle.
Much of the code is similar to the above Pan_and_tilt script.
Key difference is that when started it will ask for an angle and then proceed to aim the turret at that angle. 


#Angle Cheat Sheet Uploaded Below:
![Turret Angles_210604_161137](https://user-images.githubusercontent.com/24493952/120858189-72434980-c550-11eb-9f3b-666824c16153.jpg)

![Turret Angles_SideView](https://user-images.githubusercontent.com/24493952/120858223-7ec7a200-c550-11eb-8aca-8b90030b06cd.jpg)




