# autogen_setup.py
import os
from pathlib import Path

import autogen

from tools import (
    tool_capture_prescreenshot,
    tool_click,
    tool_double_click,
    tool_press_key,
    tool_right_click,
    tool_sleep,
    tool_type_text,
)

# ========= 讀取本地 Prompts =========
BASE = Path(__file__).parent
PROMPTS_DIR = BASE / "prompts"

def load_prompt(name: str) -> str:
    # e.g., name="orchestrator.md"
    p = PROMPTS_DIR / name
    return p.read_text(encoding="utf-8")

# ========= LLM 設定 =========
# 依你的實際供應商填入 API Key；以下示範同時準備「推理模型」與「影像模型」兩組 config_list
openai_cfg = [{
    "model": os.getenv("REASONING_MODEL", "gpt-4o-mini"),
    "api_key": os.getenv("OPENAI_API_KEY"),
    "temperature": 0.1,
}]
vision_cfg = [{
    "model": os.getenv("VISION_MODEL", "qwen-2.5-vl"),
    "api_key": os.getenv("QWEN_API_KEY"),
    # 可按供應商需求加入 "api_type": "dashscope" 等欄位
    "temperature": 0.0,
}]

reasoning_llm = {"config_list": openai_cfg}
vision_llm    = {"config_list": vision_cfg}


# ========= 建立 Agents（system_message 直接讀檔） =========
def make_agents():
    orchestrator = autogen.AssistantAgent(
        name="orchestrator",
        system_message=load_prompt("orchestrator.md"),
        llm_config=reasoning_llm,
    )

    planner = autogen.AssistantAgent(
        name="planner",
        system_message=load_prompt("planner.md"),
        llm_config=reasoning_llm,
    )

    ui_verifier = autogen.AssistantAgent(
        name="ui_verifier",
        system_message=load_prompt("ui_verifier.md"),
        llm_config=reasoning_llm,
    )

    bbox_getter = autogen.AssistantAgent(
        name="bbox_getter",
        system_message=load_prompt("bbox_getter.md"),
        llm_config=vision_llm,  # 影像模型
    )

    # Operator 綁定工具（這裡只示範幾個；你可擴充成完整工具集）
    operator = autogen.AssistantAgent(
        name="operator",
        system_message=load_prompt("operator.md"),
        llm_config=reasoning_llm,
        tools=[
            autogen.Tool(name="click",         func=tool_click),
            autogen.Tool(name="double_click",  func=tool_double_click),
            autogen.Tool(name="right_click",   func=tool_right_click),
            autogen.Tool(name="type_text",     func=tool_type_text),
            autogen.Tool(name="press_key",     func=tool_press_key),
            autogen.Tool(name="sleep",         func=tool_sleep),
            autogen.Tool(name="capture_pre",   func=tool_capture_prescreenshot),
            # 提醒：bbox_getter 不是工具函式，operator 內部需「透過對話」呼叫 bbox_getter 取得座標
        ],
    )

    return orchestrator, planner, operator, ui_verifier, bbox_getter

# ========= 建立 GroupChat =========
def make_group():
    orchestrator, planner, operator, ui_verifier, bbox_getter = make_agents()
    group = autogen.GroupChat(
        agents=[orchestrator, planner, operator, ui_verifier, bbox_getter],
        messages=[],
        max_round=60,
        speaker_selection_method="auto",
    )
    manager = autogen.GroupChatManager(groupchat=group, llm_config=reasoning_llm)
    return manager

# ========= 端到端示例：給一段任務說明，讓 orchestrator 帶著大家跑 =========
if __name__ == "__main__":
    manager = make_group()

    # 你可以建立一個 User 代理來注入任務
    user = autogen.UserProxyAgent(
        name="user",
        human_input_mode="NEVER",
        code_execution_config=False,
    )

    # 範例任務：測試 Paint 是否正常（或任意控制任務）
    # 這裡不放任何 prompt 內容，純下發需求；各角色會從 prompts/*.md 讀取 system prompt
    task = (
        "請將『測試小畫家是否正常』轉為 test case，並依步驟執行；"
        "所有原子操作由 operator 執行；執行前/後均由 ui_verifier 判斷；"
        "需要座標時 operator 請向 bbox_getter 取得 bbox；"
        "最終由 orchestrator 回傳單一 JSON 總結。"
    )

    user.initiate_chat(manager, message=task)
