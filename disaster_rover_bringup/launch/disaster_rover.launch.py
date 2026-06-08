from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    
    # PATHS


    description_pkg = get_package_share_directory(
        'disaster_rover_description'
    )

    bringup_pkg = get_package_share_directory(
        'disaster_rover_bringup'
    )

    urdf_path = os.path.join(
        description_pkg,
        'urdf',
        'rover.urdf.xacro'
    )

    world_path = os.path.join(
        description_pkg,
        'worlds',
        'testworld1.sdf'
    )

    bridge_path = os.path.join(
        bringup_pkg,
        'config',
        'ros_gz_bridge.yaml'
    )

    gazebo_launch = os.path.join(
        get_package_share_directory('ros_gz_sim'),
        'launch',
        'gz_sim.launch.py'
    )


    # ROBOT STATE PUBLISHER


    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',

        parameters=[{
            'robot_description':
            os.popen(f'xacro {urdf_path}').read(),

            'use_sim_time': True
        }],

        output='screen'
    )


    # GAZEBO
    
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            gazebo_launch
        ),

        launch_arguments={
            'gz_args': f'{world_path} -r'
        }.items()
    )

    
    # SPAWN ROBOT
    

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',

        arguments=[
            '-topic', 'robot_description',
            '-name', 'disaster_rover',
            '-x', '0',
            '-y', '0',
            '-z', '0.5'
        ],

        output='screen'
    )

    
    # ROS <-> GAZEBO BRIDGE
    

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',

        parameters=[{
            'config_file': bridge_path
        }],

        output='screen'
    )

    
    # RVIZ


    rviz = Node(
        package='rviz2',
        executable='rviz2',

        parameters=[{
            'use_sim_time': True
        }],

        output='screen'
    )

    
    # LAUNCH
    

    return LaunchDescription([

        robot_state_publisher,

        gazebo,

        spawn_robot,

        bridge,

        rviz

    ])