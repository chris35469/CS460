#!/usr/bin/env python


import rospy
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan

class ForceMapper(): 
    def __init__(self):
        self.pub_obs = rospy.Publisher('obstacle', String, queue_size=10)
        self.obstacle = ""
        self.r = rospy.Rate(250) # 250hz
        self.thresh = 1
        self.sub = rospy.Subscriber('/scan', LaserScan, self.callBack)
        self.start()
       
    def forward(self):
        self.move_cmd.linear.x = self.linear_speed
        self.move_cmd.angular.z = 0

    def start(self):
        while not rospy.is_shutdown():
            self.pub_obs.publish(self.obstacle)
            self.r.sleep()

    def callBack(self, msg):
        size = len(msg.ranges)
        right = msg.ranges[0]
        front = msg.ranges[size/2]
        left = msg.ranges[size-1]

        print(right, front, left)

        if (front < self.thresh):
            self.obstacle = "front"
        elif (right < self.thresh):
            self.obstacle = "right"
        elif (left < self.thresh):
            self.obstacle = "left"
        else:
            self.obstacle = ""
        
def main():
    rospy.init_node('ForceMapper')
    try:
        force = ForceMapper()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()