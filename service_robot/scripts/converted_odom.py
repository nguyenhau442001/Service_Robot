#!/usr/bin/env python3

import rospy
import tf
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64

class OdometryConverter:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('odom_converter')

        # Subscribe to Odom topic
        rospy.Subscriber('odom', Odometry, self.odom_callback)

        # Publishers for roll, pitch, and yaw angles
        self.roll_pub = rospy.Publisher('/converted_odom/roll', Float64, queue_size=10)
        self.pitch_pub = rospy.Publisher('/converted_odom/pitch', Float64, queue_size=10)
        self.yaw_pub = rospy.Publisher('/converted_odom/yaw', Float64, queue_size=10)

        # Initialize tf listener
        self.listener = tf.TransformListener()

    def odom_callback(self, msg):
        # Extract the Quaternion from the message
        q = [msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w]

        # Convert Quaternion to roll-pitch-yaw angles
        rpy = tf.transformations.euler_from_quaternion(q)

        # Convert roll-pitch-yaw angles to degrees
        roll = rpy[0] * 180.0 / 3.14159265359
        pitch = rpy[1] * 180.0 / 3.14159265359
        yaw = rpy[2] * 180.0 / 3.14159265359

        # Publish roll, pitch, and yaw angles
        self.roll_pub.publish(roll)
        self.pitch_pub.publish(pitch)
        self.yaw_pub.publish(yaw)

    def run(self):
        # Spin ROS node
        rospy.spin()

if __name__ == '__main__':
    odom_converter = OdometryConverter()
    odom_converter.run()
