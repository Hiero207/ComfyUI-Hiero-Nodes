"""
@author: Hiero
@title: Hiero-Nodes
@nickname: HNodes
@version: 1.2
@project: "https://github.com/Hiero207/ComfyUI-Hiero-Nodes"
@description: Just some nodes that I wanted/needed, so I made them.
"""

import subprocess
import os

from pathlib import Path

comfy_path = Path.cwd()

cwd = comfy_path.parts[-1]
needed_dir = "ComfyUI"

if needed_dir!= cwd:
    # Tack on ComfyUI to the end of the path
    comfy_path = comfy_path / needed_dir

print(f"\033[34mComfyUI Hiero Nodes: \033[92mDir Path: {comfy_path}\033[0m")
req_path = comfy_path / "custom_nodes" / "ComfyUI-Hiero-Nodes" / "requirements.txt"
settings_path = comfy_path / "custom_nodes" / "ComfyUI-Hiero-Nodes" / "settings.json"
print(f"\033[34mComfyUI Hiero Nodes: \033[92mNode Requirements Path: {req_path}\033[0m")

# Ensure parent directory exists
settings_path.parent.mkdir(parents=True, exist_ok=True)

if not settings_path.is_file():
    print("\033[34mComfyUI Hiero Nodes: \033[31mSettings file not found. Creating default\033[0m")
    with settings_path.open("x", encoding="utf-8") as file:
        file.write('{ "webhook_url": "not set"}')
else:
    print(f"\033[34mComfyUI Hiero Nodes: \033[92mSettings Path: {settings_path}\033[0m")

# Check if running venv/portable python environment
venv_path = Path.cwd() / "python_embeded"
#print("venv_path", venv_path)
venv_pip_cmd = venv_path / "python.exe"
#print(venv_pip_cmd)

if venv_path.exists():
    print("PORTABLE")
    try:
        print("\033[34mComfyUI Hiero Nodes: \033[92mInstalling required libraries\033[0m")
        subprocess.check_call([str(venv_pip_cmd), "-s", "-m", "pip", "install", "-r", str(req_path)])
    except subprocess.CalledProcessError as e:
        print(f"\033[34mComfyUI Hiero Nodes: \033[92mError installing required libraries: {e}\033[0m")
else:
    print("NOT PORTABLE")
    try:
        print("\033[34mComfyUI Hiero Nodes: \033[92mInstalling required libraries\033[0m")
        subprocess.check_call(["pip", "install", "-r", str(req_path)])
    except subprocess.CalledProcessError as e:
        print(f"\033[34mComfyUI Hiero Nodes: \033[92mError installing required libraries: {e}\033[0m")

from .nodes import *

NODE_CLASS_MAPPINGS = {
# Add mappings here
    "Post to Discord w/ Webhook": PostViaWebhook,
    "Save Prompt Travel file": SavePromptTravelFile,
    "Load Prompt Travel file": LoadPromptTravelFile,
}

print("\033[34mComfyUI Hiero Nodes: \033[92mLoaded\033[0m")
