import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class Subscriber(Node):
    def __init__(self):
        super().__init__('subscriber')
        self.subscriber_ = self.create_subscription(String, 'topic', self.listener_callback, 10)

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    subscriber = Subscriber()
    rclpy.spin(subscriber)
    subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
