#!/usr/bin/env python3
"""
grasp_pkg - hardness_node.py
담당: 남상훈
역할: 물성 판단 → 전류 임계값 결정 → 그리퍼 제어

[할 일]
1. 물체 재질 구독 (/object_class)
2. 재질에 따른 전류 임계값 결정
3. 그리퍼 닫으면서 전류 모니터링
4. 임계값 초과 시 그리퍼 멈춤

[주의]
- 전류 임계값은 실험 후 CURRENT_THRESHOLD에 직접 입력
- 토픽 이름 바꾸지 말 것
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32

# ========================
# 전류 임계값 설정 (실험 후 채워넣기)
# 단위: mA (밀리암페어)
# ========================
CURRENT_THRESHOLD = {
    'hard':   0,    # TODO: 나무 실험 후 입력
    'medium': 0,    # TODO: 실리콘 A50 실험 후 입력
    'soft':   0,    # TODO: 실리콘 A20 실험 후 입력
}

class HardnessNode(Node):
    def __init__(self):
        super().__init__('hardness_node')

        self.current_class = None  # 현재 물체 재질

        # ========================
        # 구독자 (받는 것)
        # ========================
        self.class_sub = self.create_subscription(
            String,
            '/object_class',   # ← vision_pkg에서 보내는 토픽
            self.class_callback,
            10
        )

        # ========================
        # 발행자 (보내는 것) - 수정 금지
        # ========================
        self.current_pub = self.create_publisher(
            Int32,
            '/target_current',  # ← 이름 바꾸지 말 것
            10
        )
        self.gripper_pub = self.create_publisher(
            Int32,
            '/gripper_cmd',     # ← 이름 바꾸지 말 것
            10
        )

        self.get_logger().info('HardnessNode 시작')

    def class_callback(self, msg: String):
        """
        물체 재질이 들어올 때 실행
        """
        self.current_class = msg.data
        self.get_logger().info(f'물체 재질 수신: {self.current_class}')

        # 전류 임계값 결정 및 발행
        threshold = self.get_threshold(self.current_class)
        self.publish_target_current(threshold)

    def get_threshold(self, class_name: str) -> int:
        """
        재질에 따른 전류 임계값 반환
        """
        if class_name not in CURRENT_THRESHOLD:
            self.get_logger().warn(f'알 수 없는 재질: {class_name}')
            return 0
        return CURRENT_THRESHOLD[class_name]

    def publish_target_current(self, threshold: int):
        """
        전류 임계값 발행
        """
        msg = Int32()
        msg.data = threshold
        self.current_pub.publish(msg)
        self.get_logger().info(f'전류 임계값 설정: {threshold} mA')

    def monitor_and_stop(self, present_current: int):
        """
        현재 전류값이 임계값 초과 시 그리퍼 멈춤
        DYNAMIXEL SDK로 present_current 읽어서 이 함수 호출
        """
        threshold = self.get_threshold(self.current_class)
        if present_current >= threshold:
            self.get_logger().info(
                f'임계값 도달: {present_current} mA >= {threshold} mA → 그리퍼 멈춤'
            )
            self.stop_gripper()

    def stop_gripper(self):
        """
        그리퍼 정지 명령
        """
        # TODO: 그리퍼 멈추는 로직 구현
        pass


def main(args=None):
    rclpy.init(args=args)
    node = HardnessNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
