# Overview:
This project aims to analyze the behavior of the updatePriceFeeds method across four blockchain networks (Polygon, Scroll, Linea, zkLink). By collecting and processing on-chain data, we aim to provide insights into gas usage and costs for single-asset and multi-asset transactions, as well as the effects of Merkle tree depth on these parameters. The findings will guide recommendations for optimizing operator behavior and reducing costs.


# Folder Structure:
oracle_analysis/
├── data/
│   ├── polygon_data.csv
│   ├── scroll_data.csv
│   ├── linea_data.csv
│   └── zklink_data.csv
├── data_collection_polygon.py
├── data_collection_scroll.py
├── data_collection_linea.py
├── data_collection_zklink.py
├── data_processing.ipynb
├── utils.py                   # Contains additional helper functions and the main function for collecting data for the four contract/chain 
├── requirements.txt
└── README.md


# Prerequisites:
Python 3.7 or higher
pip package installer
Main libraries used include: web3, matplotlib, pandas.


# Setup Instructions:
## Clone the Repository
`git clone https://github.com/yourusername/yourrepository.git`
`cd yourrepository`

## Create a Virtual Environment (Recommended)
`python -m venv venv`
-For Windows:
`venv\Scripts\activate`
-For macOS/Linux:
`source venv/bin/activate`

## Install Dependencies
-Install the required Python packages using requirements.txt:
pip install -r requirements.txt


# Data Collection Process (Pulling the raw data):
The data collection is performed through four Python scripts, each corresponding to a different blockchain network. 
The `utils.py` file contains helper functions and the main function for collecting data across the four contract/chain pairs. This file abstracts away redundant operations and centralizes the core logic for data collection.

├── data_collection_polygon.py
├── data_collection_scroll.py
├── data_collection_linea.py
├── data_collection_zklink.py
These scripts connect to their respective blockchain networks via RPC endpoints and collect data on transactions involving the updatePriceFeeds method.

To run the data collection scripts:
`python data_collection_polygon.py`
`python data_collection_scroll.py`
`python data_collection_linea.py`
`python data_collection_zklink.py`

Note: Each script can be run independently.


## Data Storage
The collected data will be saved in the data folder. The current files included are the raw data files for each chain use to create the dashboards.
Each script outputs a CSV file named after the chain:
│   ├── polygon_data.csv
│   ├── scroll_data.csv
│   ├── linea_data.csv
│   ├── zklink_data.csv
Ensure that the data folder exists in the root directory. The scripts will create it if it does not exist.


## Verifying and Changing the Time Range
Each data collection script defines the time range for data collection. By default, the time range is set from September 20, 2024, 12:00 PM to October 20, 2024, 12:00 PM in the Israel time zone.

To verify or modify the time range, locate the following section in each script:

tz = pytz.timezone('Israel')            # Time zone
start_date_str = '2024-09-20 12:00:00'  # Start date and time
end_date_str = '2024-10-20 12:00:00'    # End date and time

To change the time range:

Update start_date_str and end_date_str with your desired dates and times.
Ensure the date format is 'YYYY-MM-DD HH:MM:SS'.

## Ensuring Correct Data Storage Path
Each script specifies the data storage path. By default, it saves the output CSV files in the data folder with names specific to each chain.

data_folder = 'data'
csv_file_path = os.path.join(data_folder, '<chain>_data.csv')

To change the storage location or filename:

Modify data_folder and csv_file_path variables accordingly.

# Reproducing the Data
Running the data collection scripts as they are will reproduce the same results.

# Data Processing and Analysis
To analyze the collected data, the `data_processing.ipynb` notebook is provided. It walks through data loading, cleaning, and transformation steps, and produces visualizations and metrics necessary for understanding operator behavior. The notebook is divided into sections for:

Data Loading and Preprocessing
Visualization of Single and Multi-Asset Transaction Costs
Gas Usage Analysis with respect to Merkle Tree Depth
Interpretation of Results and Recommendations for Operators

To Run the Analysis
-Launch Jupyter Notebook with `jupyter notebook data_processing.ipynb`, or run it sequencially from the file.

