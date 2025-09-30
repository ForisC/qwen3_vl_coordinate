import base64
import json
import os
from pathlib import Path

import cv2
from dotenv import load_dotenv
from openai import OpenAI
import image_lib

# Load environment variables from .env file
load_dotenv()



class Qwen3VL:
    @classmethod
    def get_bbox(cls, image_path, user_input):

        bbox_getter_sys = Path("prompts/bbox_getter.md").read_text(encoding="utf-8")

        client = OpenAI(
            # If the environment variable is not configured, replace the following line with: api_key="sk-xxx"
            api_key=os.getenv("ALIBABACLOUD_API_KEY"),
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        )

        image_path = Path(image_path)
        image_base64 = image_lib.image_to_base64(image_path)

        completion = client.chat.completions.create(
            model="qwen3-vl-235b-a22b-instruct",
            messages=[
                {"role": "system", "content": bbox_getter_sys},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_input},
                        {"type": "image_url", "image_url": {"url": "data:image/png;base64," + image_base64}},
                    ],
                },
            ],
            stream=True,
            top_p=0.0001,
            temperature=0,
        )
        full_content = ""

        for chunk in completion:
            if chunk.choices[0].delta.content is None:
                continue
            full_content += chunk.choices[0].delta.content


        print(f"Complete content:\n{full_content}")

        content_json = json.loads(full_content)
        # {
        #   "bbox": [46, 659, 82, 731],
        #   "name": "TeamViewer icon",
        #   "description": "位於桌面左下角區域的 TeamViewer 應用程式圖示，具有藍色背景與白色雙箭頭標誌，下方標註「TeamViewer」文字。"
        # }


        if content_json["bbox"]:
            print("Get bbox:", content_json["bbox"])
            image = cv2.imread(str(image_path))
            image_weight, image_height = image.shape[1], image.shape[0]
            model_weight, model_height = 1000, 1000
            content_json["bbox"][0] = int(content_json["bbox"][0] / model_weight * image_weight)
            content_json["bbox"][2] = int(content_json["bbox"][2] / model_weight * image_weight)
            content_json["bbox"][1] = int(content_json["bbox"][1] / model_height * image_height)
            content_json["bbox"][3] = int(content_json["bbox"][3] / model_height * image_height)
            print("Scaled bbox:", content_json["bbox"])

        return content_json






if __name__ == "__main__":
    user_input = "桌面上的 teamviewer icon"
    user_input_image_path = r".\example\desktop1.png"

    content_json = Qwen3VL.get_bbox(user_input_image_path, user_input)
    image_lib.save_bbox_image(user_input_image_path, content_json["bbox"])
    image_lib.draw_bbox(user_input_image_path, content_json["bbox"])
