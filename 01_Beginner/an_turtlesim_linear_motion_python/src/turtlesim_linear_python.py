#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty

x = 0
y = 0
yaw = 0

def poseCallback(pose_message):
    global x
    global y, yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta


def move(speed, distance, is_forward):
    # declare a Twist message to send velocity commands
    velocity_message = Twist()

    # get current location
    global x, y
    x0 = x
    y0 = y

    if is_forward:
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message.linear.x = -abs(speed)

    distance_moved = 0.0
    loop_rate = rospy.Rate(10)  # publish message 10 times per seconds
    cmd_vel_topic = '/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size = 10)

    while True:
        rospy.loginfo("Turtlesim moves forwards")
        velocity_publisher.publish(velocity_message)

        loop_rate.sleep()

        # rospy.Duration(1.0)

        distance_moved = abs(0.5 * math.sqrt(((x-x0) ** 2) + ((y-y0) ** 2)))
        print distance_moved
        if not distance_moved < distance:
            rospy.loginfo("reached")
            break

    # finally, stop the robot when the distance is moved
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)






if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_motion_pose', anonymous = True)

        # declare velocity publisher
        cmd_vel_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size = 10)

        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)
        time.sleep(1)


        while True:
            # ini buat test si turtle maju
            move(2.0, 2.0, True)
            # ini buat test si turtle mundur
            move(2.0, 2.0, False)
            # ini buat test si turtle maju
            move(5.0, 1.0, True)
            # ini buat test si turtle mundur
            move(1.0, 3.0, False)
            # ini buat test si turtle maju
            move(5.0, 2.0, True)


        # rotate(90, 90, True)



    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated")
