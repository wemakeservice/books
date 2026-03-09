# Books Auto Capture Script 📸

This is a Python script that automatically captures pages of the Books PC/Mac viewer and saves them as images using Python.

## Prerequisites

- Python 3.8+
- The `Books` viewer installed on your OS.

## Installation

1. Clone this repository:
   ```bash
   git clone <your-github-repo-url>
   cd books-auto-capture
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Usage

1. Open the Books application and ensure the book you want to capture is open.
2. Run the script:
   ```bash
   python capture_books.py
   ```
3. The script will automatically find the active Books window, capture the screen, save it to the `screenshots/` directory, and press the `Right Arrow` key to proceed to the next page.
4. To forcefully stop the script, press `Ctrl+C` in your terminal.

## Note on Mac Support
- **Window Detection**: On macOS, the script uses AppleScript (`osascript`) to find and activate the Books window natively, avoiding issues with `pygetwindow`.
- **Permissions**: You MUST grant **Accessibility Permissions** and **Screen Recording Permissions** to your Terminal (or IDE) and Python executable in `System Preferences -> Security & Privacy -> Privacy`. This allows `pyautogui` to send the right-arrow keystrokes and `ImageGrab` to capture the screen layout.
- **Retina Displays**: If you are using a Mac with a Retina display, the bounding box coordinate scaling might differ slightly depending on your Pillow version. Ensure your `Pillow` library is updated (`pip install --upgrade Pillow`).

## Disclaimer
Note: Books employs DRM restrictions on their PC viewer (e.g., `SetWindowDisplayAffinity`) that may render screenshots black or transparent. This script handles the window automation but does not natively bypass OS-level DRM restrictions. Using an Android App Player (like BlueStacks or LDPlayer) as the target window is the most common workaround.
