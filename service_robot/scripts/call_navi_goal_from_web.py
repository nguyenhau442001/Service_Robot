#!/usr/bin/env python
from ast import Index
from operator import index
import rospy
import subprocess
from std_msgs.msg import String,Int32

int ;index=0

# Home(2,2),table 1(4,2),table 2(8,3),table3(5,6),table4(5,15),table5(9,18)
def callback(data):
    index=data.data
    
    rospy.loginfo( "Moving table %s", index)
    if(index=="Table 1"):
        subprocess.Popen('roslaunch navi_goals navi_goals.launch',shell=True) 
    if(index=="Table 2"):
        subprocess.Popen('roslaunch navi_goals_2 navi_goals.launch',shell=True) 
    if(index=="Table 3"):
        subprocess.Popen('roslaunch navi_goals_3 navi_goals.launch',shell=True) 
    if(index=="Table 4"):
        subprocess.Popen('roslaunch navi_goals_4 navi_goals.launch',shell=True) 
    if(index=="Table 5"):
        subprocess.Popen('roslaunch navi_goals_5 navi_goals.launch',shell=True) 


    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
def listener():

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("Moving_to_table", String, callback)
    
      
        
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
    # listener()
if __name__ == '__main__':
    
    listener()  
   
        

# Call navi_goals package

