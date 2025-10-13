# autogen_setup.py
from typing import Any, Dict


from pathlib import Path
import subprocess
import image_lib

SCRIPT_FOLDER = (Path(__file__).parent / "scripts").resolve()


def screenshot() -> str:
    """screenshot and return base64 string"""
    temp_dir = Path("C:/tmp_screenshots")
    temp_dir.mkdir(parents=True, exist_ok=True)

    script = SCRIPT_FOLDER / "screenshot.ps1"
    result = subprocess.run(
        ["powershell", "-File", str(script)],
        capture_output=True,
        text=True,
        cwd=temp_dir,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Error executing screenshot: {result.stderr}")

    filepath = result.stdout.strip()
    if not Path(filepath).is_file():
        raise FileNotFoundError(f"Screenshot file not found: {filepath}")

    return image_lib.image_to_base64(filepath)


def on_click_screenshot(x: int, y: int) -> Dict[str, Any]:
    script = SCRIPT_FOLDER / "uut_op.ps1"
    result = subprocess.run(
        [
            "powershell",
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
    if result.returncode != 0:
        return {
            "result": False,
            "is_error": True,
            "reason": f"Error executing click: {result.stderr}",
            "screenshot": {"path": ""},
        }


def tool_click(x: int, y: int) -> Dict[str, Any]:
    # TODO: 實作你的滑鼠點擊並截圖；回傳 post-screenshot 路徑
    return {
        "result": True,
        "is_error": False,
        "reason": f"Clicked ({x},{y})",
        "screenshot": {"path": "C:/tmp/post_click.png"},
    }


def tool_double_click(x: int, y: int) -> Dict[str, Any]:
    return {
        "result": True,
        "is_error": False,
        "reason": f"DoubleClicked ({x},{y})",
        "screenshot": {"path": "C:/tmp/post_doubleclick.png"},
    }


def tool_right_click(x: int, y: int) -> Dict[str, Any]:
    return {
        "result": True,
        "is_error": False,
        "reason": f"RightClicked ({x},{y})",
        "screenshot": {"path": "C:/tmp/post_rightclick.png"},
    }


def tool_type_text(text: str) -> Dict[str, Any]:
    return {
        "result": True,
        "is_error": False,
        "reason": f'Typed "{text}"',
        "screenshot": {"path": "C:/tmp/post_type.png"},
    }


def tool_press_key(key: str) -> Dict[str, Any]:
    return {
        "result": True,
        "is_error": False,
        "reason": f"Pressed {key}",
        "screenshot": {"path": "C:/tmp/post_presskey.png"},
    }


def tool_sleep(seconds: float) -> Dict[str, Any]:
    # 建議真的 sleep，再截圖
    # import time; time.sleep(seconds)
    return {
        "result": True,
        "is_error": False,
        "reason": f"Slept {seconds}s",
        "screenshot": {"path": "C:/tmp/post_sleep.png"},
    }


def tool_capture_prescreenshot() -> Dict[str, Any]:
    # 若 operator 在呼叫 bbox_getter 前需要 pre-snap
    return {"path": "C:/tmp/pre.png"}


if __name__ == "__main__":
    print(screenshot())
