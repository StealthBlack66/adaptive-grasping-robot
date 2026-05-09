#!/usr/bin/env python3
"""
main_pkg - main_node.py
담당: 심예영
역할: 전체 파이프라인 통합 및 흐름 제어

[역할]
1. 각 노드의 결과를 받아서 다음 단계 트리거
2. 전체 상태 관리 (대기 / 인식 / 파지 / 완료)
3. 그리퍼 최종 명령 발행
4. 예외 처리 (인식 실패, 파지 실패 등)

[주의]
- 토픽 이름 바꾸지 말 것
- 각 노드 상태를 모니터링하는 것이 핵심
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32
from geometry_msgs.msg import Pose
from trajectory_msgs.msg import JointTrajectory

# ========================
# 시스템 상태 정의
# ========================
class State:
    IDLE        = 'idle'        # 대기
    DETECTING   = 'detecting'   # 물체 인식 중
    PLANNING    = 'planning'    # 경로 계획 중
    GRASPING    = 'grasping'    # 파지 중
    DONE        = 'done'        # 완료
    ERROR       = 'error'       # 오류


class MainNode(Node):
    def __init__(self):
        super().__init__('main_node')

        self.state = State.IDLE
        self.current_class = None
        self.grasp_pose = None

        # ========================
        # 구독자 (각 노드 결과 받기)
        # ========================
        self.class_sub = self.create_subscription(
            String,
            '/object_class',
            self.class_callback,
            10
        )
        self.pose_sub = self.create_subscription(
            Pose,
            '/grasp_pose',
            self.pose_callback,
            10
        )
        self.traj_sub = self.create_subscription(
            JointTrajectory,
            '/joint_trajectory',
            self.trajectory_callback,
            10
        )

        # ========================
        # 발행자 - 수정 금지
        # ========================
        self.gripper_pub = self.create_publisher(
            Int32,
            '/gripper_cmd',  # ← 이름 바꾸지 말 것
            10
        )

        # 상태 출력 타이머 (1초마다)
        self.create_timer(1.0, self.print_state)

        self.get_logger().info('MainNode 시작 - 전체 파이프라인 준비 완료')

    def class_callback(self, msg: String):
        """
        물체 재질 수신 → 상태 업데이트
        """
        self.current_class = msg.data
        self.state = State.PLANNING
        self.get_logger().info(f'[상태: {self.state}] 물체 재질: {self.current_class}')

    def pose_callback(self, msg: Pose):
        """
        파지 위치 수신
        """
        self.grasp_pose = msg
        self.get_logger().info(
            f'[상태: {self.state}] 파지 위치 수신: '
            f'x={msg.position.x:.3f}, y={msg.position.y:.3f}, z={msg.position.z:.3f}'
        )

    def trajectory_callback(self, msg: JointTrajectory):
        """
        경로 계획 완료 수신 → 그리퍼 명령 발행
        """
        self.state = State.GRASPING
        self.get_logger().info(f'[상태: {self.state}] 경로 계획 완료 → 그리퍼 명령 발행')

        # TODO: 그리퍼 명령 발행
        # self.send_gripper_cmd(target_current)

    def send_gripper_cmd(self, current_ma: int):
        """
        그리퍼에 전류값 명령 발행
        current_ma: 목표 전류값 (mA)
        """
        msg = Int32()
        msg.data = current_ma
        self.gripper_pub.publish(msg)
        self.get_logger().info(f'그리퍼 명령: {current_ma} mA')

    def print_state(self):
        """
        현재 시스템 상태 출력 (디버깅용)
        """
        self.get_logger().info(
            f'[시스템 상태] {self.state} | '
            f'물체: {self.current_class}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = MainNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
