# PyCharm Scripting Project

This is a starter project for your Python scripts.

## How to run in PyCharm

1. Open this folder in PyCharm: `File > Open...` and select `C:\Users\DELL9\.gemini\antigravity\scratch\pycharm_scripts`
2. Open `main.py`.
3. Right-click in the editor and select `Run 'main'`.

## Login Script Setup

To run the `login_script.py`, you need to install a few libraries.

1.  **Open the Terminal** in PyCharm (usually at the bottom left).
2.  Run this command to install the required packages:
    ```bash
    pip install selenium webdriver-manager
    ```
3.  **Run the script**:
    *   Open `login_script.py`.
    *   Right-click and select `Run 'login_script'`.

### Troubleshooting: "Python not found"
If you see an error saying `Python was not found` when running commands in the terminal, try using `py` instead of `python`.
Example:
```bash
py -m pip install selenium webdriver-manager
py login_script.py
```
