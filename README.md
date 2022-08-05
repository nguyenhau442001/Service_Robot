# SERVICE ROBOT
I have consulted the documentation as below:

    1.https://github.com/devanshdhrafani/diff_drive_bot?fbclid=IwAR13gKv9AT9qRRjoVsUqTYrhSJN_SqjqlOUT3N7VGfB8ZDaehv2m5LRvvdI

    2.https://devanshdhrafani.github.io/blog/2020/11/01/diffdrive.html?fbclid=IwAR2rnmI8jEJEn0mfh6qbEmEooA_AI3zIyLfcTQ-vht6G5wXuQnkvXc8n0ow

Link youtube: 
1.  https://www.youtube.com/watch?v=k0roG6xbp_c&t=11s.


This ROS package implements SLAM on a 2 wheeled differential drive robot to map an unknown environment. A keyboard is used to teleoperate the robot in Gazebo. The map generated is then used for autonomous navigation using the ROS Navigation stack.
# Installation
1. Build package from source: navigate to the source folder of your catkin workspace and build this package using:

    $ git clone https://github.com/nguyenhau442001/Service_Robot.git
  
    $ cd ..
  
    $ catkin_make
2. Install Required dependencies:

    $ sudo apt-get install ros-noetic-dwa-local-planner.
    
If you missing any dependencies packages, please install them before go move on to the next step.

# URDF 
![image](https://user-images.githubusercontent.com/105471622/174599261-1599c94a-85e2-402d-a6ea-d82d54f4b950.png)

As we can see, this is my URDF. I exported from Solidworks. Basically, my URDF have 4 links such as base_link,left and right wheel link, and finally lidar link.

# GAZEBO 

![image](https://user-images.githubusercontent.com/105471622/174600486-9ba8c109-3487-466f-9884-f65708d84ead.png)

This is my robot when its standing in simulation environment GAZEBO.
# Simultaneous Localization And Mapping (SLAM)
![image](https://user-images.githubusercontent.com/105471622/174599138-efb09998-0637-49de-9da0-44b7cafb0878.png)

1. Load the robot in the Gazebo environment. I have changed it into environment I was created. You can change this from /worlds/mybot.world. To continue with default model:

    $ roslaunch service_robot gazebo.launch 
    
2. Launch the slam_gmapping node. This will also start rviz where you can visualize the map being created:

    $ roslaunch service_robot gmapping.launch

3. Move the robot around.

    $ rosrun service_robot keyboard_teleop.py 
    
4. Move the robot in your environment till a satisfactory map is created.
5. Save the map using:

    $ rosrun map_server map_saver -f ~/test_map

6. Copy the map file to ~/service_robot/maps/ directory and edit the .yaml file to match the path.

# Autonomous Navigation

This package uses the ROS Navigation stack to autonomously navigate through the map created using gmapping.

![image](https://user-images.githubusercontent.com/105471622/174601800-987012f9-f351-48b5-bbe9-cf92e9dda079.png)
![image](https://user-images.githubusercontent.com/105471622/174601834-11baf5ab-be07-4819-9f0b-124b17ad9798.png)
![image](https://user-images.githubusercontent.com/105471622/174601876-da303555-e9c5-422f-a7cf-7c94c22f616d.png)
![image](https://user-images.githubusercontent.com/105471622/174601905-524b1f2a-7884-48b1-a439-90a001478b1f.png)
![image](https://user-images.githubusercontent.com/105471622/174601936-592130d1-fc7c-484d-9b26-2ef86855fe07.png)
![image](https://user-images.githubusercontent.com/105471622/174601994-d28a6af9-8163-4419-8739-34981db6dccf.png)
![image](https://user-images.githubusercontent.com/105471622/174602019-5893d770-0756-439c-ab51-8da87738d705.png)

Another scenario 

![image](https://user-images.githubusercontent.com/105471622/174602677-7e549336-5f48-4194-ae6c-fee7f35aeb5f.png)
![image](https://user-images.githubusercontent.com/105471622/174602699-9895bc80-04cc-4421-bfcd-231716604422.png)
![image](https://user-images.githubusercontent.com/105471622/174602736-d7cede45-6512-4385-b37a-596598c1d45f.png)

1. To use your generated map, edit /launch/amcl_move_base.launch and add map .yaml location and name to map_server node launch.
2. Load the robot in gazebo environment:

    $ roslaunch service_robot gazebo.launch 
3. Start the amcl, move_base and rviz nodes:
 
    $ roslaunch service_robot amcl_move_base.launch

4. In rviz, click on 2D Pose Estimate and set initial pose estimate of the robot.

5. To move to a goal, click on 2D Nav Goal to set your goal location and pose.

# USER INTERFACE (WEB BROWSER)
Purpose: To control robot via web browser (Using rosbridge_server package - this package helps frontend developer build a web interface to visualize or interact with ROS Server.  
Requires components:
1. roslib,ros2djs,ros3djs,rosbridge_server (use Websocket)
2. Basic knowledge HTML,CSS,JS and ROS .

The key idea 
![image](https://user-images.githubusercontent.com/105471622/183107579-b43582d8-ba24-44d4-a6af-190ad090ca76.png)

At left hand, we using client library such as roslib, ros3djs to communicate with WebSocket, WebSocket convert message to ROS.
Objective: Click on button in web browser, at the point publish a message. File .py compare condition, if correct the string , we execute command line via subprocess.

Subprocess (python)
The subprocess use purpose when running the launch files dont need typing directly from the terminal.

![image](https://user-images.githubusercontent.com/105471622/183111655-8527b2ea-dedb-4c5f-a0c7-6503ddfa9f41.png)
Right here, I have 5 folders corresponding to 5 files running to give waypoint for /move_base_simple/goals. by the way click button on the website.
After clicked button, ROS object (Javasript Object) publish a string message. file call_navi_goal_from_web.py subcribe this message and compare with list of string"Table 1 2 3 4 5", if anything match , it will execute subprocess.Popen. Immediately, roslaunch navi_goals navi_goals.launch was being execute in shell.

![image](https://user-images.githubusercontent.com/105471622/183113599-e750508e-1a40-4d89-871d-376df5548dc0.png)

Waypoint file
The format of waypoint file as below:
![image](https://user-images.githubusercontent.com/105471622/183113920-ec51664e-7f8a-4c14-bd8a-8029d0278547.png)

We can add any point we want.Right here, I choose home position at (2,2) meters. Assumption I have 5 tables, so navi_goal contains of position of table 1, navi_goals2 contains of postion of table 2. Similar, navi_goals3 navi_goals4 navi_goals5 contain the rest of postion's table.
