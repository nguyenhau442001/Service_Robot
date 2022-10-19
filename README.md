# PART I. OVERVIEW ESSENTIAL PART COMMUNICATE
1.Introduction

One thing you need to know is that ROS supports plenty of programming languages, but popular is C++ and Python, which don’t have C language. Therefore, I conduct coding for the STM32 board (controller board) by using C++, in the embedded computer (mini pc or Ras) we run script python or C++. We will communicate between the PC with STM32 via ROS SERIAL. 
In order to communicate with ROS, the first step we need do is install the rosserial package. 

![image](https://user-images.githubusercontent.com/105471622/196738444-9dd84fe6-eab7-49eb-9ac8-48d59ac44471.png)

Next step, we need determine how many topic neccesary for this application.

Publisher node (buffer size is 1024 bytes)
1.	sensor_state [turtlebot3_msgs/SensorState]  (may be need)
2.	version_info [turtlebot3_msgs/VersionInfo] (optional)
3.	imu [sensor_msgs/Imu] (compulsory)
4.	odom [nav_msgs/Odometry] (compulsory)
5.	battery_state [sensor_msgs/BatteryState] (optional)
6.	joint_states [sensor_msgs/JointState] (compulsory)
7.	magnetic_field [sensor_msgs/MagneticField] (compulsory)
8.	/tf [tf/tfMessage] (compulsory)

Subscribe node (buffer size is 1024 bytes)
1.	cmd_vel [geometry_msgs/Twist] (compulsory)
2.	motor_power [std_msgs/Bool] (optional)
3.	reset [std_msgs/Empty] (compulsory)
4.	sound [turtlebot3_msgs/Sound] (optional)


Set up TF (Transformation) 
1.	 Setup TF on Odometry [odom]
2.	 Setup TF on IMU [imu_link]
3.	 Setup TF on MagneticField [mag_link]
4.	 Setup TF on JointState [base_link]


# PART 2: KINETIC DIFFERENTIAL DRIVE MOBILE BOT

The common method to get kinetic mobile robot, we consider as the picture it illustrate for basic model kinetic differential drive robot:

![image](https://user-images.githubusercontent.com/105471622/196739775-1a44c4a5-01c2-4700-9e5d-425551a7759b.png)

We assumed the robot rotate around any point, in instantaneous time we can consider motion is linear, so the linear velocity of the center has the formula:
                                                           
![image](https://user-images.githubusercontent.com/105471622/196741436-15c1fd77-d795-4a25-a4a0-d9e12acdfa1e.png)    
  
                                                           
Where v_l,v_r, v is left linear velocity of left,right,center of robot corresponding.

Have again

![image](https://user-images.githubusercontent.com/105471622/196741249-5b3fbe59-4a76-44c8-aabf-4c947f89cb83.png)

       
We do some projection velocity vector into flat plane, we obtain the velocity of x-axis and y-axis corresponding

![image](https://user-images.githubusercontent.com/105471622/196741322-f6b99628-0699-491f-a43b-45fbad0ea03c.png)

![image](https://user-images.githubusercontent.com/105471622/196741718-e606f7e6-6795-4b15-957f-ffa9e9ec9aac.png)

![image](https://user-images.githubusercontent.com/105471622/196741850-9b6f7e35-a65c-4105-bda0-21b122a5f165.png)

We can rewrite motion as below matrix form:

![image](https://user-images.githubusercontent.com/105471622/196741958-2b4bbf91-5204-40cc-ba7b-d752b0125322.png)

From the (3) and (8) equations, we extract:

![image](https://user-images.githubusercontent.com/105471622/196742093-a1ed9284-a8a0-402f-8e99-ec90b3971ee9.png)

![image](https://user-images.githubusercontent.com/105471622/196742140-82b8dacb-5b20-4bc0-bb91-6ab5284957ba.png)

I introduce the algorithm powerful and popular name DEAD RECKONING.

In navigation, dead reckoning is the process of calculating the current position of a moving object using a previously determined or fixed position and then combining estimates of speed, direction, and distance, time past. A corresponding term in biology is used to describe the processes by which animals update their estimate of their position or orientation. Inertial navigation systems, which provide directional information, use dead reckoning and are very widely used.
Similarly, we also apply dead reckoning to the kinetic model of the robot, and it is described as follows:

![image](https://user-images.githubusercontent.com/105471622/196742559-bfeab541-b302-47aa-b34a-11964c2cefc3.png)

Figure 1 Kinetic model of the robot

(Source: Authors: Kooktae Lee, Changbae Jung and Woojin Chung, Article “Accurate calibration of kinematic parameters for two wheel differential mobile robots”)

From the figure above we get the following equations:

![image](https://user-images.githubusercontent.com/105471622/196742675-031d5c8e-f262-4da4-b9b3-64daa166e8aa.png)

![image](https://user-images.githubusercontent.com/105471622/196742932-7de7ea88-3c02-42c7-a5be-5f41f2c4b845.png)

![image](https://user-images.githubusercontent.com/105471622/196742962-79cd54a2-f0b2-42af-8469-8f661ff43faf.png)

Wheel Encoder

An encoder is a mechanical motion sensor that generates a digital signal in response to the motion. An electromechanical device capable of converting motion into a digital signal or pulse. Thanks to the encoder, we can know the exact position of the rotation angle of the motor shaft, thereby calculating the displacement of the center of gravity of the robot. More specifically, to calculate equations (13), (14) we need to know the number of pulses reads, and ticks.
Assuming we have the right and left motor with a resolution , to know how much the wheel has rotated, we need to know how much an angle the wheel rotates according to 1 pulse (tick). For example, the motor uses a resolution of 4000 (pulses/rev), through the transmission ratio of 1:3, this means that the motor turns 3 revolutions the wheel only turns one revolution. Then 1 tick will be calculated as follows:

![image](https://user-images.githubusercontent.com/105471622/196743383-fd141aac-da01-450d-b8fb-a0bbd2de20ec.png)

The angular displacement of each wheel will be calculated as follows:

![image](https://user-images.githubusercontent.com/105471622/196743448-f78aeeca-92b7-4f52-9693-2a5647183bc3.png)

The workflow of control mobile base
![image](https://user-images.githubusercontent.com/105471622/196743528-ea7499db-eb1f-446d-af67-6e7ae8fc3f8e.png)

Keep in mind that the velocity pair sent down by Navigation stack is not constant in continuous time but it is discrete, i.e. every time delta T, this velocity pair value it will be different, it is still constant, but only for a period of delta T. So to control the robot base, we update the velocity value, but because the time is very small (select 0.001s), it can be considered as continuous.

# PART3 MAGNETOMETER CALIBRATION

MPU9250 is actually an IMU (Inertial Measurement Unit) sensor and a Magnetometer, the task of the IMU will measure inertia (including angular velocity and linear acceleration), while the Magnetometer will measure the local magnetic field. around the sensor.
The MPU9250 helps to give an exact orientation of an object with respect to its environment. It plays an important role in navigating aircraft and spacecraft. Similar in applications of self-propelled robots, we can use MPU9250 to determine the direction and coordinates of the robot. From quantities such as acceleration, angular velocity, magnetic field of the robot then converted to rotation angle of the robot.
Currently, I still not yet using Madgwick for some reason such as : error due to integral, drift. I compute yaw angle base on magnetic field. Unfortunely, hard ion and soft ion cause distortion for magnetic field. So before use it, we need to calibrate it!!!!!!!

![image](https://user-images.githubusercontent.com/105471622/196747454-4ccb4b54-f55b-4860-8dbc-64c5a87708be.png)
![image](https://user-images.githubusercontent.com/105471622/196747463-0b68a5cc-1d76-4ce3-bcfa-af1b18e30b0a.png)
![image](https://user-images.githubusercontent.com/105471622/196747485-adc2ecc4-9105-45e3-84cf-9c7852b76c33.png)

We can completely edit the magnetic field with the formula below:

![image](https://user-images.githubusercontent.com/105471622/196747610-597e5c3b-2191-46ae-8653-e50d8d5e3e98.png)

Where h_hat: calibration magnetic matrix, h_m magnetic sensor magnetic matrix, b: offset matrix, M: hard and soft iron matrix system.

The result after calibrated:

![image](https://user-images.githubusercontent.com/105471622/196747814-774c0011-895e-46ed-9a9d-c82106091522.png)

The yaw angle equal atan(my,mx)


# SIMULATION SERVICE ROBOT
I have consulted the documentation below:

    1.https://github.com/devanshdhrafani/diff_drive_bot?fbclid=IwAR13gKv9AT9qRRjoVsUqTYrhSJN_SqjqlOUT3N7VGfB8ZDaehv2m5LRvvdI

    2.https://devanshdhrafani.github.io/blog/2020/11/01/diffdrive.html?fbclid=IwAR2rnmI8jEJEn0mfh6qbEmEooA_AI3zIyLfcTQ-vht6G5wXuQnkvXc8n0ow

Link youtube: 
1.  https://www.youtube.com/watch?v=k0roG6xbp_c&t=11s.


This ROS package implements SLAM on a 2-wheeled differential drive robot to map an unknown environment. A keyboard is used to teleoperate the robot in Gazebo. The map generated is then used for autonomous navigation using the ROS Navigation stack.
# Installation
1. Build package from source: navigate to the source folder of your catkin workspace and build this package using:

    $ git clone https://github.com/nguyenhau442001/Service_Robot.git
  
    $ cd ..
  
    $ catkin_make
2. Install Required dependencies:

    $ sudo apt-get install ros-noetic-dwa-local-planner.
    $ sudo apt-get install ros-noetic-rosbridge-server
    
If you missing any dependencies packages, please install them before go move on to the next step.

# URDF 
![image](https://user-images.githubusercontent.com/105471622/174599261-1599c94a-85e2-402d-a6ea-d82d54f4b950.png)

As we can see, this is my URDF. I exported from Solidworks. My URDF have 4 links such as base_link, left and right wheel link, and finally lidar link.

# GAZEBO 

![image](https://user-images.githubusercontent.com/105471622/174600486-9ba8c109-3487-466f-9884-f65708d84ead.png)

This is my robot when it's spawning in a simulation environment GAZEBO
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
Purpose: To control the robot via the web browser (Using rosbridge_server package - this package helps frontend developers build a web interface to visualize or interact with ROS Server.  
Requires components:
1. roslib,ros2djs,ros3djs,rosbridge_server (use Websocket)
2. Basic knowledge HTML,CSS,JS and ROS .

The key idea 
![image](https://user-images.githubusercontent.com/105471622/183107579-b43582d8-ba24-44d4-a6af-190ad090ca76.png)

On the left hand, we use client library such as roslib, ros2djs and ros3djs to communicate with WebSocket, WebSocket convert message to ROS that Robot can understandable.
Objective: Click on the button in a web browser, and at that point publish a message. File python will compare conditions if correct, we execute command line like "roslaunch navi_goals navi_goals" via subprocess.


Subprocess (python)
The subprocess use purpose when running the launch files dont need typing directly from the terminal.
Reference: https://docs.python.org/3/library/subprocess.html

![image](https://user-images.githubusercontent.com/105471622/183111655-8527b2ea-dedb-4c5f-a0c7-6503ddfa9f41.png)

First of all, we create a Javascript object using "roslib". This object will publish a message type String when we click any button in a web browser.  For instance,  we have 5 buttons respective to the 5 tables we want to move to, when we hit button "Table 1", immediately Javascript object will publish a message "Table 1" underlying topic "Moving_to_table". And we have "call_navi_goal_from_web.py" file, this file will take the message that Javascript object sending. And it will compare with the conditions.  If anything matches, it will execute the subprocess.popen. Immediately, "roslaunch navi_goals navi_goals.launch" was being executed in a terminal.

![image](https://user-images.githubusercontent.com/105471622/183113599-e750508e-1a40-4d89-871d-376df5548dc0.png)

Waypoint file
The format of waypoint file as below:

![image](https://user-images.githubusercontent.com/105471622/183113920-ec51664e-7f8a-4c14-bd8a-8029d0278547.png)

We can add any point we want. Right here, I choose the home position at (2,2) meters. The assumption is I have 5 tables, so navi_goal contains the position of table 1, and navi_goals2 contains of the position of table 2. Similar, navi_goals3 navi_goals4 navi_goals5 contains the rest of the position's table.

The order of execution command line:
1. roslaunch service_robot amcl_move_base_gazebo.launch
2. roslaunch rosbridge_server rosbridge_websocket.launch
3. rosrun service_robot call_navi_goal_from_web.py
4. Open web-gui.html in your browser, sometimes need to reload page.
5. After that, we already click any button to send the goal to /move_base. 
6. Execute instruction: rostopic echo /move_base_simple/goal to check to publish waypoint to the topic yet.


# SPEECH RECOGNITION.
Well, I wanna drive my robot to table and speak several sentences. Therefore, I have using the package "audio_common".

       $ sudo apt-get install ros-noetic-audio-common
       $ sudo apt-get install libasound2
       $ cd ~/catkin_ws
       $ source devel/setup.bash
       $ source /opt/ros/noetic/setup.bash
       $ source /home/hau/catkin_ws/devel/setup.bash 
       $ catkin_make
       
Droid speak p (R2 D2 robot - Starwar) : https://gitlab.com/easymov/droidspeak
Make your robot speak like R2-D2

![image](https://user-images.githubusercontent.com/105471622/184613628-22c897bb-e3c3-42c0-96f3-05a208584b94.png)


 
