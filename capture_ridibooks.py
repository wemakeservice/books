import pygetwindow as gw
from PIL import ImageGrab, ImageChops
import time
import os
import pyautogui

def capture_ridibooks_window():
    print("리디북스 창 도구를 탐색 중입니다...")
    
    # 1. 리디북스 창 찾기
    # VS Code 등 다른 창("capture_ridibooks.py")이 선택되는 것을 방지하기 위해 정확히 일치하거나 특정 패턴만 허용합니다.
    target_window = None
    for w in gw.getAllWindows():
        title = w.title.strip()
        # 정확히 "Ridibooks" 혹은 "리디" 이거나, "리디" 로 시작하는 책 뷰어 창인지 확인 (VS Code 창 제외)
        if title == "Ridibooks" or title == "리디" or (title.startswith("리디") and "code" not in title.lower() and "python" not in title.lower()):
            target_window = w
            break

    if not target_window:
        print("❌ 리디북스 창을 찾을 수 없습니다. 앱이 실행 중이고 화면에 떠 있는지 확인해주세요.")
        return

    ridi_window = target_window
    print(f"✅ 발견된 창: {ridi_window.title}")
    
    if ridi_window.isMinimized:
        ridi_window.restore()
    
    try:
        ridi_window.activate()
    except Exception as e:
        print(f"⚠️ 창 활성화 권한 문제 발생 (진행은 계속됩니다): {e}")

    # 창이 활성화 될 시간을 대기합니다.
    time.sleep(1)

    # 창 위치 및 크기
    left = ridi_window.left
    top = ridi_window.top
    width = ridi_window.width
    height = ridi_window.height
    bbox = (left, top, left + width, top + height)

    # 캡처 저장 폴더 생성
    save_dir = "screenshots"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    page_num = 1
    previous_image = None

    print("📸 자동 캡처를 시작합니다. 도중에 강제 종료하려면 실행 중인 터미널에서 Ctrl+C를 누르세요.")
    
    # 4. 5페이지만 자동 캡처 테스트
    while page_num <= 5:
        # 매번 캡처 직전에 창을 강제로 맨 앞으로(Foreground) 가져옵니다.
        try:
            target_window.activate()
        except:
            pass
        
        # 화면이 앞으로 올 수 있도록 0.5초 대기
        time.sleep(0.5)

        # 1. 화면 스크린샷 캡처
        screenshot = ImageGrab.grab(bbox)
        
        # 마지막 장(화면이 동일한지) 체크
        if previous_image is not None:
            # 두 이미지 픽셀 비교
            diff = ImageChops.difference(screenshot, previous_image)
            # 차이가 없다면 (bounding box가 None이라면) 완료 처리
            if not diff.getbbox():
                print("🏁 이전 페이지와 동일한 화면입니다. 마지막 장에 도달하여 작업을 종료합니다.")
                break

        # 2. 스크린샷 이미지 저장
        # 보기 좋게 page_0001.png, page_0002.png 형태로 저장합니다.
        file_path = os.path.join(save_dir, f"page_{page_num:04d}.png")
        screenshot.save(file_path)
        print(f"[{page_num}페이지] 캡처 및 저장 완료")

        # 분석용으로 현재 화면을 이전 화면 변수에 저장해둡니다.
        previous_image = screenshot
        page_num += 1

        # 3. 다음장으로 이동 (키보드 오른쪽 화살표)
        # 키 입력이 리디북스에 제대로 전달되게끔 매번 창을 활성화합니다.
        try:
            target_window.activate()
        except:
            pass
        
        pyautogui.press('right')
        
        # 페이지 넘어가는 애니메이션 로딩을 위해 0.8초 정도 대기 (컴퓨터 환경에 맞춰 조절 가능)
        time.sleep(0.8)

if __name__ == "__main__":
    capture_ridibooks_window()
