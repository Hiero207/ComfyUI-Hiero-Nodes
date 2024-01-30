"""Main file for my ComfyUI nodes"""
import os
import tempfile
import shutil
import json
from datetime import datetime
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from discord_webhook import DiscordWebhook

class PostViaWebhook:
    """Class is used to send images to a Discord channel using a Discord Webhook"""

    @classmethod
    def INPUT_TYPES(cls):
        """Function sets up the inputs and outputs"""
        return {
            "required": {
                "images": ("IMAGE",),
                "URL": (
                    "STRING",
                    {"default": "Discord Webhook URI", "multiline": False},
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
        if enable == "True":
            temp_dir = tempfile.mkdtemp()
            parsed_uri = URL.replace("\\", "")
            wh = DiscordWebhook(url=parsed_uri, content="")
            counter = 0
            cur_date = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')

            for image in images:
                array = 255.0 * image.cpu().numpy()
                img = Image.fromarray(np.clip(array, 0, 255).astype(np.uint8))

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
