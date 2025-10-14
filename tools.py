# autogen_setup.py
from typing import Any, Dict, Literal
from pathlib import Path
import subprocess
import time
import image_lib

SCRIPT_FOLDER: Path = (Path(__file__).parent / "scripts").resolve()
KeyName = Literal["up", "down", "left", "right", "win", "enter", "esc"]


def screenshot() -> str:
    """
    Take a screenshot of the current screen and return it as a base64-encoded string.

    Usage:
        - Call this function when you need a screenshot after an operation.
        - No parameters required.
        - Returns a base64-encoded string of the image.
    """
    temp_dir = Path("C:/tmp_screenshots")
    temp_dir.mkdir(parents=True, exist_ok=True)

    script: Path = SCRIPT_FOLDER / "screenshot.ps1"
    result = subprocess.run(
        [
            "powershell",
            "-File",
            str(script),
            "-ExecutionPolicy",
            "Bypass",
            "-NoProfile",
        ],
        capture_output=True,
        text=True,
        cwd=temp_dir,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Error executing screenshot: {result.stderr}")

    filepath = Path(result.stdout.strip())
    if not filepath.is_file():
        raise FileNotFoundError(f"Screenshot file not found: {filepath}")

    return filepath
    return image_lib.image_to_base64(filepath)


def mouse_click(x: int, y: int) -> Dict[str, Any]:
    """
    Perform a single left mouse click at the given screen coordinates.

    Usage:
        mouse_click(500, 400)
        → Clicks once at (500, 400) and returns a result dict with screenshot.
    """
    script: Path = SCRIPT_FOLDER / "uut_op.ps1"
    result = subprocess.run(
        [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-NoProfile",
            "-File",
            str(script),
            "-operation",
            "click",
            "-x",
            str(x),
            "-y",
            str(y),
        ],
        capture_output=True,
        text=True,
    )
    time.sleep(1)
    screenshot_base64: str = screenshot()

    if result.returncode != 0:
        return {
            "result": False,
            "is_error": True,
            "reason": f"Error executing click: {result.stderr}",
            "screenshot": {"base64": screenshot_base64},
        }

    return {
        "result": True,
        "is_error": False,
        "reason": f"Clicked ({x},{y})",
        "screenshot": {"base64": screenshot_base64},
    }


def mouse_double_click(x: int, y: int) -> Dict[str, Any]:
    """
    Perform a double left mouse click at the given coordinates.

    Usage:
        mouse_double_click(300, 400)
        → Double-clicks at (300, 400) and returns a result dict with screenshot.
    """
    script: Path = SCRIPT_FOLDER / "uut_op.ps1"
    result = subprocess.run(
        [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-NoProfile",
            "-File",
            str(script),
            "-operation",
            "double",
            "-x",
            str(x),
            "-y",
            str(y),
        ],
        capture_output=True,
        text=True,
    )
    time.sleep(1)
    screenshot_base64: str = screenshot()

    if result.returncode != 0:
        return {
            "result": False,
            "is_error": True,
            "reason": f"Error executing double_click: {result.stderr}",
            "screenshot": {"base64": screenshot_base64},
        }

    return {
        "result": True,
        "is_error": False,
        "reason": f"Double Clicked ({x},{y})",
        "screenshot": {"base64": screenshot_base64},
    }


def mouse_right_click(x: int, y: int) -> Dict[str, Any]:
    """
    Perform a right mouse click at the given coordinates.

    Usage:
        mouse_right_click(600, 300)
        → Right-clicks at (600, 300) and returns a result dict with screenshot.
    """
    script: Path = SCRIPT_FOLDER / "uut_op.ps1"
    result = subprocess.run(
        [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-NoProfile",
            "-File",
            str(script),
            "-operation",
            "right",
            "-x",
            str(x),
            "-y",
            str(y),
        ],
        capture_output=True,
        text=True,
    )
    time.sleep(1)
    screenshot_base64: str = screenshot()

    if result.returncode != 0:
        return {
            "result": False,
            "is_error": True,
            "reason": f"Error executing right_click: {result.stderr}",
            "screenshot": {"base64": screenshot_base64},
        }

    return {
        "result": True,
        "is_error": False,
        "reason": f"Right Clicked ({x},{y})",
        "screenshot": {"base64": screenshot_base64},
    }


def keyboard_input(
    text: str, click_before_type: bool = False, x: int = 0, y: int = 0
) -> Dict[str, Any]:
    """
    Type the given text using the keyboard, optionally clicking a position before typing.

    Usage:
        keyboard_input("hello world")
        → Types "hello world".

        keyboard_input("username", click_before_type=True, x=400, y=500)
        → Clicks at (400, 500) first, then types "username".
    """
    script: Path = SCRIPT_FOLDER / "uut_op.ps1"
    command = [
        "powershell",
        "-ExecutionPolicy",
        "Bypass",
        "-NoProfile",
        "-File",
        str(script),
        "-operation",
        "type",
        "-text",
        text,
    ]

    if click_before_type:
        command += ["-click_before_type", "-x", str(x), "-y", str(y), "-text", text]

    result = subprocess.run(command, capture_output=True, text=True)
    time.sleep(1)
    screenshot_base64: str = screenshot()

    if result.returncode != 0:
        return {
            "result": False,
            "is_error": True,
            "reason": f"Error executing keyboard_input: {result.stderr}",
            "screenshot": {"base64": screenshot_base64},
        }

    return {
        "result": True,
        "is_error": False,
        "reason": f"Typed '{text}'",
        "screenshot": {"base64": screenshot_base64},
    }


def keyboard_hotkey(key: KeyName) -> Dict[str, Any]:
    """
    Simulate pressing a specific hotkey (e.g., arrows, Win, Enter, Esc).

    Usage:
        keyboard_hotkey("win")
        → Presses the Windows key.

        keyboard_hotkey("up")
        → Presses the Up arrow key.
    """
    script: Path = SCRIPT_FOLDER / "send_key.ps1"
    result = subprocess.run(
        [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-NoProfile",
            "-File",
            str(script),
            "-key",
            key,
        ],
        capture_output=True,
        text=True,
    )
    time.sleep(1)
    screenshot_base64: str = screenshot()

    if result.returncode != 0:
        return {
            "result": False,
            "is_error": True,
            "reason": f"Error executing keyboard_hotkey: {result.stderr}",
            "screenshot": {"base64": screenshot_base64},
        }

    return {
        "result": True,
        "is_error": False,
        "reason": f"Pressed hotkey '{key}'",
        "screenshot": {"base64": screenshot_base64},
    }


def sleep(seconds: int) -> Dict[str, Any]:
    """
    Pause execution for a specified duration and capture a screenshot afterward.

    Usage:
        sleep(2)
        → Waits for 2 seconds and returns a screenshot of the current screen.
    """
    time.sleep(seconds)
    screenshot_base64: str = screenshot()

    return {
        "result": True,
        "is_error": False,
        "reason": f"Slept for {seconds} seconds",
        "screenshot": {"base64": screenshot_base64},
    }


if __name__ == "__main__":
    print(mouse_click(100, 200))
    print(keyboard_hotkey("win"))