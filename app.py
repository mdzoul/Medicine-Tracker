import asyncio
import datetime
import re
import sqlite3

from dateutil.relativedelta import relativedelta
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from database import MedicationDatabase
from notifier import TelegramNotifier


class MedicationTrackerApp:
    """Manages the UI and orchestrates app logic."""

    def __init__(self):
        self.db = MedicationDatabase()
        self.notifier = TelegramNotifier()

    def get_expiry_alerts(self):
        """Gets medications with the closest expiry date, within one month, and within two months."""
        conn = sqlite3.connect(self.db.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medications")
        medications = cursor.fetchall()
        conn.close()

        today = datetime.date.today()
        one_month_later = today + relativedelta(months=1)
        two_months_later = today + relativedelta(months=2)

        expired_meds = []
        expiring_in_one_month_meds = []
        expiring_in_two_months_meds = []
        closest_expiry_meds = []
        closest_expiry_date = None

        for medication in medications:
            try:
                expiry_date = datetime.datetime.strptime(medication[3], "%Y/%m").date()
            except ValueError:
                continue

            if expiry_date <= today:
                expired_meds.append(medication)
            elif today < expiry_date <= one_month_later:
                expiring_in_one_month_meds.append(medication)
            elif today < expiry_date <= two_months_later:
                expiring_in_two_months_meds.append(medication)

            if closest_expiry_date is None or expiry_date < closest_expiry_date:
                closest_expiry_date = expiry_date
                closest_expiry_meds = [medication]  # new min date, reset list
            elif expiry_date == closest_expiry_date:
                closest_expiry_meds.append(
                    medication
                )  # same min date, append to the list

        return {
            "expired": expired_meds,
            "expiring_in_one_month": expiring_in_one_month_meds,
            "expiring_in_two_months": expiring_in_two_months_meds,
            "closest_expiry": closest_expiry_meds,
        }

    async def display_alerts(self, update, context, expiry_alerts):
        """Displays the alerts."""
        chat_id = update.effective_chat.id
        message = ""
        if expiry_alerts["expired"]:
            message += "Alert: The following medications have expired today. Please edit or delete:\n"
            for med in expiry_alerts["expired"]:
                message += (
                    f"   - ID:{med[0]}, Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}\n"
                )
            message += (
                "You must edit or delete these medications before adding new ones.\n\n"
            )

        if expiry_alerts["expiring_in_one_month"]:
            message += (
                "Alert: The following medication(s) expire within the next month:\n"
            )
            for med in expiry_alerts["expiring_in_one_month"]:
                message += (
                    f"   - ID:{med[0]}, Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}\n"
                )
            message += "\n"

        if expiry_alerts["expiring_in_two_months"]:
            message += "Alert: The following medication(s) expire within the next two months:\n"
            for med in expiry_alerts["expiring_in_two_months"]:
                message += (
                    f"   - ID:{med[0]}, Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}\n"
                )
            message += "\n"

        if (
            expiry_alerts["closest_expiry"]
            and not expiry_alerts["expiring_in_one_month"]
            and not expiry_alerts["expiring_in_two_months"]
        ):
            message += (
                "Alert: The following medication(s) have the soonest expiry date:\n"
            )
            for med in expiry_alerts["closest_expiry"]:
                message += (
                    f"   - ID:{med[0]}, Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}\n"
                )
            message += "\n"

        if (
            not expiry_alerts["expired"]
            and not expiry_alerts["expiring_in_one_month"]
            and not expiry_alerts["expiring_in_two_months"]
            and not expiry_alerts["closest_expiry"]
        ):
            message += "No medications found or no valid expiry dates.\n"

        await context.bot.send_message(chat_id=chat_id, text=message)

    async def handle_add_medication(self, update, context):
        """Handles the add medication logic."""
        chat_id = update.effective_chat.id
        expiry_alerts = self.get_expiry_alerts()
        if expiry_alerts["expired"]:
            await context.bot.send_message(
                chat_id=chat_id,
                text="You must edit or delete expired medications before adding new ones.",
            )
        else:
            await self.cli_add_medication(update, context)

    async def handle_edit_medication(self, update, context, medication_id=None):
        """Handles the edit medication logic"""
        chat_id = update.effective_chat.id
        expiry_alerts = self.get_expiry_alerts()
        if expiry_alerts["expired"]:
            try:
                med_id = int(context.args[0])
                if any(med[0] == med_id for med in expiry_alerts["expired"]):
                    await self.cli_edit_medication(update, context, med_id)
                else:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text="Invalid medication ID for expired medications.",
                    )
            except ValueError:
                await context.bot.send_message(
                    chat_id=chat_id, text="Invalid medication ID."
                )
        else:
            await self.cli_edit_medication(update, context)

    async def handle_start(self, update, context):
        """Handles the start command"""
        chat_id = update.effective_chat.id
        await context.bot.send_message(
            chat_id=chat_id,
            text="Welcome to the Medication Tracker Bot.\n\n Use /help to see all the available commands",
        )

    async def handle_help(self, update, context):
        """Handles the help command"""
        chat_id = update.effective_chat.id
        await context.bot.send_message(
            chat_id=chat_id,
            text="Available commands are: \n\n /add - add a new medication \n /view - view all medications \n /edit <id> - edit a medication \n /delete <id> - delete a medication \n /search <search term> - search for a medication",
        )

    async def cli_add_medication(self, update, context):
        """Interactively prompts the user to add a new medication."""
        chat_id = update.effective_chat.id
        brand_name = await self.prompt_user(chat_id, context, "Enter brand name:")
        medication_name = await self.prompt_user(
            chat_id, context, "Enter medication name:"
        )
        expiry_date_str = await self.prompt_user(
            chat_id, context, "Enter expiry date (YYYY/MM):"
        )

        # Input validation for date format
        try:
            datetime.datetime.strptime(expiry_date_str, "%Y/%m")
        except ValueError:
            await context.bot.send_message(
                chat_id=chat_id, text="Invalid date format. Please use YYYY/MM."
            )
            return

        location = await self.prompt_user(chat_id, context, "Enter location:")
        notes = await self.prompt_user(
            chat_id, context, "Enter notes (optional, press Enter to skip):"
        )
        self.db.add_medication(
            brand_name,
            medication_name,
            expiry_date_str,
            location,
            notes if notes else None,
        )
        await context.bot.send_message(
            chat_id=chat_id, text="Medication added successfully!"
        )

    async def cli_edit_medication(self, update, context, medication_id=None):
        """Interactively prompts the user to edit an existing medication."""
        chat_id = update.effective_chat.id

        if medication_id is None:
            medications = self.db.view_medications()  # gets list of all meds
            if not medications:
                await context.bot.send_message(
                    chat_id=chat_id, text="No medications found."
                )
                return

            med_text = "List of medications to edit:\n\n"
            for medication in medications:
                med_text += f"   - ID:{medication[0]}, Brand:{medication[1]}, Med:{medication[2]}, Expiry:{medication[3]}\n"

            await context.bot.send_message(chat_id=chat_id, text=med_text)
            try:
                medication_id = int(
                    await self.prompt_user(
                        chat_id, context, "Enter the ID of the medication to edit:"
                    )
                )
            except ValueError:
                await context.bot.send_message(
                    chat_id=chat_id, text="Invalid medication ID."
                )
                return

        medication = self.db.get_medication_by_id(medication_id)
        if not medication:
            await context.bot.send_message(
                chat_id=chat_id, text="Medication not found."
            )
            return

        message_body = "Current medication details:\n"
        message_body += f"  Brand Name: {medication[1]}\n"
        message_body += f"  Medication Name: {medication[2]}\n"
        message_body += f"  Expiry Date: {medication[3]}\n"
        message_body += f"  Location: {medication[4]}\n"
        message_body += f"  Notes: {medication[5] if medication[5] else 'No notes'}\n"
        await context.bot.send_message(chat_id=chat_id, text=message_body)

        brand_name = (
            await self.prompt_user(
                chat_id,
                context,
                f"Enter new brand name (leave empty to keep '{medication[1]}'): ",
            )
            or medication[1]
        )
        medication_name = (
            await self.prompt_user(
                chat_id,
                context,
                f"Enter new medication name (leave empty to keep '{medication[2]}'): ",
            )
            or medication[2]
        )
        expiry_date_str = (
            await self.prompt_user(
                chat_id,
                context,
                f"Enter new expiry date (YYYY/MM, leave empty to keep '{medication[3]}'): ",
            )
            or medication[3]
        )

        # Input validation for date format
        try:
            if expiry_date_str != medication[3]:
                datetime.datetime.strptime(expiry_date_str, "%Y/%m")
        except ValueError:
            await context.bot.send_message(
                chat_id=chat_id, text="Invalid date format. Please use YYYY/MM."
            )
            return

        location = (
            await self.prompt_user(
                chat_id,
                context,
                f"Enter new location (leave empty to keep '{medication[4]}'): ",
            )
            or medication[4]
        )
        notes = await self.prompt_user(
            chat_id,
            context,
            f"Enter new notes (leave empty to keep '{medication[5] if medication[5] else ''}'): ",
        )
        notes = notes if notes else (medication[5] if medication[5] else None)

        self.db.update_medication(
            medication_id, brand_name, medication_name, expiry_date_str, location, notes
        )
        await context.bot.send_message(
            chat_id=chat_id, text="Medication updated successfully!"
        )

    async def cli_delete_medication(self, update, context):
        """Interactively prompts the user to delete a medication."""
        chat_id = update.effective_chat.id
        medications = self.db.view_medications()
        if not medications:
            await context.bot.send_message(
                chat_id=chat_id, text="No medications found."
            )
            return

        med_text = "List of medications to delete:\n\n"
        for medication in medications:
            med_text += f"   - ID:{medication[0]}, Brand:{medication[1]}, Med:{medication[2]}, Expiry:{medication[3]}\n"

        await context.bot.send_message(chat_id=chat_id, text=med_text)
        try:
            medication_id = int(
                await self.prompt_user(
                    chat_id, context, "Enter the ID of the medication to delete:"
                )
            )
        except ValueError:
            await context.bot.send_message(
                chat_id=chat_id, text="Invalid medication ID."
            )
            return

        medication = self.db.get_medication_by_id(medication_id)
        if not medication:
            await context.bot.send_message(
                chat_id=chat_id, text="Medication not found."
            )
            return

        confirmation = await self.prompt_user(
            chat_id,
            context,
            f"Are you sure you want to delete {medication[2]}? (y/n): ",
        )
        if confirmation.lower() == "y":
            self.db.delete_medication(medication_id)
            await context.bot.send_message(
                chat_id=chat_id, text="Medication deleted successfully!"
            )
        else:
            await context.bot.send_message(chat_id=chat_id, text="Deletion cancelled.")

    async def cli_view_medications(self, update, context):
        """Interactively prompts the user to view all medications."""
        chat_id = update.effective_chat.id
        search_term = None
        if context.args:
            search_term = " ".join(context.args)
        medications = self.db.view_medications(search_term)
        if medications:
            message_body = ""
            if search_term:
                message_body += f"Search results for '{search_term}':\n\n"
            else:
                message_body += "List of medications:\n\n"

            for medication in medications:
                message_body += f"   - ID:{medication[0]}, Brand:{medication[1]}, Med:{medication[2]}, Expiry:{medication[3]}\n"
            await context.bot.send_message(chat_id=chat_id, text=message_body)

    async def prompt_user(self, chat_id, context, text):
        """Prompts the user for input"""
        await context.bot.send_message(chat_id=chat_id, text=text)
        response = await self.wait_for_response(chat_id, context)
        return response

    async def wait_for_response(self, chat_id, context):
        """Aux function to wait for the next user input"""
        response = None

        def receive_message(update, context):
            nonlocal response
            if update.effective_chat.id == chat_id:
                response = update.message.text
                return True  # this will cancel the handler
            return False  # this will not cancel the handler

        handler = MessageHandler(filters.TEXT, receive_message)
        context.dispatcher.add_handler(handler)
        while not response:
            await asyncio.sleep(0.1)
        context.dispatcher.remove_handler(handler)
        return response

    async def run(self):
        """Runs the main telegram bot loop"""
        self.db.create_database()

        application = (
            Application.builder()
            .token("7924544288:AAFmv6P-OhHTWX1cVdR05iYKdabHtUs6gus")
            .build()
        )

        application.add_handler(CommandHandler("start", self.handle_start))
        application.add_handler(CommandHandler("help", self.handle_help))
        application.add_handler(CommandHandler("add", self.handle_add_medication))
        application.add_handler(CommandHandler("edit", self.handle_edit_medication))
        application.add_handler(CommandHandler("delete", self.cli_delete_medication))
        application.add_handler(CommandHandler("view", self.cli_view_medications))
        application.add_handler(CommandHandler("search", self.cli_view_medications))
        application.add_handler(
            MessageHandler(filters.TEXT, self.notifier.handle_message)
        )

        print("Telegram bot is running...")
        application.run_polling()
