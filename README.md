# Test App: A simple app to automate testing devices with the Antutu Benchmark

# Requirements
- Python
- Tesseract OCR
- Antutu APKs

# Setup

1. Install Tesseract, Python, abd dependencies
  - [Python](https://www.python.org/downloads/)
  - [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
  - dependencies
    ```
    pip install -r requirements.txt
    ```
2. Cloning the repo
3. PyInstaller to build App
  - Install Pyinstaller
  ```
  pip install pyinstaller
  ```
  - Go to src directory
  ```
  cd src
  ```
  - Build App
  ```
  pyinstaller --onefile main.py
  ```
4. App is build. Navigate to the dist file in src and run the main.exe

# How to use

App revolves around the [ppadb](https://pypi.org/project/pure-python-adb/) package in python. Connect a device with developer mode and USB Debugging enabled. Then you can "init device" and start the benchmakring. It will output the results in the window and save the previous results in a results.json file in long format.

### Credits
- Built around [ppadb package](https://github.com/Swind/pure-python-adb/stargazers)
- Help from [pyinstaller action windows](https://github.com/JackMcKew/pyinstaller-action-windows)


