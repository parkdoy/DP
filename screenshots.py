# --- 필수 라이브러리 설치 안내 ---
# 이 코드를 실행하기 전에 아래 명령어를 터미널에 입력하여 필요한 라이브러리를 설치하세요.
# pip install pyautogui
# pip install Pillow
# pip install pynput

import pyautogui
import time
import os
import tkinter as tk
from pynput.mouse import Listener
import threading

# 드래그 시작점과 끝점 좌표를 저장할 전역 변수
start_x, start_y = None, None
end_x, end_y = None, None

# Tkinter 윈도우와 캔버스 객체를 저장할 변수
root = None
canvas = None

# 리스너 스레드 중단 플래그
listener_thread = None

def on_click(x, y, button, pressed):
    """마우스 클릭 이벤트를 처리하고 Tkinter 창에 드래그 영역을 표시합니다."""
    global start_x, start_y, end_x, end_y
    if button == button.left:
        if pressed:
            # 마우스 왼쪽 버튼을 누른 순간 (드래그 시작)
            start_x, start_y = x, y
            root.deiconify() # 창을 보이게 함
            canvas.delete("rect") # 기존 사각형 삭제
            print(f"드래그 시작 좌표: ({start_x}, {start_y})")
        else:
            # 마우스 왼쪽 버튼을 놓는 순간 (드래그 끝)
            end_x, end_y = x, y
            print(f"드래그 종료 좌표: ({end_x}, {end_y})")
            root.destroy() # Tkinter 윈도우 완전 종료
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
    root.attributes("-alpha", 0.3) # 투명도 설정
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
    
    # 드래그 방향에 상관없이 올바른 좌표 계산
    left = min(start_x, end_x)
    top = min(start_y, end_y)
    width = abs(start_x - end_x)
    height = abs(start_y - end_y)
    
    return (left, top, width, height)

# 스크린샷을 저장할 폴더를 지정합니다.
output_folder = "game_screenshots"
os.makedirs(output_folder, exist_ok=True)

# 캡처할 스크린샷 개수와 간격을 설정합니다.
num_screenshots = 500
capture_interval_seconds = 5

if __name__ == "__main__":
    print("스크린샷 캡처 프로그램을 시작합니다. 마우스 드래그로 캡처할 영역을 지정하세요.")
    
    # 캡처할 화면 영역을 드래그로 지정
    REGION_COORDS = get_region_from_drag()
    print(f"\n선택된 캡처 영역: {REGION_COORDS}")

    print(f"\n{num_screenshots}개의 스크린샷을 {capture_interval_seconds}초마다 캡처합니다. 3초 후 시작됩니다.")
    time.sleep(3)

    for i in range(num_screenshots):
        try:
            # 지정된 영역만 캡처합니다.
            screenshot = pyautogui.screenshot(region=REGION_COORDS)
            
            # 파일명을 'screenshot_001.png' 형식으로 저장합니다. companion / monster / Mycharactor / magatia
            file_path = os.path.join(output_folder, f"screenshot_{i+1:03d}.png")
            screenshot.save(file_path)
            
            print(f"{i+1}/{num_screenshots} 스크린샷 캡처 완료: {file_path}")
            
            time.sleep(capture_interval_seconds)
        except KeyboardInterrupt:
            print("\n캡처 중단. 프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"오류 발생: {e}")
