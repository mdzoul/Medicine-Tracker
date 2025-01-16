# Medication Tracker Web App

A single-page web application for managing and tracking medications, including expiry dates, with prioritized alerts, fuzzy search, and in-place editing.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Running the Scheduled Alerts](#running-the-scheduled-alerts)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)

## Introduction

Medication Tracker Web App is a web application designed to help users effectively manage their medications and keep track of expiry dates. It provides a simple and proactive approach to medication management, ensuring users prioritize expired medications and are notified of upcoming expiries. This version combines all the functionalities into one single page, but also includes an alternative view for a dedicated list of all medications.

## Features

- **Single-Page Web Interface:**
  - A single HTML page to interact with all the features of the medication tracker.
- **Medication Management:**
  - Add new medication entries, including brand name, medication name, expiry date (YYYY/MM), location, and optional notes.
  - View all medication records in a filterable and sortable list.
  - Edit existing medication entries with an integrated interface directly within the medication list.
  - Delete medication records.
- **Prioritized Expiry Alerts:**
  - Displays a prominent alert for medications that have expired today.
  - Displays an alert for medications expiring within the next month or two.
  - Provides a way to edit expired medications directly from the main page.
- **Fuzzy Search:**
  - Allows partial-match searching by brand name, medication name or location, using regular expressions.
- **Database Persistence:** Utilizes SQLite for local storage of medication data, ensuring data persistence across sessions.
- **Alternative Medication View:**
  - Includes a dedicated view for medications only, located at `/medications`, with the alerts, the sort, and the filtering logic.
- **Monthly Telegram Notifications:**
  - Has a separate script to trigger monthly Telegram notifications.

## Installation

To install and run the Medication Tracker CLI, follow these steps:

1.  Clone the repository:
    ```sh
    git clone https://github.com/mdzoul/Medicine-Tracker.git
    ```
2.  Navigate to the project directory:
    ```sh
    cd Medicine-Tracker
    ```
3.  Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4.  **Add Your CSV File:** Place your medication data in a CSV file named `BCStockExpiry.csv` in the root folder of the project. Make sure the file has the following headings: `Brand`, `Name`, `Expiry`, `Location`, and `Notes`.
5.  **Configure `runmefirst.py`**: Update the `runmefirst.py` file and set the name of your CSV file in this line: `CSV_FILENAME = "your_csv_file.csv"`.
6.  **Create and populate the database:** Run the following script to create and populate `medications.db`
    ```sh
    python runmefirst.py
    ```
7.  **Deploy the Webapp** Now your database is ready, and you can run the webapp.
    ```sh
    python app.py
    ```

## Usage

To access the Medication Tracker, open your web browser and go to the URL specified in your terminal when the application starts (usually http://127.0.0.1:5000).
The web application will present the medications in a table format, and you will be able to search, sort, add, edit and delete medications.

## Configuration

Before using the app, ensure you have set up the following:

- **Telegram Bot:** Create a Telegram bot using BotFather, and save the bot's API token and your chat id.
- **Telegram Credentials:** Add the following as **repository secrets** in the "Settings > Secrets > Actions" section of your GitHub repository:
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`

**Optional**

- You can also use environment variables for local testing. Add the same secrets mentioned above to your local environment to test the Telegram alerts.

## Running the Scheduled Alerts

The monthly alerts are handled by a separate script and can be triggered by using a scheduling system provided by services such as PythonAnywhere or similar.

To send the alerts, execute the following script in your schedule:

```sh
python alerts.py
```

## Future Enhancements

The following features are currently planned for future enhancements:

- More advanced search and filter options.
- Cloud database capabilities.
- User authentication and authorization.
- Additional alert customization and settings.

## Contributors

- [Zoul Aimi](https://github.com/mdzoul) - Creator and main contributor
