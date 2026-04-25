import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    robot_namespace = LaunchConfiguration('robot_namespace')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')
    yaw = LaunchConfiguration('yaw')
    world_sdf = LaunchConfiguration('world_sdf')
    world_name = LaunchConfiguration('world_name')
    headless = LaunchConfiguration('headless')
    bridge_sensors = LaunchConfiguration('bridge_sensors')
    use_sim_time = LaunchConfiguration('use_sim_time')
    enable_control = LaunchConfiguration('enable_control')

    gazebo_share = FindPackageShare('jimmbot_gazebo')
    description_share = FindPackageShare('jimmbot_description')

    description_launch = PathJoinSubstitution(
        [FindPackageShare('jimmbot_description'), 'launch', 'description.launch.py']
    )
    sim_launch = PathJoinSubstitution(
        [FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py']
    )
    spawn_launch = PathJoinSubstitution(
        [FindPackageShare('ros_gz_sim'), 'launch', 'gz_spawn_model.launch.py']
    )
    bridge_config = PathJoinSubstitution(
        [FindPackageShare('jimmbot_gazebo'), 'config', 'sensor_bridge.yaml']
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'robot_namespace',
            default_value='jimmbot',
            description='Entity name used when spawning the robot in Gazebo.',
        ),
        DeclareLaunchArgument('x', default_value='0.0'),
        DeclareLaunchArgument('y', default_value='0.0'),
        DeclareLaunchArgument('z', default_value='1.0'),
        DeclareLaunchArgument('yaw', default_value='0.0'),
        DeclareLaunchArgument(
            'world_sdf',
            default_value='empty.sdf',
            description='Gazebo Sim world file name.',
        ),
        DeclareLaunchArgument(
            'world_name',
            default_value='default',
            description='World name inside the SDF used for spawning.',
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
            description='Use simulation clock for robot_state_publisher.',
        ),
        DeclareLaunchArgument(
            'enable_control',
            default_value='true',
            description='Load Gazebo control plugin interfaces from the robot description.',
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
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(sim_launch),
            launch_arguments={
                'gz_args': ['-r -s ', world_sdf],
            }.items(),
            condition=IfCondition(headless),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(sim_launch),
            launch_arguments={
                'gz_args': ['-r ', world_sdf],
            }.items(),
            condition=UnlessCondition(headless),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(description_launch),
            launch_arguments={
                'use_sim_time': use_sim_time,
                'enable_control': enable_control,
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
                '/world/',
                world_name,
                '/model/',
                robot_namespace,
                '/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model',
            ]],
            remappings=[
                (
                    ['/world/', world_name, '/model/', robot_namespace, '/joint_state'],
                    'joint_states',
                ),
            ],
            condition=IfCondition(bridge_sensors),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(spawn_launch),
            launch_arguments={
                'world': world_name,
                'topic': 'robot_description',
                'entity_name': robot_namespace,
                'x': x,
                'y': y,
                'z': z,
                'Y': yaw,
            }.items(),
        ),
    ])