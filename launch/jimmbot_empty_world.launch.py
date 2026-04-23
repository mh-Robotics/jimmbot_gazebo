from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    spawn_launch = PathJoinSubstitution(
        [FindPackageShare('jimmbot_gazebo'), 'launch', 'spawn_jimmbot.launch.py']
    )

    return LaunchDescription([
        DeclareLaunchArgument('robot_namespace', default_value='jimmbot'),
        DeclareLaunchArgument('x', default_value='0.0'),
        DeclareLaunchArgument('y', default_value='0.0'),
        DeclareLaunchArgument('z', default_value='1.0'),
        DeclareLaunchArgument('yaw', default_value='0.0'),
        DeclareLaunchArgument('headless', default_value='false'),
        DeclareLaunchArgument('bridge_sensors', default_value='true'),
        DeclareLaunchArgument('enable_control', default_value='true'),
        DeclareLaunchArgument(
            'world_name',
            default_value='empty',
            description='World name inside the SDF used for spawning.',
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(spawn_launch),
            launch_arguments={
                'robot_namespace': LaunchConfiguration('robot_namespace'),
                'x': LaunchConfiguration('x'),
                'y': LaunchConfiguration('y'),
                'z': LaunchConfiguration('z'),
                'yaw': LaunchConfiguration('yaw'),
                'headless': LaunchConfiguration('headless'),
                'bridge_sensors': LaunchConfiguration('bridge_sensors'),
                'enable_control': LaunchConfiguration('enable_control'),
                'world_name': LaunchConfiguration('world_name'),
                'world_sdf': 'empty.sdf',
            }.items(),
        ),
    ])