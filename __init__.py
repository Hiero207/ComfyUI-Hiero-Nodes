import subprocess
from pathlib import Path

comfy_path = Path.cwd()
req_path = comfy_path / "custom_nodes" / "ComfyUI-Hiero-Nodes" / "requirements.txt"
print(f"\033[34mComfyUI Hiero Nodes: \033[92mNode Requirements Path: {req_path}\033[0m")
print("\033[34mComfyUI Hiero Nodes: \033[92mInstalling required libraries\033[0m")
subprocess.check_call(["pip", "install", "-r", f"{req_path}"])


from .nodes import *

NODE_CLASS_MAPPINGS = {
  # Add mappings here
    "Post to Discord w/ Webhook": PostViaWebhook,
}

print("\033[34mComfyUI Hiero Nodes: \033[92mLoaded\033[0m")
