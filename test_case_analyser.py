from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()



def test_case_analyser(input_text):
    client = OpenAI()
    system_prompt = Path("prompts/test_case_analyser.md").read_text(encoding="utf-8")
    response = client.responses.create(
        model="gpt-5",
        reasoning={"effort": "low"},
        input=[
            {
                "role": "developer",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": input_text
            }
        ]
    )

    return response.output_text



if __name__ == "__main__":
    input_text = "測試 POSTMAN 是否能正常開啟"
    output = test_case_analyser(input_text)
    print(output)