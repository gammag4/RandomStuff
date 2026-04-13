# ROS2

[Learn ROS 2: Beginner to Advanced Course (Concepts and Code)](https://www.youtube.com/watch?v=HJAE5Pk8Nyw)
[a](https://www.youtube.com/playlist?list=PLNw2RD-1J5YYvFGiMafRD_axHrBUGvuIg)
[a](https://www.youtube.com/playlist?list=PLLSegLrePWgJudpPUof4-nVFHGkB62Izy)
[a](https://www.youtube.com/playlist?list=PLunhqkrRNRhYYCaSTVP-qJnyUPkTxJnBt)
[a](https://www.youtube.com/playlist?list=PLunhqkrRNRhYAffV8JDiFOatQXuU-NnxT)

TODO check deploying/offline/how to use with real system

## Concepts

packages libraries executables
packages have multiple libs
packages offer multiple executables to use

has multiple nodes which send/receive data to each other
has parameters
    you can pass parameters to a node when you want to input data to a node
    its kind of like using the node as a function
connecting nodes: nodes can send data through
    topics (used for continuous streams of data)
        publisher nodes publish data to a topic
        subscriber nodes subscribe to topics to get data
        multiple nodes can publish/subscribe to same topic
            but they have to publish with same exact type to same topic
            topics have a type (protocol they communicate)
        decoupled: the whole idea of the system is that it should not break depending on order the nodes are created/destroyed
    services/actions (used for when you want the node to provide services for clients to use (stuff that is not stream of data))
        services are things that you dont need to keep getting progress updates over time
            client node calls for a service (does a request)
            server node does the service (sends a response)
        actions are things that you need progress updates (e.g. tasks) (more complex than services)
            client node starts the task
            server node does the task
            internally, actions use topics and services
            action has three things:
                goal service: what to achieve (e.g. move to certain location)
                result service: indicate the result of the task (if it was successful or not/why not/final position)
                feedback topic: keeps giving progress updates to client
            action type describes goal, result and feedback formats
            process:
                starting:
                    sends goal service request
                    gets goal service result
                    sends result service request
                doing task: keeps receiving progress from feedback topic
                ending: receives result service result

## Commands

```bash
rqt_graph
    shows graph with nodes topics etc

ros2 <cmd> -h
    help
ros2 <cmd> -c
    counts stuff

ros2 pkg list
ros2 executables
ros2 pkg executables turtlesim
ros2 run turtlesim turtlesim_node
ros2 run turtlesim turtle_teleop_key

ros2 node list
ros2 node info /turtlesim
    topics (subscribers/publishers), services (servers/clients), actions (servers/clients)

ros2 interface show geometry_msgs/msg/Twist
    ros2 interface show turtlesim/srv/Spawn
    shows type (topic/service/action)

ros2 param list
    ros2 param list /turtlesim
ros2 param dump /turtlesim
    ros2 param dump /turtlesim > turtlesim_params.yaml
ros2 param load /turtlesim turtlesim_params.yaml
    ros2 run turtlesim turtlesim_node --ros-args --params-file turtlesim_params.yaml
ros2 param describe /turtlesim background_g
ros2 param get /turtlesim background_b
ros2 param set /turtlesim background_b 255

ros2 topic list -t
ros2 topic info /turtle1/cmd_vel
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 2.0}}"
    creates temp node that pubs to topic
ros2 topic echo /turtle1/cmd_vel
    ros2 topic echo /turtle1/pose
    creates temp node that subs to topic and echos it
ros2 topic hz /turtle1/pose
    shows frequency that topic is published avg min max std dev

ros2 service list -t
ros2 service info /clear
ros2 service find std_srvs/srv/Empty
    finds services with that specific type
ros2 service call /clear std_srvs/srv/Empty
    ros2 service call /spawn turtlesim/srv/Spawn
    creates temp client node that calls service
    clears drawing in turtlesim
ros2 service standalone <type> <name>
    creates server temp node

ros2 action list -t
ros2 action info /turtle1/rotate_absolute
ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta: 10}"
    creates temp client node that sends action goal
    rotates turtle to the absolute angle position theta 10
```

## ROS Workspace

```
ros2_workspace_folder/
    src/
        package1/
            src/
            CMakeLists.txt
            package.xml
        package2/
            src/
            CMakeLists.txt
            package.xml
        ...
```

### colcon

configuring colcon

```bash
# install colcon
sudo apt install python3-colcon-common-extensions

# configure colcon tab completion (choose bash or fish)
#echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc
#echo "bass source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.config/fish/config.fish
```

ready example

```bash
mkdir -p ros2_workspace_folder/src
cd ros2_workspace_folder

git clone https://github.com/ros/ros_tutorials -b jazzy

# build current workspace with symlinks in source or build dirs instead of copying files (to allow editing/rebuilding workspace)
# install python dependencies needed if errors happen
colcon build --symlink-install
bass source install/local_setup.bash
```

create custom packages/nodes

```bash
# create folders
mkdir -p ros2_workspace_folder/src
cd ros2_workspace_folder

# create package (either python or cpp)
cd src
#ros2 pkg create --build-type ament_cmake --node-name my_node my_package
#ros2 pkg create --build-type ament_python my_package
cd ..

# build stuff
colcon build --packages-select my_package
bass source install/local_setup.bash

# Update code/cmakelists/package.xml

# install deps
rosdep install -i --from-path src --rosdistro jazzy -y

# build
colcon build --packages-select my_package

# run stuff terminal
bass source install/setup.bash
ros2 run pubsub_example pub_example

# run stuff terminal 2
bass source install/setup.bash
ros2 run pubsub_example sub_example
```

### launch files

```bash
# ros2 launch package_name launch_file_name.launch.py
ros2 launch gazebo_tutorial gazebo.launch.py
```

https://youtu.be/HJAE5Pk8Nyw?t=2984
