import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFont
from PIL.PngImagePlugin import PngInfo
import os, json
from discord_webhook import DiscordWebhook

class PostViaWebhook:
  
  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
        "images": {"IMAGE", },
        "URI": ("STRING", {"default": "Discord Webhook URI"}),
      },
      "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
    }
  
  RETURN_TYPES = ()
  OUTPUT_NODE = True
  FUNCTION = "post_via_webhook"
  CATEGORY = "Hiero Nodes"
  
  def post_via_webhook(self, images, URI, prompt=None, extra_pnginfo=None):
    
    wh = DiscordWebhook(url=URI)
    
    results = list()
    for image in images:
      array = 255. * image.cpu().numpy()
      img = Image.fromarray(numpy.clip(array, 0, 255).astype(numpy.uint8))
      metadata = PngInfo()
      metadata.add_text("prompt", json.dumps(prompt))
      results.append(metadata)
      #wh.add_file(file=img)
      #send_post(wh)
    
    return {"ui": {"images": results}}