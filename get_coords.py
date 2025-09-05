import pyautogui
import time

print("마우스 커서를 게임 창의 좌측 상단 모서리에 올려놓으세요. 5초 뒤에 현재 좌표를 표시합니다.")
time.sleep(5)
x1, y1 = pyautogui.position()
print(f"좌측 상단 좌표: x={x1}, y={y1}")

print("\n마우스 커서를 게임 창의 우측 하단 모서리에 올려놓으세요. 5초 뒤에 현재 좌표를 표시합니다.")
time.sleep(5)
x2, y2 = pyautogui.position()
print(f"우측 하단 좌표: x={x2}, y={y2}")

# 너비와 높이 계산
width = x2 - x1
height = y2 - y1

print("\n--- 결과 ---")
print(f"좌표: ({x1}, {y1})")
print(f"너비: {width}, 높이: {height}")
print(f"region 값: ({x1}, {y1}, {width}, {height})")
