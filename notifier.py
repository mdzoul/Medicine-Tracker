"""
This module handles sending notifications using Telegram.
It uses the python-telegram-bot library to connect to Telegram's API, 
handle incoming messages, and send messages.
"""

import os

from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters

load_dotenv()


class TelegramNotifier:
    """Manages Telegram messaging."""

    def __init__(self):
        self.bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID")

        if not all([self.bot_token, self.chat_id]):
            print("Error: Telegram environment variables not set.")
            self.bot = None
        else:
            self.bot = Bot(token=self.bot_token)

    async def send_telegram_alert(self, expiry_alerts):
        """Sends a Telegram alert with medication expiry information."""
        if not self.bot:
            return

        message_body = "Medication Expiry Alerts:\n\n"

        if expiry_alerts["expired"]:
            message_body += "---\nAlert: The following medications have expired today. Please edit or delete:\n"
            for med in expiry_alerts["expired"]:
                message_body += (
                    f"   - ID:{med[0]}, Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}\n"
                )

        if expiry_alerts["expiring_in_one_month"]:
            message_body += "---\nAlert: The following medication(s) expire within the next month:\n"
            for med in expiry_alerts["expiring_in_one_month"]:
                message_body += (
                    f"   - ID:{med[0]}, Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}\n"
                )

        if expiry_alerts["expiring_in_two_months"]:
            message_body += "---\nAlert: The following medication(s) expire within the next two months:\n"
            for med in expiry_alerts["expiring_in_two_months"]:
                message_body += (
                    f"   - ID:{med[0]}, Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}\n"
                )

        if (
            expiry_alerts["closest_expiry"]
            and not expiry_alerts["expiring_in_one_month"]
            and not expiry_alerts["expiring_in_two_months"]
        ):
            message_body += "---\nAlert: The following medication(s) have the soonest expiry date:\n"
            for med in expiry_alerts["closest_expiry"]:
                message_body += (
                    f"   - ID:{med[0]}, Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}\n"
                )

        if (
            not expiry_alerts["expired"]
            and not expiry_alerts["expiring_in_one_month"]
            and not expiry_alerts["expiring_in_two_months"]
            and not expiry_alerts["closest_expiry"]
        ):
            message_body += "---\nNo medications found or no valid expiry dates.\n"

        await self.bot.send_message(chat_id=self.chat_id, text=message_body)
        print("Telegram alert sent.")

    async def handle_message(self, update, context):
        """Handles incoming messages to the telegram bot"""
        chat_id = update.effective_chat.id
        text = update.message.text

        if text == "/start":
            await self.bot.send_message(
                chat_id=chat_id,
                text="Welcome to the Medication Tracker Bot.\n\n Use /help to see all the available commands",
            )
        elif text == "/help":
            await self.bot.send_message(
                chat_id=chat_id,
                text="Available commands are: \n\n /add - add a new medication \n /view - view all medications \n /edit - edit a medication \n /delete - delete a medication \n /search - search for a medication",
            )

        else:
            await self.bot.send_message(
                chat_id=chat_id,
                text="Invalid Command, use /help to see the list of commands available.",
            )
