"""
@author: Hiero
@title: Hiero-Nodes
@nickname: HNodes
@version: 1.2
@project: "https://github.com/Hiero207/ComfyUI-Hiero-Nodes"
@description: Just some nodes that I wanted/needed, so I made them.
"""

import subprocess
from pathlib import Path

comfy_path = Path.cwd()
req_path = comfy_path / "custom_nodes" / "ComfyUI-Hiero-Nodes" / "requirements.txt"
settings_path = comfy_path / "custom_nodes" / "ComfyUI-Hiero-Nodes" / "settings.json"
print(f"\033[34mComfyUI Hiero Nodes: \033[92mNode Requirements Path: {req_path}\033[0m")

if not settings_path.is_file():
    print("\033[34mComfyUI Hiero Nodes: \033[31mSettings file not found. Creating default\033[0m")
    with settings_path.open("w", encoding="utf-8") as file:
        file.write('{ "webhook_url": "not set"}')
else:
    print(f"\033[34mComfyUI Hiero Nodes: \033[92mSettings Path: {settings_path}\033[0m")

print("\033[34mComfyUI Hiero Nodes: \033[92mInstalling required libraries\033[0m")
subprocess.check_call(["pip", "install", "-r", f"{req_path}"])

from .nodes import *

NODE_CLASS_MAPPINGS = {
  # Add mappings here
    "Post to Discord w/ Webhook": PostViaWebhook,
    "Save Prompt Travel file": SavePromptTravelFile,
    "Load Prompt Travel file": LoadPromptTravelFile,
}

print("\033[34mComfyUI Hiero Nodes: \033[92mLoaded\033[0m")
