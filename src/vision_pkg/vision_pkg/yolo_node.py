#!/usr/bin/env python3
"""
vision_pkg - yolo_node.py
담당: 이현호
역할: 카메라 이미지 구독 → YOLOv8 물체 인식 → 재질 분류 결과 발행

[할 일]
1. 카메라 이미지 구독 (/image_raw)
2. YOLOv8 모델 로드 및 추론
3. 물체 재질 분류 결과 발행 (/object_class)
4. 물체 위치(픽셀 좌표) → 로봇 좌표계 변환 후 발행 (/grasp_pose)

[주의]
- /object_class 값은 반드시 "hard" / "medium" / "soft" 만 사용
- 토픽 이름 바꾸지 말 것
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from geometry_msgs.msg import Pose

class YoloNode(Node):
    def __init__(self):
        super().__init__('yolo_node')

        # ========================
        # 구독자 (받는 것)
        # ========================
        self.image_sub = self.create_subscription(
            Image,
            '/image_raw',
            self.image_callback,
            10
        )

        # ========================
        # 발행자 (보내는 것) - 수정 금지
        # ========================
        self.class_pub = self.create_publisher(
            String,
            '/object_class',  # ← 이름 바꾸지 말 것
            10
        )
        self.pose_pub = self.create_publisher(
            Pose,
            '/grasp_pose',    # ← 이름 바꾸지 말 것
            10
        )

        self.get_logger().info('YoloNode 시작')

    def image_callback(self, msg: Image):
        """
        카메라 이미지가 들어올 때마다 실행되는 함수
        여기에 YOLOv8 추론 코드 작성
        """
        # TODO: 이미지 → numpy 변환
        # TODO: YOLOv8 추론
        # TODO: 결과에 따라 "hard" / "medium" / "soft" 결정
        # TODO: publish_class() 호출

        pass

    def publish_class(self, class_name: str):
        """
        물체 재질 분류 결과 발행
        class_name: "hard" / "medium" / "soft" 중 하나
        """
        assert class_name in ['hard', 'medium', 'soft'], \
            f"잘못된 class_name: {class_name}"

        msg = String()
        msg.data = class_name
        self.class_pub.publish(msg)
        self.get_logger().info(f'물체 인식: {class_name}')

    def publish_pose(self, x: float, y: float, z: float):
        """
        물체 파지 위치(로봇 좌표계) 발행
        x, y, z: 미터 단위
        """
        msg = Pose()
        msg.position.x = x
        msg.position.y = y
        msg.position.z = z
        self.pose_pub.publish(msg)
        self.get_logger().info(f'파지 위치: x={x:.3f}, y={y:.3f}, z={z:.3f}')


def main(args=None):
    rclpy.init(args=args)
    node = YoloNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
