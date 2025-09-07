# --- 필수 라이브러리 설치 안내 ---
# 이 코드를 실행하기 전에 아래 명령어를 터미널에 입력하여 필요한 라이브러리를 설치하세요.
# pip install pyautogui
# pip install Pillow
# pip install opencv-python
# pip install ultralytics
# pip install pynput
# pip install tk
# pip install pydirectinput

import pyautogui
import pydirectinput
import cv2
import numpy as np
import time
from ultralytics import YOLO
import tkinter as tk
from pynput.mouse import Listener
import threading
import math # 거리 계산을 위해 math 모듈 추가

# 드래그 시작점과 끝점 좌표를 저장할 전역 변수
start_x, start_y = None, None
end_x, end_y = None, None

# Tkinter 윈도우와 캔버스 객체를 저장할 변수
root = None
canvas = None
listener_thread = None
REGION_COORDS = None

def on_click(x, y, button, pressed):
    """마우스 클릭 이벤트를 처리하고 Tkinter 창에 드래그 영역을 표시합니다."""
    global start_x, start_y, end_x, end_y, REGION_COORDS
    if button == button.left:
        if pressed:
            # 마우스 왼쪽 버튼을 누른 순간 (드래그 시작)
            start_x, start_y = x, y
            root.deiconify()  # 창을 보이게 함
            canvas.delete("rect")  # 기존 사각형 삭제
            print(f"드래그 시작 좌표: ({start_x}, {start_y})")
        else:
            # 마우스 왼쪽 버튼을 놓는 순간 (드래그 끝)
            end_x, end_y = x, y
            print(f"드래그 종료 좌표: ({end_x}, {end_y})")
            
            # 드래그 방향에 상관없이 올바른 좌표 계산
            left = min(start_x, end_x)
            top = min(start_y, end_y)
            width = abs(start_x - end_x)
            height = abs(start_y - end_y)
            REGION_COORDS = (left, top, width, height)
            
            root.destroy()  # Tkinter 윈도우 완전 종료
            return False

def on_move(x, y):
    """마우스 이동 이벤트를 처리하여 드래그 영역을 실시간으로 그립니다."""
    if start_x is not None:
        canvas.delete("rect")
        
        # 드래그 방향에 상관없이 올바른 사각형을 그리기 위한 좌표 계산
        rect_x1 = min(start_x, x)
        rect_y1 = min(start_y, y)
        rect_x2 = max(start_x, x)
        rect_y2 = max(start_y, y)
        
        canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, 
                                outline="blue", tags="rect", width=2)
        root.update_idletasks() # 화면을 즉시 업데이트

def start_listener_thread():
    """pynput 리스너를 별도의 스레드로 시작합니다."""
    with Listener(on_click=on_click, on_move=on_move) as listener:
        listener.join()
        
def get_region_from_drag():
    """마우스 드래그로 캡처 영역을 지정하고 값을 반환합니다."""
    global root, canvas, listener_thread
    
    # Tkinter 윈도우 생성
    root = tk.Tk()
    root.attributes("-alpha", 0.3)  # 투명도 설정
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.overrideredirect(True) # 윈도우 테두리 제거
    root.withdraw() # 초기에는 창을 숨김

    canvas = tk.Canvas(root, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    # 리스너 스레드 시작
    listener_thread = threading.Thread(target=start_listener_thread)
    listener_thread.daemon = True
    listener_thread.start()

    # Tkinter 이벤트 루프 시작
    root.mainloop()
    
    return REGION_COORDS

def capture_screen():
    """
    마우스 드래그로 지정된 영역을 캡처하여 NumPy 배열로 반환합니다.
    """
    if REGION_COORDS:
        screen = pyautogui.screenshot(region=REGION_COORDS)
        return np.array(screen)
    return None

def calculate_distance(p1, p2):
    """
    두 점 (x1, y1)와 (x2, y2)를 사용하여 유클리드 거리를 계산합니다.
    """
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def main():
    """
    메인 실행 함수: YOLO 모델을 이용해 실시간으로 객체를 탐지하고 버프 로직을 실행합니다.
    """
    print("--- 딥러닝 기반 객체 인식 시작 ---")
    print("마우스 드래그로 캡처할 영역을 지정하세요.")
    
    global REGION_COORDS
    REGION_COORDS = get_region_from_drag()
    print(f"\n선택된 캡처 영역: {REGION_COORDS}")
    
    if not REGION_COORDS:
        print("캡처 영역이 지정되지 않아 프로그램을 종료합니다.")
        return

    # 1. 학습된 모델 로드
    model_path = "yolo_project\\Game_Macro\\companion_try2\\weights\\best.pt"  # 사용자 모델 경로
    model = YOLO(model_path)
    
    # 2. 클래스 이름 정의
    MY_CHARACTER_CLASS = "Mycharactor"
    ALLY_CHARACTER_CLASS = "companion"

    # 버프를 제공할 최소 거리 설정 (픽셀 단위)
    BUFF_DISTANCE_THRESHOLD = 120
    # 버프 스킬의 재사용 대기 시간 (초 단위)
    BUFF_COOLDOWN = 15
    # 마지막으로 버프를 사용한 시간
    last_buff_time = 0

    while True:
        try:
            # 3. 화면 캡처
            screen_image = capture_screen()
            if screen_image is None:
                break

            # 4. 모델 추론 (Inference)
            results = model(screen_image, verbose=False, stream=True)
            
            my_char_locs = []
            ally_char_locs = []
            
            display_image = np.array(screen_image)

            for result in results:
                # 5. 탐지 결과 추출
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]
                    confidence = float(box.conf[0])
                    
                    # 6. 신뢰도(Confidence) 설정
                    if confidence > 0.45:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        
                        # 7. 캐릭터 분류 및 좌표 저장
                        if class_name == MY_CHARACTER_CLASS:
                            my_char_locs.append(((x1 + x2) / 2, (y1 + y2) / 2))
                            cv2.rectangle(display_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(display_image, f'{class_name} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        elif class_name == ALLY_CHARACTER_CLASS:
                            ally_char_locs.append(((x1 + x2) / 2, (y1 + y2) / 2))
                            cv2.rectangle(display_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                            cv2.putText(display_image, f'{class_name} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                    
            # 8. 버프 제공 로직 추가
            current_time = time.time()
            remaining_cooldown = BUFF_COOLDOWN - (current_time - last_buff_time)
            
            if my_char_locs and ally_char_locs:
                # 버프 재사용 대기 시간이 지났는지 확인
                if remaining_cooldown <= 0:
                    # 첫 번째로 인식된 내 캐릭터의 위치를 기준으로 삼습니다.
                    my_char_pos = my_char_locs[0]

                    for ally_pos in ally_char_locs:
                        # 내 캐릭터와 동료 캐릭터 간의 거리를 계산합니다.
                        distance = calculate_distance(my_char_pos, ally_pos)

                        # 거리가 버프 제공 조건보다 가까운지 확인합니다.
                        if distance < BUFF_DISTANCE_THRESHOLD:
                            print(f"동료 캐릭터가 가까이 있습니다. 버프를 제공합니다! (거리: {distance:.2f})")
                            
                            # C++ 연동 또는 WinAPI를 사용한 버프 제공 키 입력
                            print("C 키를 눌렀습니다.")
                            pydirectinput.keyDown('c')
                            time.sleep(0.1) # 키를 누른 상태 유지
                            pydirectinput.keyUp('c')

                            last_buff_time = current_time # 마지막으로 버프를 사용한 시간 업데이트
                            # 버프가 한 번 제공되면 더 이상 순회할 필요 없으므로 break
                            break
                else:
                    # 버프 재사용 대기 중일 때 메시지 출력
                    formatted_time = time.strftime('%M:%S', time.gmtime(remaining_cooldown))
                    print(f"버프 재사용 대기 중입니다. 남은 시간: {formatted_time}")
            else:
                # 캐릭터를 찾을 수 없을 때
                if remaining_cooldown > 0:
                    formatted_time = time.strftime('%M:%S', time.gmtime(remaining_cooldown))
                    print(f"동료 캐릭터를 찾을 수 없습니다. (버프 쿨타임 남은 시간: {formatted_time})")
                else:
                    print("동료 캐릭터를 찾을 수 없습니다.")

            # 9. 화면에 결과 표시
            cv2.imshow('Object Detection', display_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\n매크로를 종료합니다.")
            break
        except Exception as e:
            print(f"오류 발생: {e}")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
