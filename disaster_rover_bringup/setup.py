from setuptools import setup, find_packages

package_name = 'disaster_rover_bringup'

setup(
    name=package_name,

    version='0.0.0',

    packages=find_packages(exclude=['test']),

    data_files=[

        # ==========================================
        # PACKAGE INDEX
        # ==========================================

        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),

        # ==========================================
        # PACKAGE.XML
        # ==========================================

        (
            'share/' + package_name,
            ['package.xml'],
        ),

        # ==========================================
        # LAUNCH FILES
        # ==========================================

        (
            'share/' + package_name + '/launch',
            [
                'launch/disaster_rover.launch.py',
            ],
        ),

        # ==========================================
        # CONFIG FILES
        # ==========================================

        (
            'share/' + package_name + '/config',
            [
                'config/ros_gz_bridge.yaml',
            ],
        ),

    ],

    install_requires=['setuptools'],

    zip_safe=True,

    maintainer='sai-abhinay',

    maintainer_email='24ec01030@iitbbs.ac.in',

    description='Disaster rover bringup package',

    license='Apache License 2.0',

    tests_require=['pytest'],

    entry_points={
        'console_scripts': [
        ],
    },
)