# autogen_setup.py
from typing import Any, Dict

# ========= Operator 可呼叫的工具（請替換為你的實作） =========
# 這些函式應該執行「單一步原子動作」並回傳 {result,is_error,reason,screenshot:{path}}
# 若你已經有自家的 agent/服務，直接在這裡呼叫即可。

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
