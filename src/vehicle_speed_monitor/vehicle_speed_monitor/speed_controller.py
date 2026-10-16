
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import Float32

from vehicle_speed_interfaces.action import ReachSpeed


class SpeedController(Node):

    def __init__(self):
        super().__init__('speed_controller')

        self.current_speed = 0.0

        # Separate callback groups allow concurrent execution
        self.sensor_group = ReentrantCallbackGroup()
        self.action_group = ReentrantCallbackGroup()

        # Receive measured speed from the sensor
        self.speed_subscriber = self.create_subscription(
            Float32,
            '/vehicle/speed',
            self.speed_callback,
            10,
            callback_group=self.sensor_group
        )

        # Send target speed to the vehicle model
        self.target_publisher = self.create_publisher(
            Float32,
            '/vehicle/target_speed',
            10
        )

        # Create the action server
        self.action_server = ActionServer(
            self,
            ReachSpeed,
            'reach_speed',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            callback_group=self.action_group
        )

        self.get_logger().info('Speed controller ready.')

    def speed_callback(self, msg):
        self.current_speed = msg.data

    def goal_callback(self, goal_request):
        target = goal_request.target_speed

        if 0.0 <= target <= 60.0:
            self.get_logger().info(
                f'Accepted target: {target:.1f} km/h'
            )
            return GoalResponse.ACCEPT

        self.get_logger().warn('Target must be between 0 and 60 km/h.')
        return GoalResponse.REJECT

    def execute_callback(self, goal_handle):
        target = goal_handle.request.target_speed

        command = Float32()
        command.data = target
        self.target_publisher.publish(command)

        feedback = ReachSpeed.Feedback()

        self.get_logger().info(f'Trying to reach {target:.1f} km/h.')

        while abs(self.current_speed - target) > 0.5:
            if goal_handle.is_cancel_requested:
                stop_command = Float32()
                stop_command.data = self.current_speed
                self.target_publisher.publish(stop_command)

                goal_handle.canceled()

                result = ReachSpeed.Result()
                result.success = False
                result.message = 'Goal cancelled.'
                return result

            feedback.current_speed = self.current_speed
            goal_handle.publish_feedback(feedback)

            time.sleep(0.5)

        goal_handle.succeed()

        result = ReachSpeed.Result()
        result.success = True
        result.message = f'Target speed of {target:.1f} km/h reached.'

        self.get_logger().info(result.message)
        return result


def main(args=None):
    rclpy.init(args=args)
    node = SpeedController()

    executor = MultiThreadedExecutor(num_threads=3)
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
