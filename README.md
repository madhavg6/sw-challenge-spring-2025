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


Data Cleaning:
-
- I identified four major data issues that needed to be addressed: 
  1. Invalid Prices or Volumes: Some trades had prices or volumes that were zero or negative, which are not possible in real market transactions. I iterated through the dataset and used an if condition to check if the price was <= 0 or if the volume was <= 0. If either condition was met, the row was skipped to ensure only valid trades were processed.
  2. Duplicate Entries: Some rows appeared more than once, which could distort analysis if not handled. For this, I stored processed trades in a set() using (timestamp, price, volume) as the key. Before adding a new row, I checked if it was already present in the set. This ensured only unique rows were retained.
  3. Corrupt or Incomplete Rows: Some rows had missing values, which could cause errors when processing. I implemented a try-except block when reading and processing each row to catch any errors due to missing or malformed data. If an error occurred (e.g., ValueError when converting strings to numbers), the row was skipped.
  4. Timestamp Inconsistencies: I saw some trades were not always in chronological order, which could impact time-series analysis from what I know. After cleaning, I sorted the dataset using Python’s sorted() function to ensure all trades appeared in chronological order.
