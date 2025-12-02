# Machine-Learning-Project-2025
project repository for 2025 fall semester machine learning course

## Data&Data Preprocessing
This directory contains all datasets used throughout our pipelines.
During the feature engineering stage, we extracted two intermediate files:

- [train_set_AB.csv](Data/train_set_AB.csv)

- [test_set_AB.csv](Data/test_set_AB.csv)

Using these files, we generated the final datasets for the model experiments:

- Closed-world: [closedworld_train.csv](Data/closedworld_train.csv), [closedworld_test.csv](Data/closedworld_test.csv)

- Open-world: [openworld_train.csv](Data/openworld_train.csv), [openworld_test.csv](Data/openworld_test.csv)

We also perform basic preprocessing steps—such as clipping and scaling—using
the following notebook:

- [Data Preprocessing Notebook](Data%20Preprocessing/DataPreprocessing.ipynb)

You can reproduce all experimental datasets (closedworld_* and openworld_*) from
train_set_AB.csv and test_set_AB.csv by running this notebook.

## Data Analysis

This section provides EDA notebooks to visualize and analyze network traffic patterns, distributions, and feature correlations for both monitored and unmonitored datasets. All experiments were conducted using an NVIDIA T4 GPU on Google Colab and a local environment utilizing torch-directml.

| Target Data | Notebook |
| :--- | :--- |
| **Monitored** | [monitored_analysis.ipynb](Feature%20Engineering/monitored_analysis.ipynb) |
| **Unmonitored** | [unmonitored_analysis.ipynb](Feature%20Engineering/unmonitored_analysis.ipynb) |

## Feature Engineering

This directory contains scripts and notebooks for extracting meaningful features from raw traffic data (`.pkl`) and generating datasets (`.csv`) for model training. All experiments were conducted using an NVIDIA T4 GPU on Google Colab and a local environment utilizing torch-directml.

**⚠️ Usage Note:** You must run **`feature_engineering_v0_5.py`** first to generate the `train_set_AB.csv` and `test_set_AB.csv` files required for other notebooks. If you prefer, you may skip this step and simply use the pre-generated data provided in the Data/ directory.

| Step | Script / Notebook | Description |
| :--- | :--- | :--- |
| **1. Extraction & Generation** | [feature_engineering_v0_5.ipynb](./Feature%20Engineering/feature_engineering_v0_5.ipynb) | **(Main)** Extracts Non-leaky (18) & Fingerprint (8) features. Generates final CSV datasets (`Set A`, `Set B`, `Set A+B`). |
| **2. Validation** | [feature_engineering_v1.ipynb](./Feature%20Engineering/feature_engineering_v1.ipynb) | Validates feature sets and evaluates baseline model performance using the generated CSVs. |
| **3. Initial Selection** | [feature_engineering_v0.ipynb](./Feature%20Engineering/feature_engineering_v0.ipynb) | (Legacy) Initial feature selection using correlation analysis. |

## Models
This directory provides .ipynb files for training and evaluating the performance of each model.
All experiments were conducted using a CPU / NVIDIA T4 GPU on Google Colab.

**⚠️ Usage Note:** Before running any notebook, update the train/test data path according to your environment.

### Baseline
| Model | Closed World | Open World |
| :----: | :----: | :----: |
|  XGBoost |[Notebook](Models/Baseline/XGBoost_closed-world.ipynb)|[Notebook](Models/Baseline/XGBoost_open-world.ipynb)|
|  Neural Network |[Notebook](Models/Baseline/MLP_closed-world.ipynb)|[Notebook_binary](Models/Baseline/MLP_open-world_bin.ipynb)/[Notebook_multiclass](Models/Baseline/MLP_open-world_mul.ipynb)|
|  SVM |[Notebook](Models/Baseline/SVM_closed-world.ipynb)|[Notebook](Models/Baseline/SVM_open-world.ipynb)|

### Tuning
| Model | Closed World | Open World |
| :----: | :----: | :----: |
|  XGBoost |[Notebook](Models/Tuning/XGBoost_closed-world-tuning.ipynb)|[Notebook](Models/Tuning/XGBoost_open-world-tuning.ipynb)|
| Neural Network | [Notebook](Models/Tuning/MLP_closed-world-tuning.ipynb) | [Notebook_binary](Models/Tuning/MLP_open-world-tuning_bin.ipynb)/[Notebook_multiclass](Models/Tuning/MLP_open-world-tuning_mul.ipynb)|
| SVM | [Notebook](Models/Tuning/SVM_closed-world-tuning.ipynb) | [Notebook_binary](Models/Tuning/SVM_open-world-tuning_bin.ipynb)/[Notebook_multiclass](Models/Tuning/SVM_open-world-tuning_multi.ipynb)|

### Ensemble
| Model | Closed World | Open World |
| :----: | :----: | :----: |
|  XGBoost + CatBoost |[Notebook](Models/Ensemble/XGBoost+Catboost_closed-world.ipynb)|[Notebook](Models/Ensemble/XGBoost+Catboost_open-world.ipynb)|
|  MLP + XGBoost |[Notebook](Models/Ensemble/MLP+XGBoost_closed-world.ipynb)|[Notebook_binary](Models/Ensemble/MLP+XGBoost_open-world_bin.ipynb)/[Notebook_multiclass](Models/Ensemble/MLP+XGBoost_open-world_mul.ipynb)|
|  MLP + XGBoost + SVM |[Notebook](Models/Ensemble/MLP+XGBoost+SVM_closed-world.ipynb)|-|
|  MLP + LightGBM |-|[Notebook_binary](Models/Ensemble/MLP+LightGBM_open-world_bin.ipynb)|
|  MLP + LightGBM + XGBoost |-|[Notebook_multiclass](Models/Ensemble/MLP+XGBoost+LightGBM_open-world_mul.ipynb)|

## Extra Credit
A pipeline of data extraction -> feature engineering -> preprocessing -> model training -> model assessment.

### **extra_credit_main.py**:

- **Overview**

  This script loads .cell files from monitored (mon/) and unmonitored (unmon/) directories, extracts traffic features from each file, labels them, and appends all results into a single CSV file (all_features.csv).

  It is designed for the website fingerprinting feature engineering pipeline and works together with:

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

  ### Additional Experiments
  The Extra Credit folder also includes two exploratory experiments:
  - `_extra_credit_chunk_experiment.ipynb`: basic + chunk-based statistical features
  - `_extra_credit_iat_experiment.ipynb`: FFT-based IAT frequency features, spectral analysis

  - **Data Used**
    - These exploratory experiments were performed on "mon_25.zip"
    - Each exploratory notebook loads raw `.cell` files from "mon_25" and applies its own preprocessing

  - These experiments are independent exploratory analyses and are not part of the final submitted pipeline.  
  - They are included to document additional attempts at alternative feature engineering approaches.
