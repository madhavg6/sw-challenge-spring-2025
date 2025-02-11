CTG Data Processing Documentation:

Data Cleaning:
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
- 
