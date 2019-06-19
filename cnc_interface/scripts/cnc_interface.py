#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

from cnc_class import cnc

cnc_obj = cnc()

def cmdCallback(msg):

	rospy.loginfo(rospy.get_name() + ": " + str(msg))
	print msg.linear.x, msg.linear.y, msg.linear.z
	cnc_obj.moveTo(msg.linear.x, msg.linear.y, msg.linear.z, blockUntilComplete=True)

def stopCallback(msg):
		#stop steppers
	if   msg.data == 's':
		cnc_obj.disableSteppers()
		# fire steppers
	elif msg.data == 'f':
		cnc_obj.enableSteppers()

def main():

	''' create ROS topics '''
	pos_pub     = rospy.Publisher('/cnc_interface/position',  Twist, queue_size = 10)
	status_pub  = rospy.Publisher('/cnc_interface/status'  , String, queue_size = 10)
	rospy.Subscriber('cnc_interface/cmd' ,  Twist,  cmdCallback)
	rospy.Subscriber('cnc_interface/stop', String, stopCallback)

	rospy.init_node('cnc_interface', anonymous=True)

	port          = rospy.get_param('cnc_interface/port')
	baud          = rospy.get_param('cnc_interface/baudrate')
	acc           = rospy.get_param('cnc_interface/acceleration')  
	max_x 		  = rospy.get_param('cnc_interface/x_max')   
	max_y 		  = rospy.get_param('cnc_interface/y_max')   
	max_z 		  = rospy.get_param('cnc_interface/x_max')
	default_speed = rospy.get_param('cnc_interface/default_speed')   
	speed_x  	  = rospy.get_param('cnc_interface/x_max_speed')
	speed_y  	  = rospy.get_param('cnc_interface/y_max_speed')
	speed_z  	  = rospy.get_param('cnc_interface/z_max_speed')
	steps_x 	  = rospy.get_param('cnc_interface/x_steps_mm')
	steps_y 	  = rospy.get_param('cnc_interface/y_steps_mm')
	steps_z 	  = rospy.get_param('cnc_interface/z_steps_mm')

	cnc_obj.startup(port,baud,acc,max_x,max_y,max_z,default_speed,speed_x,speed_y,
					speed_z,steps_x,steps_y,steps_z)
	rate = rospy.Rate(10)

	while not rospy.is_shutdown():

		status     = cnc_obj.getStatus()
		cnc_pose   = cnc_obj.getTwist()
		ros_status = String(status)
		pos_pub.publish(cnc_pose)
		status_pub.publish(ros_status)
		rate.sleep()

	rospy.spin()

main()
