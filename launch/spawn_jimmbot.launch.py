from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """Spawn jimmbot robot into Gazebo Sim world."""
    robot_namespace = LaunchConfiguration('robot_namespace')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')
    yaw = LaunchConfiguration('yaw')
    world_name = LaunchConfiguration('world_name')

    spawn_launch = PathJoinSubstitution(
        [FindPackageShare('ros_gz_sim'), 'launch', 'gz_spawn_model.launch.py']
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'robot_namespace',
            default_value='jimmbot',
            description='Entity name used when spawning the robot in Gazebo.',
        ),
        DeclareLaunchArgument('x', default_value='0.0', description='X position'),
        DeclareLaunchArgument('y', default_value='0.0', description='Y position'),
        DeclareLaunchArgument('z', default_value='1.0', description='Z position'),
        DeclareLaunchArgument('yaw', default_value='0.0', description='Yaw rotation'),
        DeclareLaunchArgument(
            'world_name',
            default_value='default',
            description='World name inside the SDF used for spawning.',
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