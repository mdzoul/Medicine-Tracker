# Medication Tracker CLI

A command-line application for managing and tracking medications, including expiry dates, with prioritized alerts and fuzzy search capabilities.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)

## Introduction

Medication Tracker CLI is a command-line tool designed to help users effectively manage their medications and keep track of expiry dates. It provides a simple and proactive approach to medication management, ensuring users prioritize expired medications and are notified of upcoming expiries, and also a fast way to access the information through the CLI.

## Features

- **Command-Line Interface (CLI):**
   An easy-to-use text-based interface for managing medications.
-   **Medication Management:**
    -   Add new medication entries, including brand name, medication name, expiry date (YYYY/MM), location, and optional notes.
    -   View all medication records in a structured list.
    -   Edit existing medication entries based on their IDs.
    -   Delete medication records.
-   **Prioritized Expiry Alerts:**
    -   Displays an alert for medications that have expired today first.
    -   Then displays an alert for medications expiring within the next month.
    -   Then displays an alert for medications expiring within the next two months.
    -   If none of the above is true, displays an alert for the medication(s) with the soonest expiry date.
- **Fuzzy Search:**
    - Allows partial-match searching by brand name and medication name using regular expressions.
-   **Modular Codebase:**
    -   The codebase has been refactored using classes, in separate files, for better organization, maintainability and extensibility.
-   **Database Persistence:** Utilizes SQLite for local storage of medication data, ensuring data persistence across sessions.
-   **Background WhatsApp Alerts**
    - Sends scheduled monthly WhatsApp alerts with the status of the medication expiries.

## Installation

To install and run the Medication Tracker CLI, follow these steps:

1.  Clone the repository:
    ```sh
    git clone https://github.com/mdzoul/medicine-tracker.git
    ```
2.  Navigate to the project directory:
    ```sh
    cd medicine-tracker
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To run the Medication Tracker CLI, execute the script from your terminal:

```sh
python med_tracker.py
```

This application will then show you a menu that you can navigate by typing numbers.

## Configuration

Before using the app, ensure you have set up the following:

- Twilio Account: Create a free Twilio account at [https://www.twilio.com/](https://www.twilio.com/).
- Twilio Phone Number: Get a Twilio phone number that is WhatsApp enabled.
- WhatsApp Sandbox: Connect your personal WhatsApp number to the Twilio sandbox.
- Twilio Credentials: Add the following as repository secrets in the "Settings > Secrets > Actions" section of your GitHub repository:
    - `TWILIO_ACCOUNT_SID`
    - `TWILIO_AUTH_TOKEN`
    - `TWILIO_PHONE_NUMBER`
    - `WHATSAPP_TO_NUMBER`

**Optional**

- You can also use environment variables for local testing. Add the same secrets mentioned above to your local environment to test the Twilio logic.

## Future Enhancements

The following features are currently planned for future enhancements:

- GUI interface for more user-friendly experience.
- Additional alert customization and settings.
- Cloud database capabilities

## Contributors

- [Zoul Aimi](https://github.com/mdzoul) - Creator and main contributor

