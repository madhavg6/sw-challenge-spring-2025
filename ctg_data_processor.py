import os
import csv
from datetime import datetime, timedelta
from collections import defaultdict

class TickDataProcessor:
    """
    Processes tick data from CSV files, clean the data
    Aggregates it into OHLCV format, and save the processed data to a CSV file
    """

    def __init__(self, data_folder):
        # Initialize the processor with the path to the data folder
        # Folder contains multiple CSV files with tick data
        self.data_folder = data_folder
        self.data = [] # List to store tick data after loading

    def load_data(self):
        """
        Loads tick data from all CSV files in the specified folder
        Reads each file line by line to extract relevant tick data
        """
        all_files = [f for f in os.listdir(self.data_folder) if f.endswith(".csv")] # Gets all CSV files
        print(f"Found {len(all_files)} CSV files.") # Prints number of CSV files found

        for file in all_files:
            file_path = os.path.join(self.data_folder, file) # Constructs full file path
            with open(file_path, "r") as f:
                reader = csv.reader(f)
                next(reader)  # Skip the first row (header row)
                for row in reader:
                    try:
                        # Extracts timestamp, price, and volume from each row
                        timestamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f") # Parses timestamp
                        price = float(row[1]) # Converts price to a float
                        volume = int(row[2]) # Converts volume to an int
                        self.data.append((timestamp, price, volume)) # Stores extracted data
                    except (ValueError, IndexError):
                        continue  # Skips rows with missing data

        print(f"Loaded {len(self.data)} rows.")

    def clean_data(self):
        """
        Cleans the tick data by removing invalid entries and sorting it chronologically
        Removes entries with non-positive prices or volumes
        """
        cleaned_data = [] # List to store only valid tick data

        for timestamp, price, volume in self.data:
            if price <= 0 or volume <= 0:  # Removes invalid prices/volumes
                continue
            cleaned_data.append((timestamp, price, volume))

        self.data = sorted(cleaned_data, key=lambda x: x[0])  # Sorts by timestamp
        print(f"After cleaning: {len(self.data)} rows remain.")

    def aggregate_data(self, interval_str):
        # Aggregates tick data into OHLCV bars based on a given time interval
        interval = self.parse_interval(interval_str) # Convert interval string to timedelta

        # Dictionary to store OHLCV data where keys are time intervals (buckets)
        ohlcv = defaultdict(lambda: [None, float("-inf"), float("inf"), None, 0])

        for timestamp, price, volume in self.data:
            # Determines the bucket time by rounding down to the nearest interval
            bucket_time = timestamp - timedelta(
                seconds=timestamp.second % interval.total_seconds(),
                microseconds=timestamp.microsecond
            )

            if ohlcv[bucket_time][0] is None:
                ohlcv[bucket_time][0] = price # Sets open price (first trade in interval)
            ohlcv[bucket_time][1] = max(ohlcv[bucket_time][1], price)  # Updates high price (max)
            ohlcv[bucket_time][2] = min(ohlcv[bucket_time][2], price)  # Updates low price (min)
            ohlcv[bucket_time][3] = price  # Sets close price (last trade in interval)
            ohlcv[bucket_time][4] += volume  # Sums up total traded volume in the interval

        # Convert dictionary to sorted list of tuples for CSV export
        self.data = [(ts, *values) for ts, values in sorted(ohlcv.items())]

        print(f"Aggregated into {len(self.data)} OHLCV bars.") # Prints total bars generated

    def save_to_csv(self, output_file):
        # Saves the aggregated OHLCV data to a new CSV file
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "open", "high", "low", "close", "volume"]) # Writes header row
            writer.writerows(self.data) # Write processed data rows

        print(f"Saved {len(self.data)} rows to {output_file}.") # Print confirmation message

    @staticmethod
    def parse_interval(interval_str):
        """
        Converts a human-readable interval string into a timedelta object
        Supports seconds, minutes, hours, and days
        """
        units = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days"} # Defines units that can be used
        total_seconds = 0 # Initializes total seconds count

        num = "" # Buffers for numeric part of the interval
        for char in interval_str:
            if char.isdigit():
                num += char # Builds numeric value as string
            elif char in units:
                total_seconds += int(num) * timedelta(**{units[char]: 1}).total_seconds() # Converts and sums up time
                num = "" # Resets buffer for the next unit

        return timedelta(seconds=total_seconds) # Returns timedelta object representing the interval

if __name__ == "__main__":
    # Main execution block to process the tick data
    processor = TickDataProcessor("./data") # Initialize processor with the data folder path
    processor.load_data() # Load tick data from all available CSV files
    processor.clean_data() # Remove invalid data and ensure correct ordering
    processor.aggregate_data("1m")  # Can modify time interval to liking (used 1m for basic)
    processor.save_to_csv("aggregated_data.csv") # Saves processed data to CSV file