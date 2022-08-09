import subprocess
import time

subprocess.Popen('roslaunch service_robot amcl_move_base_gazebo.launch',shell=True) 
time.sleep(5000)
subprocess.Popen('roslaunch rosbridge_server rosbridge_websocket.launch',shell=True) 
time.sleep(500)
