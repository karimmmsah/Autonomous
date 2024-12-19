#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class WallFollower:
    def __init__(self):
        # Initialize the node
        rospy.init_node('wall_follower', anonymous=True)

        # Publisher to control the robot's velocity
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        # Subscriber to the LiDAR /scan topic
        self.sub = rospy.Subscriber("/scan", LaserScan, self.lidar_callback)

        # Initialize the movement command
        self.move_cmd = Twist()

        # Define parameters
        self.robot_width = 0.14  # Robot width (in meters, approx for TurtleBot3 Burger)
        self.buffer = self.robot_width / 2  # Add half-width as buffer
        self.min_distance_threshold = 0.3 + self.buffer  # Safe minimum distance
        self.max_distance_threshold = 1.0  # Maximum distance to avoid walls
        self.turn_speed = 0.8  # Angular speed for turning
        self.forward_speed = 0.2  # Linear speed for moving forward

    def lidar_callback(self, msg):
        # Process LiDAR scan data
        ranges = msg.ranges  # List of range readings from LiDAR

        # Get relevant sections of the scan
        front_ranges = ranges[0:10] + ranges[-10:]  # Front (10 degrees on each side)
        left_ranges = ranges[80:100]  # Left side
        right_ranges = ranges[260:280]  # Right side

        # Calculate minimum distances
        front_min = min(front_ranges)
        left_min = min(left_ranges)
        right_min = min(right_ranges)

        rospy.loginfo(f"Front: {front_min:.2f}, Left: {left_min:.2f}, Right: {right_min:.2f}")

        # Decision-making based on sensor data
        if front_min < self.min_distance_threshold:  # Obstacle directly ahead
            rospy.loginfo("Obstacle ahead! Choosing direction to turn...")
            self.move_cmd.linear.x = 0.0  # Stop moving forward
            if right_min > left_min:  # More space on the right
                rospy.loginfo("Turning right.")
                self.move_cmd.angular.z = -self.turn_speed
            else:  # More space on the left
                rospy.loginfo("Turning left.")
                self.move_cmd.angular.z = self.turn_speed
        elif front_min > self.max_distance_threshold:  # Path is clear ahead
            rospy.loginfo("Path is clear. Moving forward.")
            self.move_cmd.linear.x = self.forward_speed
            self.move_cmd.angular.z = 0.0  # Move straight
        else:  # Maintain a safe distance and follow the wall
            rospy.loginfo("Following the wall...")
            self.move_cmd.linear.x = self.forward_speed
            if left_min < right_min:  # Adjust toward the center of the lane
                self.move_cmd.angular.z = -0.1  # Slightly turn right
            else:
                self.move_cmd.angular.z = 0.1  # Slightly turn left

        # Publish the movement command
        self.pub.publish(self.move_cmd)

    def run(self):
        # Run the node and keep it alive
        rospy.spin()

if __name__ == '__main__':
    try:
        wall_follower = WallFollower()
        wall_follower.run()
    except rospy.ROSInterruptException:
        pass

