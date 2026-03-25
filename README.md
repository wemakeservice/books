<div align="center">
  <h1>📸 Books Auto Capture Script</h1>
  <p>파이썬을 활용한 리디북스(Ridibooks) 등 PC/Mac 뷰어 화면 자동 캡처 스크립트입니다.</p>
</div>

---

## ✨ Features
해당 스크립트는 **macOS**와 **Windows** 환경 모두에서 네이티브하게 작동하도록 설계되었습니다.

- **Mac 네이티브 지원**: `AppleScript`(`osascript`)를 활용하여 리디북스 창의 위치와 크기를 빠르고 정확하게 찾아냅니다. (`pygetwindow` 의존성 탈피)
- **Windows 지원**: `pygetwindow` 라이브러리를 통해 데스크톱 환경의 뷰어 창을 찾아 활성화합니다.
- **전자동 캡처 시스템**:
  - 지정 윈도우의 테두리 좌표(Bbox)를 감지하여 캡처합니다.
  - 다음 페이지로 넘기기 위해 자동으로 `오른쪽 화살표(Right Arrow)` 키 이벤트를 발생시킵니다.
  - 모든 스크린샷은 안전하게 `screenshots/` 디렉토리에 일련번호 형식으로 자동 저장됩니다.

## 🛠️ Prerequisites
- **Python 3.8+** 이상
- 지원 대상인 책 뷰어 앱 (예: 리디북스 PC/Mac 클라이언트)

## 🚀 Installation & Usage

1. **저장소 가져오기 및 디렉토리 이동**
   ```bash
   git clone <your-github-repo-url>
   cd books
   ```

2. **가상 환경 생성 및 의존성 패키지 설치**
   <details>
   <summary><b>macOS / Linux 의 경우</b></summary>
   
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   </details>

   <details>
   <summary><b>Windows 의 경우</b></summary>

   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
   </details>

3. **스크립트 실행**
   먼저 캡처하고자 하는 뷰어 앱(예: 리디북스)을 실행하여 원하는 책 이미지를 띄워 둡니다. 그 후 아래 명령어를 터미널에 입력하여 실행합니다.
   
   ```bash
   python capture_books.py
   ```
   * 실행 후 터미널 창에서 **`Ctrl+C`**를 누르면 언제든지 캡처를 강제 종료할 수 있습니다.

---

## 🚨 Important Notes & Troubleshooting

### 🍏 Mac 환경 설정 (필수 권한 부여)
macOS에서 스크립트가 창을 제어하고 화면을 녹화하려면 **반드시 권한이 부여되어야 합니다**.
> [!IMPORTANT]
> **시스템 설정(System Preferences) -> 개인정보 보호 및 보안(Privacy & Security)** 으로 이동하세요.
> 1. **화면 기록(Screen Recording)**: 사용 중인 터미널 앱(또는 커서, VSCode 등 IDE)의 권한 허용
> 2. **손쉬운 사용(Accessibility)**: 제어(화살표 키)를 위해 터미널 및 `python` 실행 파일에 대한 권한 허용

> [!NOTE]
> **Retina 디스플레이 해상도 이슈**
> 바탕화면 해상도 배율에 따라 캡처 크기가 달라질 수 있습니다(x2 스케일링 이슈). 화면의 일부만 잘려서 캡처된다면 `Pillow` 패키지를 최신 버전으로 업데이트(`pip install --upgrade Pillow`)하거나 사용 중인 디스플레이 해상도를 표준 배율로 임시 변경해 보세요.

### 🔒 DRM (디지털 권리 관리) 관련 안내
> [!WARNING]
> 이 스크립트는 단순히 윈도우 위치 좌표를 지정해 캡처 버튼을 누르고 화면을 넘겨주는 역할에 한정됩니다.
> 만약 뷰어 자체에서 OS 레벨의 화면 캡처 방지(예: `SetWindowDisplayAffinity`)가 적용된 경우, 캡처된 결과물이 **검은 화면**으로 저장될 수 있습니다. (이 스크립트는 DRM 자체를 우회하는 크래킹 툴이 아님을 밝힙니다.)
