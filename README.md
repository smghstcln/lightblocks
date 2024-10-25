# Overview:
This project aims to analyze the behavior of the updatePriceFeeds method across four blockchain networks (Polygon, Scroll, Linea, zkLink). By collecting and processing on-chain data, we aim to provide insights into gas usage and costs for single-asset and multi-asset transactions, as well as the effects of Merkle tree depth on these parameters. The findings will guide recommendations for optimizing operator behavior and reducing costs.


# Folder Structure:<br/>
oracle_analysis/<br/>
data_collection_polygon.py<br/>
data_collection_scroll.py<br/>
data_collection_linea.py<br/>
data_collection_zklink.py<br/>
data_processing.ipynb<br/>
utils.py                   # Contains additional helper functions and the main function for collecting data for the four contract/chain<br/>
requirements.txt<br/>
README.md<br/>
data/<br/>
polygon_data.csv<br/>
scroll_data.csv<br/>
linea_data.csv<br/>
zklink_data.csv<br/>


# Prerequisites:
Python 3.7 or higher<br/>
pip package installer<br/>
Main libraries used include: web3, matplotlib, pandas.<br/>


# Setup Instructions:
## Clone the Repository
`git clone https://github.com/smghstcln/lightblocks.git`<br/>
`cd yourrepository`<br/>

## Create a Virtual Environment (Recommended)
`python -m venv venv`<br/>
-For Windows:<br/>
`venv\Scripts\activate`<br/>
-For macOS/Linux:<br/>
`source venv/bin/activate`<br/>

## Install Dependencies
-Install the required Python packages using requirements.txt:<br/>
`pip install -r requirements.txt`<br/>


# Data Collection Process (Pulling the raw data):
The data collection is performed through four Python scripts, each corresponding to a different blockchain network. <br/>
The `utils.py` file contains helper functions and the main function for collecting data across the four contract/chain pairs. This file abstracts away redundant operations and centralizes the core logic for data collection.<br/>

data_collection_polygon.py<br/>
data_collection_scroll.py<br/>
data_collection_linea.py<br/>
data_collection_zklink.py<br/>
These scripts connect to their respective blockchain networks via RPC endpoints and collect data on transactions involving the 'updatePriceFeeds' method.<br/>

To run the data collection scripts:<br/>
`python data_collection_polygon.py`<br/>
`python data_collection_scroll.py`<br/>
`python data_collection_linea.py`<br/>
`python data_collection_zklink.py`<br/>

Note: Each script can be run independently.<br/>


## Data Storage
The collected data will be saved in the data folder. The current files included are the raw data files for each chain use to create the dashboards.
Each script outputs a CSV file named after the chain:<br/>
polygon_data.csv<br/>
scroll_data.csv<br/>
linea_data.csv<br/>
zklink_data.csv<br/>
Ensure that the data folder exists in the root directory. The scripts will create it if it does not exist.<br/>


## Verifying and Changing the Time Range
Each data collection script defines the time range for data collection. By default, the time range is set from September 20, 2024, 12:00 PM to October 20, 2024, 12:00 PM in the Israel time zone.<br/>

To verify or modify the time range, locate the following section in each script:<br/>

tz = pytz.timezone('Israel')            # Time zone<br/>
start_date_str = '2024-09-20 12:00:00'  # Start date and time<br/>
end_date_str = '2024-10-20 12:00:00'    # End date and time<br/>

To change the time range:<br/>

Update start_date_str and end_date_str with your desired dates and times.<br/>
Ensure the date format is 'YYYY-MM-DD HH:MM:SS'.<br/>

## Ensuring Correct Data Storage Path
Each script specifies the data storage path. By default, it saves the output CSV files in the data folder with names specific to each chain.<br/>

data_folder = 'data'<br/>
csv_file_path = os.path.join(data_folder, '<chain>_data.csv')<br/>

To change the storage location or filename:<br/>

Modify data_folder and csv_file_path variables accordingly.

# Reproducing the Data
Running the data collection scripts as they are will reproduce the same results.<br/>

# Data Processing and Analysis
To analyze the collected data, the `data_processing.ipynb` notebook is provided. It walks through data loading, cleaning, and transformation steps, and produces visualizations and metrics necessary for understanding operator behavior. The notebook is divided into sections for:<br/>

Data Loading and Preprocessing<br/>
Visualization of Single and Multi-Asset Transaction Costs<br/>
Gas Usage Analysis with respect to Merkle Tree Depth<br/>
Interpretation of Results and Recommendations for Operators<br/>

To run the Analysis, launch Jupyter Notebook with `jupyter notebook data_processing.ipynb`, or run it sequencially from the file.

