#ROS2 package for Logitech F710 wireless joystick

Ensure the evdev library is installed:
  pip3 install evdev

ros2 run logitech_f10_ros joystick_node

will publish /joy node with joystick axes and buttons.
topic type: sensor_msgs/msg/Joy

---
header:
  stamp:
    sec: 1720872191
    nanosec: 503086803
  frame_id: ''
axes:
- 0.0
- -0.003936887718737125
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
buttons:
- 0
- 0
- 0
- 0
- 0
- 0
- 0
- 0
- 0
- 0
- 0
- 0
---

