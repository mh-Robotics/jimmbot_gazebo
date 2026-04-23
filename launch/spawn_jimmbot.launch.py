from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    robot_namespace = LaunchConfiguration('robot_namespace')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')
    yaw = LaunchConfiguration('yaw')
    world_sdf = LaunchConfiguration('world_sdf')
    headless = LaunchConfiguration('headless')

    description_launch = PathJoinSubstitution(
        [FindPackageShare('jimmbot_description'), 'launch', 'description.launch.py']
    )
    sim_launch = PathJoinSubstitution(
        [FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py']
    )
    spawn_launch = PathJoinSubstitution(
        [FindPackageShare('ros_gz_sim'), 'launch', 'gz_spawn_model.launch.py']
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
            'headless',
            default_value='false',
            description='Run Gazebo Sim server-only when true.',
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
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(spawn_launch),
            launch_arguments={
                'world': 'empty',
                'topic': 'robot_description',
                'entity_name': robot_namespace,
                'x': x,
                'y': y,
                'z': z,
                'Y': yaw,
            }.items(),
        ),
    ])