cmake_minimum_required(VERSION 3.0.2)
project(jimmbot_gazebo)

add_compile_options(-std=c++17)

find_package(catkin REQUIRED COMPONENTS roslaunch)

catkin_package()

roslaunch_add_file_check(launch)

install(
  DIRECTORY launch worlds
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
