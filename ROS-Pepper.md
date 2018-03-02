<p align="center">April 2017
<br>PXL University College
<br>Maarten Bloemen (Junior)
<br>
<br>Updated for ROS Kinetic Kame by
<br>Niels Debrier</p>



### 1. Installing ROS Kinetic Kame
Follow the instructions given on the ROS wiki [here](http://wiki.ros.org/kinetic/Installation/Ubuntu).

### 2. Installation for Pepper
1. Pepper requires some additional ROS packages:
* Open a terminal
* Type (copy/paste) the following commands:
  * `$ sudo apt-get update`
  * `$ sudo apt-get install ros-kinetic-dr-base ros-kinetic-move-base-msgs ros-kinetic-octomap ros-kinetic-octomap-msgs ros-kinetic-humanoid-msgs ros-kinetic-humanoid-nav-msgs ros-kinetic-camera-info-manager ros-kinetic-camera-info-manager-py`
2. Installing the necessary packages:
* Open a terminal
* Type (copy/paste) the following command:
  * `$ sudo apt-get install ros-kinetic-pepper-.*`
3. Installing the developer packages from source:
* CD into your catkin workspace (`$ cd ~/catkin_ws/src`)
  * if you don't have a catkin workspace, follow tutorial: [here](http://wiki.ros.org/catkin/Tutorials/create_a_workspace)
* Clone the developer packages into your catkin workspace (~/catkin_ws/src):
  * `$ git clone https://github.com/ros-naoqi/naoqi_driver.git`
* Make sure you get all the dependencies installed:
  * `$ rosdep install -i -y --from-paths ./naoqi_driver`
* And finally build the packages:
  * `$ source /opt/ros/indigo/setup.sh`
  * `$ cd ../ && catkin_make`
4. Installing NAOqi SDK:
* Download python SDK (download "pynaoqi-python2.7-2.1.2.17-linux64", this is the one we tested and works)
* Extract the tar.gz
* Add the following line to your .bashrc:
  * `export PYTHONPATH=${PYTHONPATH}:/path/to/python-sdk`

### 3. Connecting to a physical Pepper
1. Start a roscore:
* `$ roscore`
2. Connecting to Pepper:
* `$ roslaunch pepper_bringup pepper_full.launch nao_ip:=<robot_ip> roscore_ip:=<roscore_ip> network_interface:=<eth0|wlan0|vpn0>`
3. **[OPTIONAL]** Connecting to Pepper with the python bridge:
* `$ roslaunch pepper_bringup pepper_full_py.launch nao_ip:=<yourRobotIP> roscore_ip:=<roscore_ip>`

### 4. Connecting to a virtual Pepper
**TBA**

### 5. Vizualize Pepper in RVIZ
1. Starting Rviz:
* `$ rosrun rviz rviz`
2. **TBA**
