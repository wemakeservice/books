import sys
import os
import time
import subprocess
from PIL import ImageGrab, ImageChops
import pyautogui

if sys.platform != 'darwin':
    import pygetwindow as gw

def get_mac_window_bounds():
    """
    AppleScript를 사용하여 활성화된 리디북스 창의 위치와 크기(bounds)를 가져옵니다.
    반환값: (left, top, right, bottom)
    """
    script = '''
    tell application "System Events"
        -- "Ridibooks" 또는 "리디" 프로세스 찾기
        set procName to ""
        if exists (process "Ridibooks") then
            set procName to "Ridibooks"
        else if exists (process "리디") then
            set procName to "리디"
        end if
        
        if procName is not "" then
            tell process procName
                set frontmost to true
                set wBounds to position of window 1 & size of window 1
                return wBounds
            end tell
        else
            return ""
        end if
    end tell
    '''
    try:
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        out = result.stdout.strip()
        if not out:
            return None
            
        # AppleScript 결과 포맷: x, y, width, height (예: 100, 200, 800, 600)
        parts = [int(p.strip()) for p in out.split(',')]
        x, y, w, h = parts[0], parts[1], parts[2], parts[3]
        return (x, y, x + w, y + h)
    except Exception as e:
        print(f"Mac 창 정보 가져오기 실패: {e}")
        return None

def capture_ridibooks_window():
    print("리디북스 창 도구를 탐색 중입니다...")
    
    bbox = None
    target_window = None
    
    # 1. OS별 리디북스 창 찾기 및 활성화
    if sys.platform == 'darwin':  # macOS
        bbox = get_mac_window_bounds()
        if not bbox:
            print("❌ 리디북스 창을 찾을 수 없습니다. 앱이 실행 중이고 화면에 떠 있는지 확인해주세요.")
            return
        print("✅ Mac 환경: 리디북스 창 활성화 및 위치 획득 완료")
        
    else:  # Windows (win32)
        # 기존 로직 유지 (pygetwindow 사용)
        for w in gw.getAllWindows():
            title = w.title.strip()
            if title == "Ridibooks" or title == "리디" or (title.startswith("리디") and "code" not in title.lower() and "python" not in title.lower()):
                target_window = w
                break

        if not target_window:
            print("❌ 리디북스 창을 찾을 수 없습니다. 앱이 실행 중이고 화면에 떠 있는지 확인해주세요.")
            return

        print(f"✅ 발견된 창: {target_window.title}")
        
        if target_window.isMinimized:
            target_window.restore()
        
        try:
            target_window.activate()
        except Exception as e:
            print(f"⚠️ 창 활성화 권한 문제 발생 (진행은 계속됩니다): {e}")

        # 창 위치 및 크기
        left = target_window.left
        top = target_window.top
        width = target_window.width
        height = target_window.height
        bbox = (left, top, left + width, top + height)

    # 창이 활성화 될 시간을 대기합니다.
    time.sleep(1)

    # 캡처 저장 폴더 생성
    save_dir = "screenshots"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    page_num = 1
    previous_image = None

    print("📸 자동 캡처를 시작합니다. 도중에 강제 종료하려면 실행 중인 터미널에서 Ctrl+C를 누르세요.")
    
    # 사용자가 직접 강제종료할 때까지 무한 반복 캡처
    while True:
        # 매번 캡처 직전에 창을 강제로 맨 앞으로(Foreground) 가져옵니다.
        if sys.platform == 'darwin':
            # Mac에서는 AppleScript를 한 번 호출해서 창을 앞으로 가져올 수 있지만 속도/부하 고려
            # Mac의 경우 이미 frontmost 상태이므로 pyautogui나 약간의 대기만으로 충분합니다.
            pass
        else:
            try:
                if target_window:
                    target_window.activate()
            except:
                pass
        
        # 화면이 앞으로 올 수 있도록 0.5초 대기
        time.sleep(0.5)

        # 1. 화면 스크린샷 캡처
        # Mac의 경우 Retina 해상도(x2) 이슈가 있을 수 있으나, 최신 Pillow에서 all_screens=True 로 잡히거나 bounding_box 대로 잡힐 수 있음.
        if sys.platform == 'darwin':
            screenshot = ImageGrab.grab(bbox=bbox, all_screens=True)
        else:
            screenshot = ImageGrab.grab(bbox=bbox)
        
        # 이전 페이지와 동일한 화면인지 체크하는 로직은 사용자의 요청으로 제외되었습니다.

        # 2. 스크린샷 이미지 저장
        file_path = os.path.join(save_dir, f"page_{page_num:04d}.png")
        screenshot.save(file_path)
        print(f"[{page_num}페이지] 캡처 및 저장 완료")

        previous_image = screenshot
        page_num += 1

        # 3. 다음장으로 이동 (키보드 오른쪽 화살표)
        if sys.platform != 'darwin':
            try:
                if target_window:
                    target_window.activate()
            except:
                pass
        
        pyautogui.press('right')
        
        # 페이지 넘어가는 애니메이션 로딩을 위해 0.8초 대기
        time.sleep(0.8)

if __name__ == "__main__":
    capture_ridibooks_window()
