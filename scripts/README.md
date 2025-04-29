# WhatsApp Cinema Bot Scripts

This directory contains utility scripts for the WhatsApp Cinema Bot application.

## Log to Excel Converter

The `log_to_excel.py` script extracts booking information from the application logs and exports it to an Excel file.

### Features

- Automatically extracts phone numbers and ticket quantities from successful bookings
- Updates an Excel file with the latest booking information
- Runs continuously and checks for new bookings every 30 seconds
- Maintains a timestamp for each booking

### Usage

1. Make sure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```

2. Run the script:

```bash
python scripts/log_to_excel.py
```

The script will start monitoring the log file at `logs/app.log` and will create/update an Excel file at `data/bookings.xlsx` whenever new bookings are detected.

### Configuration

You can modify the following settings at the top of the script:

- `LOG_FILE_PATH`: Path to the log file (default: `logs/app.log`)
- `EXCEL_OUTPUT_PATH`: Path to the Excel output file (default: `data/bookings.xlsx`)
- `SCAN_INTERVAL_SECONDS`: How often to check for new bookings (default: 30 seconds)

### Example Output

The generated Excel file contains the following columns:

- `timestamp`: When the booking was made
- `phone_number`: The WhatsApp phone number that made the booking
- `ticket_count`: How many tickets were booked
- `location`: The cinema location

### Running as a Background Service

To run the script as a background service that starts automatically:

#### On Linux/macOS

Create a systemd service or use cron:

```bash
# Using cron (edit with crontab -e)
@reboot cd /path/to/app && python scripts/log_to_excel.py > /path/to/app/logs/excel_converter.log 2>&1
```

#### On Windows

Create a scheduled task or use a service manager like NSSM. 