import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()  # add this to load the .env file


class TwilioNotifier:
    """Manages WhatsApp messaging."""

    def __init__(self):
        self.account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.twilio_number = os.environ.get("TWILIO_PHONE_NUMBER")
        self.to_number = os.environ.get("WHATSAPP_TO_NUMBER")

        if not all([self.account_sid,
                    self.auth_token,
                    self.twilio_number,
                    self.to_number]):
            print("Error: Twilio environment variables not set.")
            self.client = None
        else:
            self.client = Client(self.account_sid, self.auth_token)

    def send_whatsapp_alert(self, expiry_alerts):
        """Sends a WhatsApp alert with medication expiry information."""
        if not self.client:
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

        message = self.client.messages.create(
            from_=f"whatsapp:{self.twilio_number}",
            body=message_body,
            to=f"whatsapp:{self.to_number}"
        )
        print(f"WhatsApp alert sent. SID: {message.sid}")
