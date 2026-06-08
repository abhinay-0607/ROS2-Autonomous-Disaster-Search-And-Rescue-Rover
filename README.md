# 🚨 Disaster Rover: Autonomous Search and Rescue System

![ROS2](https://img.shields.io/badge/ROS2-Jazzy-blue)
![Gazebo](https://img.shields.io/badge/Gazebo-Harmonic-orange)
![Python](https://img.shields.io/badge/Python-3.12-green)
![Status](https://img.shields.io/badge/Status-Active-success)

---

# 📖 Overview

Disaster Rover is an autonomous search and rescue robot developed using ROS 2 Jazzy and Gazebo Harmonic.

The rover is designed to operate in disaster environments where human access may be difficult or dangerous.

The system autonomously:

- Explores the environment
- Detects victims
- Approaches victims
- Locates emergency backpacks
- Retrieves backpacks using a robotic arm
- Delivers supplies to victims
- Reports mission completion

The entire system is implemented as a collection of ROS 2 nodes communicating through topics and state transitions.

---

# 🎯 Project Objectives

The goal of the project is to develop an autonomous disaster response rover capable of:

✅ Autonomous exploration

✅ Victim detection

✅ Victim localization

✅ Obstacle avoidance

✅ Backpack retrieval

✅ Emergency supply delivery

✅ Robotic arm manipulation

✅ Sensor integration

✅ Fully autonomous mission execution

---

# 🏗 System Architecture

```text
                         +----------------+
                         | Mission Manager|
                         +-------+--------+
                                 |
        --------------------------------------------------
        |                     |                         |
        v                     v                         v

+---------------+   +----------------+     +------------------+
| Explorer Node |   | Victim Detector|     | Obstacle Detector|
+-------+-------+   +--------+-------+     +--------+---------+
        |                    |                     |
        |                    |                     |
        v                    v                     |
+---------------+   +----------------+            |
| Rover Motion  |   | Victim Pose    |            |
+-------+-------+   +--------+-------+            |
        |                    |                    |
        |                    v                    |
        |          +--------------------+         |
        |          | Victim Approach    |         |
        |          +---------+----------+         |
        |                    |                    |
        |                    v                    |
        |          +--------------------+         |
        |          | Backpack Approach  |         |
        |          +---------+----------+         |
        |                    |                    |
        |                    v                    |
        |          +--------------------+         |
        |          | Backpack Pickup    |         |
        |          +---------+----------+         |
        |                    |                    |
        |                    v                    |
        |          +--------------------+         |
        |          | Backpack Delivery  |         |
        |          +--------------------+         |
```

---

# 📂 Repository Structure

```text
disaster_ws/
│
├── src/
│
├── disaster_rover_ai/
│   │
│   ├── autonomous_explorer.py
│   ├── victim_detector.py
│   ├── victim_approach.py
│   ├── backpack_approach.py
│   ├── backpack_pickup.py
│   ├── backpack_delivery.py
│   ├── obstacle_detector.py
│   ├── ambulance_reacher.py
│   └── mission_manager.py
│
├── disaster_rover_description/
│   │
│   ├── urdf/
│   │   ├── rover.urdf.xacro
│   │   ├── sensors.xacro
│   │   └── gazebo_plugins.xacro
│   │
│   ├── worlds/
│   │   └── testworld1.sdf
│   │
│   ├── meshes/
│   │
│   └── rviz/
│
└── disaster_rover_bringup/
    │
    ├── launch/
    └── config/
```

---

# 🤖 Robot Description

The robot is a four-wheel differential drive rover.

## Base

- Differential drive
- Four wheels
- Independent wheel joints

## Sensors

### LiDAR

Used for:

- Obstacle detection
- Environment perception
- Exploration

Topic:

```bash
/scan
```

### RGB Camera

Used for:

- Victim detection
- Visual perception

Topics:

```bash
/camera/image_raw
/camera/camera_info
```

### IMU

Used for:

- Orientation estimation
- Motion feedback

Topic:

```bash
/imu
```

### Odometry

Used for:

- Position tracking
- Mission execution

Topic:

```bash
/odom
```

---

# 🦾 Robotic Arm

The rover contains a multi-joint manipulator.

Joints:

```text
arm_base_joint
shoulder_joint
elbow_joint
wrist_joint
```

Purpose:

- Backpack pickup
- Supply delivery
- Future object manipulation tasks

---

# 🌍 Disaster Environment

The custom Gazebo world contains:

- Victims
- Emergency backpacks
- Ambulance
- Rocks
- Obstacles
- Rubble
- Terrain features

The rover must autonomously complete rescue missions within this environment.

---

# 🧠 Mission States

Mission Manager controls the rover through different stages.

```text
EXPLORE

VICTIM_FOUND

APPROACH_VICTIM

SEARCH_BACKPACK

APPROACH_BACKPACK

PICKUP_BACKPACK

DELIVER_BACKPACK

MISSION_COMPLETE
```

---

# 🔄 ROS Topics

## Published Topics

```text
/cmd_vel
/mission_state
/victim_detected
/victim_pose
```

## Sensor Topics

```text
/scan
/camera/image_raw
/camera/camera_info
/imu
/odom
```

## Arm Control Topics

```text
/arm_base_joint/cmd_pos
/shoulder_joint/cmd_pos
/elbow_joint/cmd_pos
/wrist_joint/cmd_pos
```

---

# 🔧 Installation

## Clone Repository

```bash
cd ~/disaster_ws/src

git clone https://github.com/yourusername/disaster-rover.git
```

---

## Install Dependencies

```bash
sudo apt update

sudo apt install \
ros-jazzy-ros-gz \
ros-jazzy-xacro \
ros-jazzy-rviz2 \
ros-jazzy-tf2-tools \
python3-opencv
```

---

## Build Workspace

```bash
cd ~/disaster_ws

colcon build --symlink-install
```

---

## Source Workspace

```bash
source install/setup.bash
```

---

# 🚀 Running the Project

## Launch Gazebo World

```bash
ros2 launch disaster_rover_bringup disaster_rover.launch.py
```

---

## Launch ROS-Gazebo Bridges

### LiDAR

```bash
ros2 run ros_gz_bridge parameter_bridge \
/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan
```

### Camera

```bash
ros2 run ros_gz_bridge parameter_bridge \
/camera@sensor_msgs/msg/Image@gz.msgs.Image
```

### TF

```bash
ros2 run ros_gz_bridge parameter_bridge \
/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V
```

---

## Run Mission Manager

```bash
ros2 run disaster_rover_ai mission_manager
```

---

## Run Explorer

```bash
ros2 run disaster_rover_ai autonomous_explorer
```

---

## Run Victim Detector

```bash
ros2 run disaster_rover_ai victim_detector
```

---

## Run Victim Approach

```bash
ros2 run disaster_rover_ai victim_approach
```

---

## Run Backpack Approach

```bash
ros2 run disaster_rover_ai backpack_approach
```

---

## Run Backpack Pickup

```bash
ros2 run disaster_rover_ai backpack_pickup
```

---

## Run Backpack Delivery

```bash
ros2 run disaster_rover_ai backpack_delivery
```

---

# 🧪 Useful Commands

Check nodes:

```bash
ros2 node list
```

Check topics:

```bash
ros2 topic list
```

View TF tree:

```bash
ros2 run tf2_tools view_frames
```

Check odometry:

```bash
ros2 topic echo /odom
```

Check LiDAR:

```bash
ros2 topic echo /scan
```

Check camera:

```bash
ros2 topic echo /camera/image_raw
```

---

# 📸 Demonstration

Example mission sequence:

1. Rover starts exploration.
2. Victim detected.
3. Rover approaches victim.
4. Backpack located.
5. Rover approaches backpack.
6. Arm retrieves backpack.
7. Rover delivers backpack.
8. Mission completed.

---

# 🔮 Future Improvements

- YOLO-based victim detection
- Thermal camera integration
- Real-world hardware deployment
- Multi-rover coordination
- GPS-denied navigation
- Reinforcement learning exploration
- 3D mapping
- Autonomous grasping

---

# 👨‍💻 Author

Abhinay

B.Tech

Indian Institute of Technology Bhubaneswar

Areas of Interest:

- ROS 2
- Autonomous Robotics
- Search and Rescue Systems
- Computer Vision
- Artificial Intelligence

---

# 📜 License

MIT License

---

# ⭐ Support

If you found this project useful, consider giving the repository a ⭐ on GitHub.
