
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class VehicleModel(Node):

    def __init__(self):
        super().__init__('vehicle_model')

        self.speed = 0.0
        self.target_speed = 0.0

        # Publishes the simulated vehicle's true speed
        self.speed_publisher = self.create_publisher(
            Float32,
            '/vehicle/true_speed',
            10
        )

        # Receives the target speed from the controller
        self.target_subscriber = self.create_subscription(
            Float32,
            '/vehicle/target_speed',
            self.target_speed_callback,
            10
        )

        # Updates the simulated vehicle once per second
        self.timer = self.create_timer(1.0, self.update_vehicle)

        self.get_logger().info('Vehicle model started.')

    def target_speed_callback(self, msg):
        self.target_speed = max(0.0, min(60.0, msg.data))
        self.get_logger().info(
            f'New target speed: {self.target_speed:.1f} km/h'
        )

    def update_vehicle(self):
        # Simplified model: change speed by at most 2 km/h per second
        step = 2.0

        if self.speed < self.target_speed:
            self.speed = min(self.speed + step, self.target_speed)
        elif self.speed > self.target_speed:
            self.speed = max(self.speed - step, self.target_speed)

        msg = Float32()
        msg.data = self.speed
        self.speed_publisher.publish(msg)

        self.get_logger().info(
            f'Vehicle true speed: {self.speed:.1f} km/h'
        )


def main(args=None):
    rclpy.init(args=args)
    node = VehicleModel()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
