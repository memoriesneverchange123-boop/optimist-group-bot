#!/usr/bin/env python3
"""
Optimist Group Creator Bot - Railway Edition
Runs 24/7 on Railway.app
"""

import asyncio
import logging
import os
import sys
from telethon import TelegramClient, events
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.sessions import StringSession

# Configuration from environment variables
API_ID = int(os.environ.get("API_ID", "38661481"))
API_HASH = os.environ.get("API_HASH", "d642499d2e5f8ed52ac7b45ade397a8f")
SESSION_STRING = os.environ.get("SESSION_STRING", "")
YOUR_USERNAME = os.environ.get("YOUR_USERNAME", "iamretro123")
FRIEND_USERNAMES = os.environ.get("FRIEND_USERNAMES", "poggers6000,roxinft").split(",")

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

client = None


async def create_group_and_get_invite(group_name):
    global client
    full_name = group_name + " <> Optimists"
    result = await client(CreateChannelRequest(
        title=full_name,
        about="Group created via Optimist Group Creator Bot",
        megagroup=True
    ))
    channel = result.chats[0]
    logger.info("Created group: " + full_name)
    invite_result = await client(ExportChatInviteRequest(peer=channel, legacy_revoke_permanent=True))
    return invite_result.link, channel.id


async def send_invite_to_friends(invite_link, group_name):
    global client
    for username in FRIEND_USERNAMES:
        username = username.strip()
        if username:
            try:
                msg = "You've been invited to join '" + group_name + " <> Optimists'! Join here: " + invite_link
                await client.send_message(username, msg)
                logger.info("Sent invite to @" + username)
            except Exception as e:
                logger.error("Failed to send invite to @" + username + ": " + str(e))


async def main():
    global client
    logger.info("Starting Optimist Group Creator Bot...")
    
    if not SESSION_STRING:
        logger.error("SESSION_STRING not set!")
        return

    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    
    @client.on(events.NewMessage(pattern=r'/creates+(.+)', outgoing=True))
    async def handle_create(event):
        logger.info("Received /create command!")
        group_name = event.pattern_match.group(1).strip()
        if not group_name:
            await event.reply("Usage: /create GroupName")
            return
        await event.reply("Creating group: " + group_name + " <> Optimists...")
        try:
            invite_link, _ = await create_group_and_get_invite(group_name)
            await event.reply("Sending invites to friends...")
            await send_invite_to_friends(invite_link, group_name)
            await event.reply("Done! Invite link: " + invite_link)
            logger.info("Created group: " + group_name)
        except Exception as e:
            await event.reply("Error: " + str(e))
            logger.error("Failed to create group: " + str(e))

    try:
        await client.start()
        me = await client.get_me()
        logger.info("Logged in as: " + me.first_name + " (@" + me.username + ")")
        logger.info("Bot is now listening for /create commands...")
        
        # Keep running with periodic pings
        while True:
            await asyncio.sleep(60)
            logger.info("Bot still running...")
            
    except Exception as e:
        logger.error("Error: " + str(e))
    finally:
        if client:
            await client.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")