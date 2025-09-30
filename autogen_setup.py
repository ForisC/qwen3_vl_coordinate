# run_team.py  —  AutoGen AgentChat v0.4+ 版本
import asyncio
from pathlib import Path

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient

PROMPTS_DIR = Path("prompts")
def load(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")

# 1) 準備模型（可改成你偏好的 4o/4.1-mini 等）
model = OpenAIChatCompletionClient(model="gpt-4o-2024-08-06")  # 會讀 OPENAI_API_KEY

# 2) 建立五個角色（用你的檔案當 system_message）
orchestrator = AssistantAgent(
    name="orchestrator",
    model_client=model,
    system_message=load("orchestrator.md"),
)
planner = AssistantAgent(
    name="planner",
    model_client=model,
    system_message=load("planner.md"),
)
operator = AssistantAgent(
    name="operator",
    model_client=model,
    system_message=load("operator.md"),
)
ui_verifier = AssistantAgent(
    name="ui_verifier",
    model_client=model,
    system_message=load("ui_verifier.md"),
)
bbox_getter = AssistantAgent(
    name="bbox_getter",
    model_client=model,                # 若你有影像模型，可替換成該供應商的 model_client
    system_message=load("bbox_getter.md"),
)

# 3) 把五個 agent 放進一個 RoundRobin 團隊
team = RoundRobinGroupChat([orchestrator, planner, operator, ui_verifier, bbox_getter])

async def main():
    # 4) 發任務（你可以把 User 指令寫得更具體；這裡僅為示例）
    task = TextMessage(
        content="請將『測試小畫家是否正常』轉為 test case 並依流程執行；"
                "原子操作由 operator；執行前/後由 ui_verifier；"
                "需要座標時 operator 透過 bbox_getter 取得；"
                "最後 orchestrator 回傳單一 JSON 總結。",
        source="user",
    )
    result = await team.run(task=task)
    # 5) 取得所有訊息或從 result 裡擷取 orchestrator 的最終 JSON
    for m in result.messages:
        if m.source == "orchestrator":
            print(m.content)

if __name__ == "__main__":
    asyncio.run(main())
