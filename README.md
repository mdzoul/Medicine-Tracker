# Medication Tracker CLI

A command-line application for managing and tracking medications, including expiry dates, with prioritized alerts and fuzzy search capabilities, and monthly Telegram notifications.

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

Medication Tracker CLI is a command-line tool designed to help users effectively manage their medications and keep track of expiry dates. It provides a simple and proactive approach to medication management, ensuring users prioritize expired medications, are notified of upcoming expiries, and also offers a fast way to access the information through the CLI. This version is now decoupled, separating the medication management from the monthly alerts.

## Features

- **Command-Line Interface (CLI):**
  An easy-to-use text-based interface for managing medications.
- **Medication Management:**
  - Add new medication entries, including brand name, medication name, expiry date (YYYY/MM), location, and optional notes.
  - View all medication records in a structured list.
  - Edit existing medication entries based on their IDs.
  - Delete medication records.
- **Prioritized Expiry Alerts:**
  - Displays an alert for medications that have expired today first.
  - Then displays an alert for medications expiring within the next month.
  - Then displays an alert for medications expiring within the next two months.
  - If none of the above is true, displays an alert for the medication(s) with the soonest expiry date.
- **Fuzzy Search:**
  - Allows partial match searching by brand name and medication name using regular expressions.
- **Modular Codebase:**
  - The codebase has been refactored using classes, in separate files, for better organization, maintainability and extensibility.
- **Database Persistence:** Utilizes SQLite for local storage of medication data, ensuring data persistence across sessions.
- **Telegram Notifications:**
  - Sends scheduled monthly Telegram alerts with the status of the medication expiries.

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
3.  Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To interact with the medication management, run the following script from your terminal:

```sh
python main.py
```

This application will then show you a menu that you can navigate by typing numbers.

## Configuration

The application will use the `medications.db` file to store all the information of your medications.

## Future Enhancements

The following features are currently planned for future enhancements:

- GUI interface for more user-friendly experience.
- Additional alert customization and settings.
- Cloud database capabilities

## Contributors

- [Zoul Aimi](https://github.com/mdzoul) - Creator and main contributor
