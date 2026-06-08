from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'disaster_rover_ai'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
    (
        'share/ament_index/resource_index/packages',
        ['resource/disaster_rover_ai']
    ),

    (
        'share/disaster_rover_ai',
        ['package.xml']
    ),
    (
        os.path.join('share', 'disaster_rover_ai', 'launch'),
        glob('launch/*.py')
    ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sai-abhinay',
    maintainer_email='24ec01030@iitbbs.ac.in',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    'console_scripts': [
        'autonomous_explorer = disaster_rover_ai.autonomous_explorer:main',
        'victim_detector = disaster_rover_ai.victim_detector:main',
        'obstacle_detector = disaster_rover_ai.obstacle_detector:main',
        
        'victim_approach = disaster_rover_ai.victim_approach:main',
        'mission_manager = disaster_rover_ai.mission_manager:main',
        'backpack_approach = disaster_rover_ai.backpack_approach:main',
        'ambulance_reacher = disaster_rover_ai.ambulance_reacher:main',
        'backpack_pickup = disaster_rover_ai.backpack_pickup:main',
        'backpack_follower = disaster_rover_ai.backpack_follower:main',
    ],
},
)
