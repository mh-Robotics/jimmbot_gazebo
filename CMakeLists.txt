cmake_minimum_required(VERSION 3.8)
project(jimmbot_gazebo)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config launch media
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
