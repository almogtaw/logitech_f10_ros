import os
import rclpy
from rclpy.node import Node
from evdev import InputDevice, categorize, ecodes
from sensor_msgs.msg import Joy

class JoystickNode(Node):
    def __init__(self):
        super().__init__('joystick_node')
        self.publisher_ = self.create_publisher(Joy, 'joy', 10)

        # Declare and get the normalization parameter
        self.declare_parameter('normalization_factor', 32767.0)
        self.normalization_factor = self.get_parameter('normalization_factor').get_parameter_value().double_value

        self.device_path = self.find_device_path()

        try:
            self.gamepad = InputDevice(self.device_path)
            self.get_logger().info(f'Connected to {self.gamepad.name} at {self.device_path}')
            self.create_timer(0.01, self.read_joystick)
        except Exception as e:
            self.get_logger().error(f'Could not connect to joystick: {e}')

    def find_device_path(self):
        base_path = '/dev/input/by-id/'
        devices = os.listdir(base_path)
        for device in devices:
            if 'Logitech' in device and 'event' in device:
                return os.path.join(base_path, device)
        raise Exception('Joystick not found')

    def read_joystick(self):
        try:
            for event in self.gamepad.read_loop():
                if event.type == ecodes.EV_KEY or event.type == ecodes.EV_ABS:
                    msg = Joy()
                    msg.header.stamp = self.get_clock().now().to_msg()
                    msg.axes = [0.0] * 8
                    msg.buttons = [0] * 12

                    if event.type == ecodes.EV_ABS:
                        if event.code == ecodes.ABS_X:
                            msg.axes[0] = event.value / self.normalization_factor
                        elif event.code == ecodes.ABS_Y:
                            msg.axes[1] = event.value / self.normalization_factor
                        elif event.code == ecodes.ABS_Z:
                            msg.axes[2] = event.value / self.normalization_factor
                        elif event.code == ecodes.ABS_RX:
                            msg.axes[3] = event.value / self.normalization_factor
                        elif event.code == ecodes.ABS_RY:
                            msg.axes[4] = event.value / self.normalization_factor
                        elif event.code == ecodes.ABS_RZ:
                            msg.axes[5] = event.value / self.normalization_factor
                        elif event.code == ecodes.ABS_HAT0X:
                            msg.axes[6] = event.value / self.normalization_factor
                        elif event.code == ecodes.ABS_HAT0Y:
                            msg.axes[7] = event.value / self.normalization_factor

                    if event.type == ecodes.EV_KEY:
                        if event.code == ecodes.BTN_A:
                            msg.buttons[0] = event.value
                        elif event.code == ecodes.BTN_B:
                            msg.buttons[1] = event.value
                        elif event.code == ecodes.BTN_X:
                            msg.buttons[2] = event.value
                        elif event.code == ecodes.BTN_Y:
                            msg.buttons[3] = event.value
                        elif event.code == ecodes.BTN_TL:
                            msg.buttons[4] = event.value
                        elif event.code == ecodes.BTN_TR:
                            msg.buttons[5] = event.value
                        elif event.code == ecodes.BTN_SELECT:
                            msg.buttons[6] = event.value
                        elif event.code == ecodes.BTN_START:
                            msg.buttons[7] = event.value
                        elif event.code == ecodes.BTN_MODE:
                            msg.buttons[8] = event.value
                        elif event.code == ecodes.BTN_THUMBL:
                            msg.buttons[9] = event.value
                        elif event.code == ecodes.BTN_THUMBR:
                            msg.buttons[10] = event.value
                        elif event.code == ecodes.BTN_TRIGGER_HAPPY1:
                            msg.buttons[11] = event.value

                    self.publisher_.publish(msg)
        except Exception as e:
            self.get_logger().error(f'Error reading joystick: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = JoystickNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
