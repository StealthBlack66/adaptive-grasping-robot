#!/usr/bin/env python3
"""
motion_pkg - moveit_node.py
담당: 임현찬
역할: 파지 위치 수신 → MoveIt2로 경로 계획 → E0509 이동

[할 일]
1. 파지 위치 구독 (/grasp_pose)
2. MoveIt2로 충돌 회피 경로 계획
3. E0509 로봇암 이동 실행
4. 완료 후 main_pkg에 알림

[주의]
- 토픽 이름 바꾸지 말 것
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from trajectory_msgs.msg import JointTrajectory

class MoveitNode(Node):
    def __init__(self):
        super().__init__('moveit_node')

        # ========================
        # 구독자 (받는 것)
        # ========================
        self.pose_sub = self.create_subscription(
            Pose,
            '/grasp_pose',        # ← grasp_pkg에서 보내는 토픽
            self.pose_callback,
            10
        )

        # ========================
        # 발행자 (보내는 것) - 수정 금지
        # ========================
        self.traj_pub = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory',  # ← 이름 바꾸지 말 것
            10
        )

        self.get_logger().info('MoveitNode 시작')

    def pose_callback(self, msg: Pose):
        """
        파지 위치가 들어올 때 실행
        여기에 MoveIt2 경로 계획 코드 작성
        """
        self.get_logger().info(
            f'파지 위치 수신: x={msg.position.x:.3f}, '
            f'y={msg.position.y:.3f}, z={msg.position.z:.3f}'
        )

        # TODO: MoveIt2 MoveGroupInterface 설정
        # TODO: 목표 위치 설정
        # TODO: plan() 호출
        # TODO: execute() 호출
        # TODO: publish_trajectory() 호출

        pass

    def publish_trajectory(self, trajectory: JointTrajectory):
        """
        계획된 경로 발행
        """
        self.traj_pub.publish(trajectory)
        self.get_logger().info('경로 계획 완료 → main_pkg로 전달')


def main(args=None):
    rclpy.init(args=args)
    node = MoveitNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
