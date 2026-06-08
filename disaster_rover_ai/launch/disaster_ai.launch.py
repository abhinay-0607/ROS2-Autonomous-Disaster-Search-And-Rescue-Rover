from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([

       

        Node(
            package='disaster_rover_ai',
            executable='victim_detector',
            output='screen'
        ),

        Node(
            package='disaster_rover_ai',
            executable='obstacle_detector',
            output='screen'
        ),

       

        Node(
            package='disaster_rover_ai',
            executable='mission_manager',
            output='screen'
        ),


        Node(
            package='disaster_rover_ai',
            executable='autonomous_explorer',
            output='screen'
        ),

        

        Node(
            package='disaster_rover_ai',
            executable='victim_approach',
            output='screen'
        ),

      

        Node(
            package='disaster_rover_ai',
            executable='backpack_approach',
            output='screen'
        ),

        Node(
            package='disaster_rover_ai',
            executable='backpack_pickup',
            output='screen'
        ),

        Node(
            package='disaster_rover_ai',
            executable='backpack_follower',
            output='screen'
        ),


        Node(
            package='disaster_rover_ai',
            executable='ambulance_reacher',
            output='screen'
        )

    ])