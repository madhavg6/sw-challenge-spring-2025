CTG Data Processing Documentation:

Data Loading:
-
- I identified all the CSV files in the given directory using os.listdir(), making sure to filter for files that end with .csv so I only process relevant data.
- I used csv.reader to open each file and read its content.
- Remaining rows are processed, extracting three key values:
  - timestamp: Converted from string to datetime object
  - price: Converted to a floating-point number
  - volume: Converted to an integer
- Any malformed or incomplete rows are ignored using exception handling (try except block used)
- Challenges: One issue I had was dealing with corrupt or incomplete data as some rows were missing values or had incorrect formatting. I solved this by using a try-except block to catch errors and skip problematic rows without crashing the program. Ensuring timestamp consistency was also important, so I used datetime.strptime() to standardize all timestamps, making it easier to sort and aggregate the data later.


Data Interface:
-
- I built this interface to process tick data and generate OHLCV (Open-High-Low-Close-Volume) bars based on custom time intervals.
- I let users specify time intervals (e.g., "5s", "15m", "2h", "1d", "1h30m") and define a time frame with start and end datetime values.
- Once processed, I export the OHLCV data as a CSV file for easy analysis.
  
- Functionality
  - Time Interval Input
    - I allow users to enter time intervals as strings, such as "10s" (10 seconds), "5m" (5 minutes), and "1h30m" (1 hour 30 minutes).
    - I convert the input into total seconds to standardize the aggregation process.
  - Time Frame Selection
    - I require users to provide a start and end datetime (e.g., "2024-02-01 09:30:00" to "2024-02-01 16:00:00").
    - I automatically filter out trades that fall outside this time range.
  - OHLCV Data Aggregation
    - I group tick data into time-based buckets according to the selected interval.
    - For each bucket, I calculate:
     - Open Price: The first trade price in the interval.
     - High Price: The highest trade price recorded in the interval.
     - Low Price: The lowest trade price recorded in the interval.
     - Close Price: The last trade price in the interval.
     - Volume: The total number of shares traded in the interval.
       
- Output Generation
  - I save the aggregated OHLCV data as a CSV file with the following format:
    
    - timestamp,open,high,low,close,volume
    - 2024-02-01 09:30:00,100.5,101.0,99.5,100.0,20
    - 2024-02-01 09:30:10,100.0,100.8,99.2,100.5,15

- Error Handling & Validation
 - I check if the time interval input follows the correct format and alert the user if it's invalid.
 - If the start or end datetime is missing or incorrect, I notify the user and prevent further processing.
 - If no trades exist within the specified time range, I display a message instead of generating an empty file.
 
- Assumptions & Limitations
 - I assume that all timestamps in the dataset are in chronological order; otherwise, sorting is required.
 - The interface is optimized for large datasets but may slow down if the interval is extremely short (e.g., "1s").
 - I currently output only CSV files, but additional formats like JSON could be added later.

- Usage Example
 - A user wants to generate OHLCV bars for "15m" intervals between "2024-02-01 09:30:00" and "2024-02-01 16:00:00".
 - I process the data, group trades into 15-minute intervals, calculate OHLCV values, and export the results as a CSV file.
 - The user can then load this file into their analysis tools for further evaluation.

