#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt

class TurtleBot:
 def __init__(self):
	 # Creating our node, publisher and subscriber
	 rospy.init_node('turtlebot_controller', anonymous=True)
	 self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
	 self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)
	 self.pose = Pose()
	 self.rate = rospy.Rate(10)
 def update_pose(self, data):
	 """Callback function which is called when a new message of type Pose is received by the subscriber"""
	 self.pose = data
	 self.pose.x = round(self.pose.x, 4)
	 self.pose.y = round(self.pose.y, 4)
 def euclidean_distance(self, goal_pose):
	 """Euclidean distance between current pose and the goal"""
	 return sqrt(pow((goal_pose.x - self.pose.x), 2) +
	 pow((goal_pose.y - self.pose.y), 2))
 def linear_vel_controller(self, goal_pose, k_p=1.5):
	 """Linear velocity P controller"""
	 return k_p * self.euclidean_distance(goal_pose)
 def steering_angle(self, goal_pose):
	 """Calculating steering angle"""
	 return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)
 def angular_vel_controller(self, goal_pose, k_p=6):
	 """Angular velocity P controller"""
	 return k_p * (self.steering_angle(goal_pose) - self.pose.theta)
 def move2goal(self):
	 """Moves the turtle to the goal."""
	 goal_pose = Pose()
	 # Get the input from the user.
	 goal_pose.x = float(input("Set your x goal: "))
	 goal_pose.y = float(input("Set your y goal: "))
	 distance_tolerance = 0.1
	 vel_msg = Twist()
	 while self.euclidean_distance(goal_pose) >= distance_tolerance:
		 # Porportional controller.
		 # https://en.wikipedia.org/wiki/Proportional_control
		 
		 # Linear velocity in the x-axis.
		 vel_msg.linear.x = self.linear_vel_controller(goal_pose)
		 vel_msg.linear.y = 0
		 vel_msg.linear.z = 0
		 
		 # Angular velocity in the z-axis.
		 vel_msg.angular.x = 0
		 vel_msg.angular.y = 0
		 vel_msg.angular.z = self.angular_vel_controller(goal_pose)
		 
		 # Publishing our vel_msg
		 self.velocity_publisher.publish(vel_msg)
		 
		 # Publish at the desired rate.
		 self.rate.sleep()
		 
		 # Stopping our turtle after the movement is over.
		 vel_msg.linear.x = 0
		 vel_msg.angular.z = 0
		 self.velocity_publisher.publish(vel_msg)
		 
if __name__ == '__main__':
 try:
	 x = TurtleBot()
	 x.move2goal()
 except rospy.ROSInterruptException:
 	pass

