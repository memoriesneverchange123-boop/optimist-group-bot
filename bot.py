#!/usr/bin/env python3
"""
Optimist Group Creator Bot - Railway Edition
Runs 24/7 on Railway.app
"""

import asyncio
import logging
import os
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

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_group_and_get_invite(client, group_name):
      full_name = f"{group_name} <> Optimists"
      result = await client(CreateChannelRequest(
          title=full_name,
          about="Group created via Optimist Group Creator Bot",
          megagroup=True
      ))
      channel = result.chats[0]
      logger.info(f"Created group: {full_name}")
      invite_result = await client(ExportChatInviteRequest(peer=channel, legacy_revoke_permanent=True))
      return invite_result.link, channel.id


async def send_invite_to_friends(client, invite_link, group_name):
      message = f"You've been invited to join: {group_name} <> Optimists\nJoin here: {invite_link}"
      for username in FRIEND_USERNAMES:
                username = username.strip()
                if not username:
                              continue
                          try:
                                        user = await client.get_entity(username)
                                        await client.send_message(user, message)
                                        logger.info(f"Sent invite to @{username}")
except Exception as e:
            logger.error(f"Failed to send to @{username}: {e}")


async def main():
      logger.info("Starting Optimist Group Creator Bot...")
      if not SESSION_STRING:
                logger.error("SESSION_STRING not set!")
                return

      client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
      await client.connect()

    if not await client.is_user_authorized():
              logger.error("Session invalid!")
              return

    me = await client.get_me()
    logger.info(f"Logged in as: {me.first_name} (@{me.username})")

    @client.on(events.NewMessage(pattern=r'/create\s+(.+)'))
    async def handle_create(event):
              sender = await event.get_sender()
              if sender.username and sender.username.lower() == YOUR_USERNAME.lower():
                            group_name = event.pattern_match.group(1).strip()
                            if not group_name:
                                              await event.reply("Usage: /create GroupName")
                                              return
                                          await event.reply(f"Creating group: {group_name} <> Optimists...")
                            try:
                                              invite_link, _ = await create_group_and_get_invite(client, group_name)
                                              await event.reply("Sending invites...")
                                              await send_invite_to_friends(client, invite_link, group_name)
                                              await event.reply(f"Done! Invite link: {invite_link}")
                                              logger.info(f"Created '{group_name}'")
except Exception as e:
                await event.reply(f"Error: {str(e)}")
                logger.error(f"Failed: {e}")

    await client.run_until_disconnected()


if __name__ == "__main__":
      asyncio.run(main())
