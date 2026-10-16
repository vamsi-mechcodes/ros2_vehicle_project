import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class SpeedSensor(Node):

    def __init__(self):
        super().__init__('speed_sensor')

        self.sensor_subscription = self.create_subscription(
            Float32,
            '/vehicle/true_speed',
            self.speed_callback,
            10
        )

        self.publisher = self.create_publisher(
            Float32,
            '/vehicle/speed',
            10
        )

    def speed_callback(self, message):
        measured_speed = Float32()
        measured_speed.data = message.data

        self.publisher.publish(measured_speed)

        self.get_logger().info(
            f'Measured vehicle speed: {measured_speed.data} km/h'
        )


def main(args=None):
    rclpy.init(args=args)
    node = SpeedSensor()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()