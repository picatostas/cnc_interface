# cnc_interface
ROS node to interface cnc machines using GRBL as GCODE interpreter.

Author : Pablo Costas Franco

This project is based on https://github.com/openautomation/ROS-GRBL

## Topics 

### Publishing
Change the Rospy Rate to change the publishing rate
- /cnc_interface/position (Twist)
          Publish actual position of the machine 
- /cnc_interface/status (String)
          Dumps GRBL status message

### Suscribing
- /cnc_interface/cmd (Twist)
          XYZ absolute coordinates in ROS Msg format Twist
- /cnc_interface/stop (String) 
          's' To stop the stepper motors
          'f' to reenable stepper motors

## Running the node

In `/cnc_interface/launch` you will have to place a launch file describing you machine for the node to config properly the parameters.
An example has been included for interfacing a Shapeoko cnc controlled by a Smoothieboard.
Note that for operating the serial port, first you will have to locate the serial port under `/dev/tty*`. Before running the node, 
the user has to be granted with permissions to operate the port. ` sudo chmod 0777 /dev/tty<whatever>` 

Once cloned, grant check that the file cnc_interace.py in `scripts` has excute permisions, otherwise set them with `chmod +x scripts/cnc_interface.py` or the node wont launch.

Once the node is launched the machine will start the homing procedure, so keep in mind.
