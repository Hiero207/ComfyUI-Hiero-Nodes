"""Main file for my ComfyUI nodes"""
import os
import tempfile
import shutil
import json
from datetime import datetime
from pathlib import Path
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from discord_webhook import DiscordWebhook

class PostViaWebhook:
    """Class is used to send images to a Discord channel using a Discord Webhook"""

    @classmethod
    def INPUT_TYPES(cls):
        """Function sets up the inputs and outputs"""
        comfy_path = Path.cwd()
        settings_path = comfy_path / "custom_nodes" / "ComfyUI-Hiero-Nodes" / "settings.json"
        with open(settings_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        data_dict = json.loads(data)
        webhook_url = data_dict["webhook_url"]

        return {
            "required": {
                "images": ("IMAGE",),
                "URL": (
                    "STRING",
                    {"default": webhook_url, "multiline": False},
                ),
                "enable": (["True", "False"],)
            },
            "hidden": {"prompt": "PROMPT"},
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "post_via_webhook"
    CATEGORY = "Hiero Nodes"

    def post_via_webhook(self, images, URL, enable, prompt):
        """Function for sending image to discord channel"""
        comfy_path = Path.cwd()
        settings_path = comfy_path / "custom_nodes" / "ComfyUI-Hiero-Nodes" / "settings.json"
        data = f'{{ "webhook_url": "{URL}" }}'
        parsed_data = data.replace("\\", "")
        with open(settings_path, "w", encoding="utf-8") as file:
            json.dump(parsed_data, file, indent=4)

        if enable == "True":
            temp_dir = tempfile.mkdtemp()
            parsed_uri = URL.replace("\\", "")
            wh = DiscordWebhook(url=parsed_uri, content="")
            counter = 0
            cur_date = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')

            for image in images:
                array = 255.0 * image.cpu().numpy()
                img = Image.fromarray(np.clip(array, 0, 255).astype(np.uint8))

                for key, value in prompt.items():
                    if isinstance(value, dict):
                        for inner_key, inner_value in value.items():
                            if inner_key == "inputs" and isinstance(inner_value, dict) and "URL" in inner_value:
                                prompt[key]["inputs"]["URL"] = "https://www.nyan.cat/"
                
                print("Prompt info", prompt)
                metadata = PngInfo()
                metadata.add_text("prompt", json.dumps(prompt))
                
                file_name = f"ComfyUI_{cur_date}_{counter}.png"
                file_path = os.path.join(temp_dir, file_name)
                img_params = {
                    "png": {"compress_level": 4},
                    "webp": {"method": 6, "loseless": False, "quality": 80},
                    "jpg": {"format": "JPEG"},
                    "tif": {"format": "TIFF"},
                }
                img.save(file_path, **img_params["png"], pnginfo=metadata)

                with open(file_path, "rb") as f:
                    wh.add_file(file=f.read(), filename=file_name)
                counter += 1
            response = wh.execute()
            print(response)
            shutil.rmtree(temp_dir)
        return {}
