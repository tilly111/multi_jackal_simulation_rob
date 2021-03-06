#!/usr/bin/env python

###Random exploration for jackal robot


#additional imports
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import random
import sys
import threading

class velo_publisher():
    def __init__(self, topic):
        rospy.init_node('avoid')
        self.pub = rospy.Publisher(topic, Twist, queue_size=10)
        self.vel_msg=Twist()
        self.vel_msg.linear.x = 0
        self.vel_msg.linear.y = 0
        self.vel_msg.linear.z = 0
        self.vel_msg.angular.x = 0
        self.vel_msg.angular.y = 0
        self.vel_msg.angular.z = 0
        self.reset_time=3.0

        # init the listener?
        print(ns+"/odom_ground_truth")
        self.sub = rospy.Subscriber(ns+"/odom_ground_truth", Odometry, self.listener_callback)

        self.timer1 = 0
        self.timer2 = 0

    def publish(self):
        # self.vel_msg.linear.x = random.random()
        # self.vel_msg.angular.z = random.uniform(-1, 1)
        self.pub.publish(self.vel_msg)

    def reset_var(self):
        #resets variables randomly after
        self.vel_msg.linear.x = 0.5 #random.random()
        self.vel_msg.angular.z = random.uniform(-1, 1)
        threading.Timer(self.reset_time, self.reset_var).start()


    def listener_callback(self, data):
        #print("callback worked irgendwie")
        #print(data.pose.pose)

        if (data.pose.pose.position.x > 5 or data.pose.pose.position.x < -5 or data.pose.pose.position.y > 5 \
                or data.pose.pose.position.y < -5) and self.timer1 == 0:
            print("found to wall")
            self.vel_msg.angular.z = 1
            self.vel_msg.linear.x = 0
            self.timer1 = random.randint(10, 40)
        elif not (self.timer1 == 0) and self.timer2 == 0: # dreht sich?
            print("turning")
            self.vel_msg.angular.z = 1
            self.vel_msg.linear.x = 0
            self.timer1 -= 1
            if self.timer1 == 1:
                self.timer2 = random.randint(10, 15)
        elif not self.timer2 == 0:
            print("drive back")
            self.vel_msg.angular.z = 0
            self.vel_msg.linear.x = 0.7
            self.timer2 -= 1
            if self.timer2 == 0:
                self.timer1 = 0
        else:
            print("normal drive")
            self.vel_msg.angular.z = 0
            self.vel_msg.linear.x = 0.7

        return

if __name__ == '__main__':
    try:
        ns=sys.argv[1]
        topic=ns+"/cmd_vel"  # topic /cmd_vel published direkt an die motoren; muss eine Twist msg sein -> zyklisch
        vp = velo_publisher(topic)
        #vp.reset_var()

        while True:
            vp.publish()
            rospy.sleep(0.2)
            #print("debug print ")

    except rospy.ROSInterruptException or KeyboardInterrupt: pass

