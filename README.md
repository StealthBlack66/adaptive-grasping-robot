# 물성 기반 적응형 파지 로봇
**Hardness-Aware Adaptive Grasping with ROS2 + E0509**

![ROS2](https://img.shields.io/badge/ROS2-Humble-blue)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-purple)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 개요

카메라로 물체의 재질(딱딱함/중간/말랑)을 인식하고,  
그리퍼의 **전류 임계값(mA)** 을 물성에 맞게 설정하여 물체를 파지하는 협동 로봇 시스템.

> "단순히 집는 것이 아니라, 물체의 물성을 판단하여 최적의 힘으로 파지한다."

## 🎯 파지 목적

| 물체 | 문제 | 해결 |
|---|---|---|
| **말랑한 물체** (A4용지) | 너무 세게 잡으면 찌그러짐 | 낮은 전류 임계값으로 약하게 파지 |
| **딱딱한 물체** (나무) | 너무 약하게 잡으면 미끄러져 떨어짐 | 높은 전류 임계값으로 강하게 파지 |

→ 물성에 따라 **찌그러지지 않으면서도 미끄러지지 않는** 적절한 힘으로 파지하는 것이 목표.

---

## 🎯 핵심 기술

| 기술 | 설명 |
|---|---|
| **Adaptive Grasping** | 물성별 전류 임계값 기반 그립 힘 조절 |
| **YOLOv8** | 카메라 이미지에서 물체 재질 분류 |
| **Current-based Control** | DYNAMIXEL RH-P12-RN-A 전류 피드백 제어 |
| **ROS2** | 노드 간 통신 및 전체 파이프라인 관리 |

---

## 🤖 하드웨어

- **로봇암**: Doosan Robotics E0509
- **그리퍼**: ROBOTIS RH-P12-RN-A
- **카메라**: RGB 카메라 (상단 고정)
- **실험 물체**: 나무 / 매직스펀지 / A4 용지 (20×20×20mm 정육면체)

---

## 🏗️ 시스템 아키텍처

```
[Camera]
    │ /image_raw
    ▼
[YOLOv8 Node]  ──→  물체 재질 분류 (hard / medium / soft)
    │ /object_class
    ▼
[판단 노드]  ──→  전류 임계값 결정 (mA)
    │ /target_current
    │ /grasp_pose
    ▼
[MoveIt2]  ──→  경로 계획 + Collision Avoidance
    │ /joint_trajectory
    ▼
[E0509]  ──→  로봇암 이동
    │ /gripper_cmd
    ▼
[RH-P12-RN-A]  ──→  Adaptive Grasping
    │ /present_current (피드백)
    ▼
파지 성공 판단 → 임계값 초과 시 멈춤
```

---

## 📊 전류 임계값 (실험 결과)

| 물체 | 경도 | 전류 임계값 |
|---|---|---|
| 나무 블록 | Hard | TBD mA |
| 매직스펀지 | Medium | TBD mA |
| A4 용지 | Soft | TBD mA |

> 실험 방법: 물체별로 그리퍼를 닫으면서 `Present Current(621)` 레지스터 실시간 모니터링

---

## 📁 패키지 구조

```
adaptive-grasping-robot/
├── src/
│   ├── vision_pkg/          # YOLOv8 인식 노드
│   │   ├── yolo_node.py
│   │   └── coord_transform.py
│   ├── grasp_pkg/           # 물성 판단 + 전류 제어
│   │   ├── hardness_node.py
│   │   └── gripper_control.py
│   ├── motion_pkg/          # MoveIt2 경로 계획
│   │   └── moveit_node.py
│   └── main_pkg/            # 전체 파이프라인 통합
│       └── main_node.py
├── config/
│   └── current_threshold.yaml   # 전류 임계값 설정
├── launch/
│   └── grasping.launch.py
└── README.md
```

---

## 🚀 실행 방법

```bash
# 1. 시뮬레이션 실행
ros2 launch e0509_gripper_description bringup.launch.py mode:=virtual

# 2. 전체 파이프라인 실행
ros2 launch main_pkg grasping.launch.py

# 3. 개별 노드 실행
ros2 run vision_pkg yolo_node
ros2 run grasp_pkg hardness_node
ros2 run motion_pkg moveit_node
```

---

## 📅 개발 일정

| 주차 | 내용 |
|---|---|
| 1주차 | YOLOv8 데이터셋 준비 + 파인튜닝, 카메라 캘리브레이션 |
| 2주차 | 전류 임계값 실험, 파이프라인 통합 |
| 3주차 | 통합 테스트, 예외 처리, 시연 영상 촬영 |

---

## 👥 팀원

| 이름 | 역할 |
|---|---|
| - | 카메라 + YOLOv8 인식 |
| - | 물성 판단 + 전류 임계값 실험 |
| - | MoveIt2 경로 계획 |
| - | 전체 통합 + ROS2 파이프라인 |

---

## 🔮 향후 과제

- Collision Avoidance 고도화 (박스 내 겹친 물체 처리)
- VLA(Vision-Language-Action) 기반 제어로 확장
- 실리콘 경도 세분화 (3단계 → 5단계)

---

## 📚 참고

- [ROBOTIS RH-P12-RN-A e-Manual](https://emanual.robotis.com/docs/en/platform/rh_p12_rna/)
- [Doosan Robotics E0509](https://www.doosanrobotics.com)
- [YOLOv8 Ultralytics](https://github.com/ultralytics/ultralytics)
- [MoveIt2](https://moveit.ros.org)
