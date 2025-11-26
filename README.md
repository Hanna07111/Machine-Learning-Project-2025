# Machine-Learning-Project-2025
project repository for 2025 fall semester machine learning course

## Extra Credit
A pipeline of data extraction -> feature engineering -> preprocessing -> model training -> model assessment.

### **extra_credit_main.py**:

- **Overview**

  This script loads .cell files from monitored (mon/) and unmonitored (unmon/) directories, extracts traffic features from each file, labels them, and appends all results into a single CSV file (all_features.csv).

  It is designed for the website fingerprinting (WF) feature engineering pipeline and works together with:

  - extra_credit_data_loader.py — provides load_one_cell()
  - extra_credit_feature_engineering.py — provides extract_all_features()

- **Directory structure**

  The directory structure should be like this:
  
    ```
    BASE/
     ├── mon/
     │     ├── .cell
     │     └── ...
     ├── unmon/
     │     ├── .cell
     │     └── ...
     ├── extra_credit_data_loader.py
     ├── extra_credit_feature_engineering.py
     └── feature_extraction_main.py
    ```
    
- **What the script does**
  
  1. Iterates through all .cell files in both mon/ and unmon/.
  2. Skips irrelevant files:
     
     files containing "join"

     files without "split"
  4. Loads each valid .cell sequence using load_one_cell().
  5. Validates the sequence shape (must be (T, 3) for (t, d, s)).
  6. Extracts numerical features using extract_all_features().
  7. Assigns labels:

     Monitored: label = site ID (e.g., "3-1_split_0" → 3)

     Unmonitored: label = 95
  9. Appends features row-by-row to all_features.csv.


- **Output**
  
  A CSV file with one row per .cell instance: ```all_features.csv```

  Note that you can change the file name by modifying:

  ```
  out_path = "all_features.csv"
  ```

- **How to Run**

  ```
  python extra_credit_main.py
  ```

  Modify the BASE path inside the script if your data directory differs.

- **Requirements**

  - Python 3.8+
  - pandas
  - numpy
  - your existing modules:
    - extra_credit_data_loader.py
    - extra_credit_feature_engineering.py
  
  Install standard packages if needed:
  ```
  
  pip install pandas numpy
  ```

  
