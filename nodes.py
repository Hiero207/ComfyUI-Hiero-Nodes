import os
import tempfile
import shutil
import json
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
                "URI": (
                    "STRING",
                    {"default": "Discord Webhook URI", "multiline": False},
                ),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "post_via_webhook"
    CATEGORY = "Hiero Nodes"

    def post_via_webhook(self, images, URI, prompt, extra_pnginfo=None):

        temp_dir = tempfile.mkdtemp()
        parsed_uri = URI.replace("\\", "")
        wh = DiscordWebhook(url=parsed_uri, content="")
        counter = 0

        for image in images:
            array = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(array, 0, 255).astype(np.uint8))

            metadata = PngInfo()
            metadata.add_text("prompt", json.dumps(prompt))
            file_name = f"Preview_{counter}.png"
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
      