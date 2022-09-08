from telethon import TelegramClient, events
from telethon.tl.types import InputChannel
import yaml
import asyncio

import aiohttp
import nextcord

message = None

with open('config.yml', 'rb') as f:
    config = yaml.safe_load(f)



"""
TELEGRAM CLIENT STUFF
"""
client = TelegramClient("forwardgram", config["api_id"], config["api_hash"])
client.start()

#Find input telegram channel
for d in client.iter_dialogs():
    if d.name in config["input_channel_name"]:
        input_channel = InputChannel(d.entity.id, d.entity.access_hash)
        break

#TELEGRAM NEW MESSAGE
@client.on(events.NewMessage())
async def handler(event):
    # If the message contains a URL, parse and send Message + URL
    try:
        parsed_response = (event.message.message + '\n' + event.message.entities[0].url )
        parsed_response = ''.join(parsed_response)
    # Or we only send Message    
    except:
        parsed_response = event.message.message

    globals()['message'] = parsed_response
    await send_to_webhook(parsed_response,"TipManager Bot")



"""
DISCORD CLIENT STUFF
"""
async def send_to_webhook(message,username): # Send message to webhook
    async with aiohttp.ClientSession() as session:
        print('Sending w/o media')
        webhook = nextcord.Webhook.from_url(config["webhook"], session=session)
        await webhook.send(content=message,username=username)



"""
RUN EVERYTHING ASYNCHRONOUSLY
"""

print("Listening now")
asyncio.run( client.run_until_disconnected() )
