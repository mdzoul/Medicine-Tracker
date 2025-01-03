import os
from telegram import Bot
from dotenv import load_dotenv
import asyncio

load_dotenv()


class TelegramNotifier:
    """Manages WhatsApp messaging."""

    def __init__(self):
        self.bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID")

        if not all([self.bot_token,
                    self.chat_id]):
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
                message_body += f"   - ID:{med[0]}, Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}\n"

        if expiry_alerts["expiring_in_one_month"]:
            message_body += "---\nAlert: The following medication(s) expire within the next month:\n"
            for med in expiry_alerts["expiring_in_one_month"]:
                message_body += f"   - ID:{med[0]}, Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}\n"

        if expiry_alerts["expiring_in_two_months"]:
            message_body += "---\nAlert: The following medication(s) expire within the next two months:\n"
            for med in expiry_alerts["expiring_in_two_months"]:
                message_body += f"   - ID:{med[0]}, Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}\n"

        if expiry_alerts["closest_expiry"] and not expiry_alerts["expiring_in_one_month"] and not expiry_alerts["expiring_in_two_months"]:
            message_body += "---\nAlert: The following medication(s) have the soonest expiry date:\n"
            for med in expiry_alerts["closest_expiry"]:
                message_body += f"   - ID:{med[0]}, Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}\n"

        if not expiry_alerts["expired"] and not expiry_alerts["expiring_in_one_month"] and not expiry_alerts["expiring_in_two_months"] and not expiry_alerts["closest_expiry"]:
            message_body += "---\nNo medications found or no valid expiry dates.\n"

        await self.bot.send_message(chat_id=self.chat_id, text=message_body)
        print("Telegram alert sent.")
