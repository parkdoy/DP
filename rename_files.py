import os

def rename_files(folder_path, old_prefix, new_prefix):
    """
    폴더 내의 파일 이름을 일괄적으로 변경하는 함수

    Args:
        folder_path (str): 파일이 있는 폴더 경로
        old_prefix (str): 변경하려는 파일 이름의 접두사 (예: 'screenshot')
        new_prefix (str): 새로 지정할 파일 이름의 접두사 (예: 'companion')
    """
    # 파일이 있는 폴더 경로를 확인합니다.
    if not os.path.exists(folder_path):
        print(f"오류: {folder_path} 경로를 찾을 수 없습니다.")
        return

    # 폴더 내 모든 파일 리스트를 가져옵니다.
    files = os.listdir(folder_path)
    
    # 숫자 순서대로 정렬하기 위해 리스트를 정렬합니다.
    files.sort()

    count = 1
    for filename in files:
        # 파일 이름이 지정된 접두사로 시작하고 확장자가 .png인지 확인합니다.
        if filename.startswith(old_prefix) and filename.endswith(".png"):
            # 기존 파일 이름에서 숫자 부분을 추출합니다.
            try:
                # 'screenshot_001.png' -> '001.png'
                num_str = filename[len(old_prefix) + 1:-4]
                
                # 새로운 파일 이름 생성 (0으로 채워진 3자리 숫자)
                new_name = f"{new_prefix}_{count:03d}.png"
                
                old_file_path = os.path.join(folder_path, filename)
                new_file_path = os.path.join(folder_path, new_name)
                
                # 파일 이름 변경
                os.rename(old_file_path, new_file_path)
                print(f"{filename} -> {new_name}")
                
                count += 1

            except ValueError:
                print(f"경고: {filename} 파일 이름이 예상된 형식이 아닙니다. 건너뜁니다.")

if __name__ == "__main__":
    # 스크린샷 파일이 있는 폴더 경로를 지정하세요.
    # 예시 경로: "yolo_project/dataset/train/images"
    folder = "./game_screenshots"
    
    # 변경하려는 파일 이름의 접두사 (예: 'screenshot')
    old_prefix = "screenshot"

    # 새로 지정할 파일 이름의 접두사 (예: 'companion')
    new_prefix = "companion"

    rename_files(folder, old_prefix, new_prefix)
    print("\n파일 이름 변경이 완료되었습니다.")

'''
### 2. 스크립트 실행 방법

1.  위 코드를 `rename_files.py`라는 이름으로 저장합니다.
2.  스크립트 내의 `folder` 변수 값을 이미지 파일이 있는 정확한 경로로 수정합니다. 예를 들어, `screenshots.py` 파일로 캡처한 이미지가 `game_screenshots` 폴더에 있다면, `folder = "game_screenshots"`로 설정하면 됩니다.
3.  터미널(또는 명령 프롬프트)을 열고, 스크립트가 있는 폴더로 이동합니다.
4.  아래 명령어를 입력하여 스크립트를 실행합니다.

```bash
python rename_files.py
'''