# ComfyUI-Hiero-Nodes
Just some random custom nodes I need/want to use and programmed for ComfyUI.

## Post w/ Discord Webhook Node

You will need a url to your discord channel's webhook, which can be retrieved by going to Edit Channel> Integrations> Webhooks> New Webhook. 
That will create a new webhook for that channel. You can get the URL for that webhook by clicking on "Copy Webhook URL".

This all requires you to have a Discord server and ability to edit a channel, which if you own the server in question you already have access to that.

### Disclaimer

I've since modified my node so that images sent through this node have it's webhook url replaced to nyan.cat, however, if you just share the workflow with this node you WILL share your private webhook url. Please excerise caution and remove this node from your workflow before you share it with the public space.

## Save Prompt Travel File Node

I wanted a way to save a text file with the prompting for each frame in a video (to be used in AnimateDiff video generation). I tried a couple of ways to do it and I wasn't feeling it, so I made my own solution. For the prompts I just pass each frame through an WD14 Tagger node

## Load Prompt Travel File Node

Again, made to use in video generation. Right now I have it made so that it actually adds in the frame number for each prompt when loaded, instead of it being saved that way. I did this so that I can start at any point in my collection of prompts and have it be referenced as the first frame and etc. 

I find the Batch Prompt Schelude node from FizzNodes works great with this. 