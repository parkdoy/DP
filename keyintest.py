# 입력 테스트를 위한 스크립트입니다.
# pydirectinput 라이브러리를 사용하여 키 입력을 시뮬레이 테스트

import time
import pydirectinput

def main():
    """
    pydirectinput을 사용한 키 입력 테스트를 실행합니다.
    """
    print("--- 키 입력 테스트 시작 ---")
    print("5초 안에 메모장이나 다른 텍스트 편집기 창을 클릭하세요.")
    print("그러면 '5'가 입력됩니다.")
    time.sleep(5)  # 사용자가 창을 전환할 시간을 줍니다.

    print("키 입력 이벤트 생성 중...")
    # '5'번 키를 누르는 이벤트 생성
    # pydirectinput은 더 낮은 레벨의 하드웨어 신호를 보냅니다.
    pydirectinput.press('5')
    
    print("테스트 완료. 메모장 창에 '5'가 입력되었는지 확인하세요.")
    
if __name__ == "__main__":
    main()
