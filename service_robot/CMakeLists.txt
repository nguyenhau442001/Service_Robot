cmake_minimum_required(VERSION 2.8.3)

project(service_robot)

find_package(catkin REQUIRED COMPONENTS roscpp rospy std_msgs roslaunch message_generation )

catkin_package()

# very important (import library)
include_directories(include ${catkin_INCLUDE_DIRS})

foreach(dir config launch meshes urdf)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)

add_executable(talker.cpp scripts/talker.cpp)
target_link_libraries(talker.cpp ${catkin_LIBRARIES})


add_executable(listener.cpp scripts/listener.cpp)
target_link_libraries(listener.cpp ${catkin_LIBRARIES})

catkin_install_python(PROGRAMS scripts/keyboard_teleop.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

catkin_install_python(PROGRAMS scripts/call_navi_goal_from_web.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

catkin_install_python(PROGRAMS scripts/converted_odom.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
