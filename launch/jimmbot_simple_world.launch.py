import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """Launch jimmbot in Gazebo Sim with a custom world (default: simple.sdf)."""
    robot_namespace = LaunchConfiguration('robot_namespace')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')
    yaw = LaunchConfiguration('yaw')
    world_path = LaunchConfiguration('world_path')
    headless = LaunchConfiguration('headless')
    bridge_sensors = LaunchConfiguration('bridge_sensors')
    use_sim_time = LaunchConfiguration('use_sim_time')

    gazebo_share = FindPackageShare('jimmbot_gazebo')
    description_share = FindPackageShare('jimmbot_description')

    description_launch = PathJoinSubstitution(
        [FindPackageShare('jimmbot_description'), 'launch', 'description.launch.py']
    )
    sim_launch = PathJoinSubstitution(
        [FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py']
    )
    spawn_launch = PathJoinSubstitution(
        [FindPackageShare('jimmbot_gazebo'), 'launch', 'spawn_jimmbot.launch.py']
    )
    bridge_config = PathJoinSubstitution(
        [FindPackageShare('jimmbot_gazebo'), 'config', 'sensor_bridge.yaml']
    )
    server_config = PathJoinSubstitution(
        [FindPackageShare('jimmbot_gazebo'), 'config', 'server.config']
    )
    default_world_path = PathJoinSubstitution(
        [FindPackageShare('jimmbot_gazebo'), 'media', 'worlds', 'simple.sdf']
    )

    return LaunchDescription([
        DeclareLaunchArgument('robot_namespace', default_value='jimmbot'),
        DeclareLaunchArgument('x', default_value='0.0'),
        DeclareLaunchArgument('y', default_value='0.0'),
        DeclareLaunchArgument('z', default_value='1.0'),
        DeclareLaunchArgument('yaw', default_value='0.0'),
        DeclareLaunchArgument(
            'world_path',
            default_value=default_world_path,
            description='Path to the Gazebo world SDF file.',
        ),
        DeclareLaunchArgument(
            'headless',
            default_value='false',
            description='Run Gazebo Sim server-only when true.',
        ),
        DeclareLaunchArgument(
            'bridge_sensors',
            default_value='true',
            description='Bridge Gazebo sensor topics to ROS 2 topics.',
        ),
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation clock.',
        ),
        SetEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=[
                gazebo_share,
                os.pathsep,
                description_share,
                os.pathsep,
                EnvironmentVariable('GZ_SIM_RESOURCE_PATH', default_value=''),
            ],
        ),
        SetEnvironmentVariable(
            name='GZ_SIM_SERVER_CONFIG_PATH',
            value=server_config,
        ),
        SetEnvironmentVariable(
            name='IGN_GAZEBO_SERVER_CONFIG_PATH',
            value=server_config,
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(sim_launch),
            launch_arguments={
                'gz_args': ['-r -s ', world_path],
            }.items(),
            condition=IfCondition(headless),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(sim_launch),
            launch_arguments={
                'gz_args': ['-r ', world_path],
            }.items(),
            condition=UnlessCondition(headless),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(description_launch),
            launch_arguments={
                'use_sim_time': use_sim_time,
            }.items(),
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='jimmbot_sensor_bridge',
            output='screen',
            parameters=[{'config_file': bridge_config}],
            condition=IfCondition(bridge_sensors),
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='jimmbot_joint_state_bridge',
            output='screen',
            arguments=[[
                '/world/default/model/',
                robot_namespace,
                '/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model',
            ]],
            remappings=[
                (
                    ['/world/default/model/', robot_namespace, '/joint_state'],
                    'joint_states',
                ),
            ],
            condition=IfCondition(bridge_sensors),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(spawn_launch),
            launch_arguments={
                'robot_namespace': robot_namespace,
                'x': x,
                'y': y,
                'z': z,
                'yaw': yaw,
                'world_name': 'default',
            }.items(),
        ),
    ])