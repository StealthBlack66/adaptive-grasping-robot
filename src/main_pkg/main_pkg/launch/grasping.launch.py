"""
grasping.launch.py
전체 파이프라인을 한 번에 실행하는 런치 파일

실행 방법:
    ros2 launch main_pkg grasping.launch.py
    ros2 launch main_pkg grasping.launch.py mode:=virtual  # 시뮬레이션
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    # ========================
    # 인자 선언
    # ========================
    mode_arg = DeclareLaunchArgument(
        'mode',
        default_value='virtual',
        description='실행 모드: virtual(시뮬레이션) / real(실로봇)'
    )

    # ========================
    # E0509 시뮬레이션 런치 포함
    # ========================
    e0509_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('e0509_gripper_description'),
                'launch',
                'bringup.launch.py'
            )
        ]),
        launch_arguments={'mode': LaunchConfiguration('mode')}.items()
    )

    # ========================
    # 1번: YOLOv8 인식 노드 (이현호)
    # ========================
    yolo_node = Node(
        package='vision_pkg',
        executable='yolo_node',
        name='yolo_node',
        output='screen',
        parameters=[{
            'model_path': 'best.pt',  # TODO: 이현호가 학습한 모델 경로
        }]
    )

    # ========================
    # 2번: 물성 판단 + 전류 제어 노드 (남상훈)
    # ========================
    hardness_node = Node(
        package='grasp_pkg',
        executable='hardness_node',
        name='hardness_node',
        output='screen',
    )

    # ========================
    # 3번: MoveIt2 경로 계획 노드 (임현찬)
    # ========================
    moveit_node = Node(
        package='motion_pkg',
        executable='moveit_node',
        name='moveit_node',
        output='screen',
    )

    # ========================
    # 4번: 통합 메인 노드 (심예영)
    # ========================
    main_node = Node(
        package='main_pkg',
        executable='main_node',
        name='main_node',
        output='screen',
    )

    return LaunchDescription([
        mode_arg,
        e0509_launch,
        yolo_node,
        hardness_node,
        moveit_node,
        main_node,
    ])
