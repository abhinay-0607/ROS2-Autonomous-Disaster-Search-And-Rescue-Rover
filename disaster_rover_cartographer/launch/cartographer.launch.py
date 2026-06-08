from launch import LaunchDescription
from launch_ros.actions import Node

import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    pkg_dir = get_package_share_directory(
        'disaster_rover_cartographer'
    )

    config_dir = os.path.join(pkg_dir, 'config')

    return LaunchDescription([

        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            output='screen',
            arguments=[
                '-configuration_directory',
                config_dir,
                '-configuration_basename',
                'rover.lua'
            ]
        ),

        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            output='screen',
            arguments=[
                '-resolution',
                '0.05'
            ]
        )
    ])