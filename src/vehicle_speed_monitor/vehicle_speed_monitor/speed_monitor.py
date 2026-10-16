import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class SpeedMonitor(Node):

    def __init__(self):
        super().__init__('speed_monitor')

        self.subscription = self.create_subscription(
            Float32,
            '/vehicle/speed',
            self.speed_callback,
            10
        )

    def speed_callback(self, msg):
        self.get_logger().info(
            f'Received speed: {msg.data} km/h'
        )


def main(args=None):
    rclpy.init(args=args)

    node = SpeedMonitor()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()