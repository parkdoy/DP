from ultralytics import YOLO
import os

# 필수 라이브러리 설치
# pip install ultralytics

# 'dataset.yaml' 파일 경로를 지정합니다.
data_yaml = 'dataset.yaml'

# 미리 학습된 YOLOv8 모델을 로드합니다.
# 처음 실행 시 자동으로 다운로드됩니다.
model = YOLO('yolov8n.pt')

# 모델 학습
# data: 데이터 설정 파일 경로
# epochs: 학습 반복 횟수. 많을수록 정확해지지만, 과적합 위험이 있습니다.
# imgsz: 이미지 크기. 숫자를 늘리면 정확도가 높아지지만, 학습 속도가 느려집니다.
results = model.train(data=data_yaml, epochs=50, imgsz=640, project='Game_Macro', name='companion_try', exist_ok=True)

# 학습된 모델은 'runs/detect/train/weights/best.pt'에 저장됩니다.
print("\n모델 학습이 완료되었습니다. 결과는 'Game_Macro/' 폴더에 저장됩니다.")
print("최종 모델 파일: 'companion_try.pt'")
