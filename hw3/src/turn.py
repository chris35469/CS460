#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class Turn(): 
    def __init__(self):
        self.cmd_pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=1)
        self.r = rospy.Rate(250) # 250hz
        self.move_cmd = Twist()
        self.angular_speed = 0.8
        self.isTurning = "False"
        self.pub_turning = rospy.Publisher('/turning', String, queue_size=1)
        self.sub = rospy.Subscriber('/obstacle', String, self.callBack)
        self.start()
        
    def turn(self, factor):
        self.move_cmd.linear.x = 0
        self.move_cmd.angular.z = self.angular_speed * factor
        self.isTurning = "True"

    def stopTurning(self):
        self.move_cmd.linear.x = 0
        self.move_cmd.angular.z = 0
        self.isTurning = "False"

    def start(self):
        while not rospy.is_shutdown():
            self.pub_turning.publish(self.isTurning)
            self.cmd_pub.publish(self.move_cmd)
            self.r.sleep()

    def callBack(self, msg):
        if (msg.data == "front"):
            self.turn(1)
        elif (msg.data == "left"):
            self.turn(1)
        elif (msg.data == "right"):
            pass
        else:
            self.stopTurning()
        
def main():
    rospy.init_node('Turn')
    try:
        Turn()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()