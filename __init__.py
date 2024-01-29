import subprocess

subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

from .nodes import *

NODE_CLASS_MAPPINGS = {
  # Add mappings here
    "Post to Discord w/ Webhook": PostViaWebhook,
}

print("\033[34mComfyUI Hiero Nodes: \033[92mLoaded\033[0m")
