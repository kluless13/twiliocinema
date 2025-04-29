#!/usr/bin/env python3
"""
Log to Excel Converter
---------------------
Extracts booking information from app.log and exports it to Excel.
Runs every 30 seconds to keep the Excel file updated with the latest bookings.
"""

import os
import re
import time
import pandas as pd
from datetime import datetime
from pathlib import Path

# Configuration
LOG_FILE_PATH = Path("logs/app.log")
EXCEL_OUTPUT_PATH = Path("data/bookings.xlsx")
SCAN_INTERVAL_SECONDS = 30
BOOKING_PATTERN = r"New booking: (whatsapp:\+\d+), (\d+) tickets at (\w+)"

class LogToExcelConverter:
    """Converts log entries to Excel data"""
    
    def __init__(self, log_path, excel_path):
        """Initialize with file paths"""
        self.log_path = Path(log_path)
        self.excel_path = Path(excel_path)
        self.last_processed_line = 0
        self.bookings = []
        
        # Create directories if they don't exist
        self.excel_path.parent.mkdir(exist_ok=True)
    
    def extract_bookings_from_log(self):
        """Extract booking information from the log file"""
        if not self.log_path.exists():
            print(f"Log file not found: {self.log_path}")
            return []
        
        new_bookings = []
        try:
            with open(self.log_path, 'r') as file:
                # Skip to the last processed line
                lines = file.readlines()
                new_lines = lines[self.last_processed_line:]
                self.last_processed_line = len(lines)
                
                for line in new_lines:
                    match = re.search(BOOKING_PATTERN, line)
                    if match:
                        phone_number = match.group(1)
                        ticket_count = int(match.group(2))
                        location = match.group(3)
                        timestamp = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                        booking_time = timestamp.group(1) if timestamp else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        
                        new_bookings.append({
                            'timestamp': booking_time,
                            'phone_number': phone_number,
                            'ticket_count': ticket_count,
                            'location': location
                        })
                        print(f"Found new booking: {phone_number}, {ticket_count} tickets")
            
            # Add new bookings to the list
            if new_bookings:
                self.bookings.extend(new_bookings)
                
        except Exception as e:
            print(f"Error reading log file: {e}")
        
        return new_bookings
    
    def save_to_excel(self):
        """Save the bookings to an Excel file"""
        if not self.bookings:
            print("No bookings to save")
            return False
        
        try:
            # Create DataFrame from bookings
            df = pd.DataFrame(self.bookings)
            
            # Sort by timestamp
            df = df.sort_values(by='timestamp', ascending=False)
            
            # Save to Excel
            df.to_excel(self.excel_path, index=False, sheet_name="Bookings")
            print(f"Saved {len(self.bookings)} bookings to {self.excel_path}")
            return True
        except Exception as e:
            print(f"Error saving to Excel: {e}")
            return False
    
    def run_once(self):
        """Run a single cycle of extracting and saving"""
        new_bookings = self.extract_bookings_from_log()
        if new_bookings:
            self.save_to_excel()
    
    def run_continuously(self):
        """Run in a loop with a delay between iterations"""
        print(f"Starting log to Excel converter. Watching {self.log_path}")
        print(f"Saving bookings to {self.excel_path}")
        print(f"Checking every {SCAN_INTERVAL_SECONDS} seconds...")
        
        try:
            while True:
                self.run_once()
                time.sleep(SCAN_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("\nStopping log to Excel converter")
            # Save one last time before exiting
            self.save_to_excel()

def main():
    """Main entry point"""
    converter = LogToExcelConverter(LOG_FILE_PATH, EXCEL_OUTPUT_PATH)
    converter.run_continuously()

if __name__ == "__main__":
    main() 