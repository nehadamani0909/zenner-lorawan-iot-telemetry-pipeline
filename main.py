import pandas as pd
import json
import logging
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from datetime import datetime

# =========================================================
# LOGGING CONFIGURATION
# =========================================================
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("========== LoRaWAN Pipeline Started ==========")

# =========================================================
# MONGODB CONNECTION
# =========================================================
try:
    client = MongoClient("mongodb://localhost:27017/")

    db = client["lorawan_db"]

    collection = db["uplinks"]

    logging.info("Connected to MongoDB successfully")

except Exception as e:
    logging.error(f"MongoDB connection failed: {e}")
    raise

# =========================================================
# CSV INGESTION
# =========================================================
CSV_FILE = "lorawan_uplink_devices.csv"

try:
    df = pd.read_csv(CSV_FILE)

    logging.info(f"CSV loaded successfully with {len(df)} records")

except Exception as e:
    logging.error(f"Failed to read CSV file: {e}")
    raise

# =========================================================
# DATA VALIDATION
# =========================================================
required_columns = [
    "device_id",
    "timestamp",
    "temperature",
    "humidity",
    "rssi",
    "snr",
    "latitude",
    "longitude",
    "gateway_id"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    logging.error(f"Missing columns: {missing_columns}")
    raise Exception(f"Missing columns: {missing_columns}")

# Remove rows with missing device_id
df = df.dropna(subset=["device_id"])

logging.info("Data validation completed")

# =========================================================
# CREATE INDEXES
# =========================================================
try:
    collection.create_index("device_id")
    collection.create_index("gateway_id")
    collection.create_index("temperature")

    logging.info("Indexes created successfully")

except Exception as e:
    logging.warning(f"Index creation warning: {e}")

# =========================================================
# INSERT DATA INTO MONGODB
# =========================================================
try:
    records = df.to_dict(orient="records")

    if records:
        collection.insert_many(records)

        logging.info(f"{len(records)} records inserted into MongoDB")

except BulkWriteError as bwe:
    logging.error(f"Bulk write error: {bwe.details}")

except Exception as e:
    logging.error(f"Data insertion failed: {e}")

# =========================================================
# QUERY 1:
# TOP 10 DEVICES WITH HIGHEST UPLINKS
# =========================================================
print("\n=================================================")
print("TOP 10 DEVICES WITH HIGHEST UPLINKS")
print("=================================================\n")

pipeline_top_devices = [
    {
        "$group": {
            "_id": "$device_id",
            "uplink_count": {"$sum": 1}
        }
    },
    {
        "$sort": {"uplink_count": -1}
    },
    {
        "$limit": 10
    }
]

top_devices = list(collection.aggregate(pipeline_top_devices))

for device in top_devices:
    print(device)

logging.info("Top 10 devices query executed successfully")

# =========================================================
# QUERY 2:
# AVERAGE RSSI AND SNR PER DEVICE
# =========================================================
print("\n=================================================")
print("AVERAGE RSSI AND SNR PER DEVICE")
print("=================================================\n")

pipeline_signal = [
    {
        "$group": {
            "_id": "$device_id",
            "avg_rssi": {"$avg": "$rssi"},
            "avg_snr": {"$avg": "$snr"}
        }
    },
    {
        "$sort": {"avg_rssi": 1}
    }
]

signal_stats = list(collection.aggregate(pipeline_signal))

for stat in signal_stats[:10]:
    print(stat)

logging.info("RSSI and SNR analysis completed")

# =========================================================
# QUERY 3:
# AVERAGE TEMPERATURE AND HUMIDITY PER GATEWAY
# =========================================================
print("\n=================================================")
print("AVERAGE TEMPERATURE AND HUMIDITY PER GATEWAY")
print("=================================================\n")

pipeline_gateway = [
    {
        "$group": {
            "_id": "$gateway_id",
            "avg_temperature": {"$avg": "$temperature"},
            "avg_humidity": {"$avg": "$humidity"}
        }
    }
]

gateway_stats = list(collection.aggregate(pipeline_gateway))

for gateway in gateway_stats:
    print(gateway)

logging.info("Gateway environmental analysis completed")

# =========================================================
# QUERY 4:
# FIND DUPLICATE DEVICE IDs
# =========================================================
print("\n=================================================")
print("DUPLICATE DEVICE IDs")
print("=================================================\n")

pipeline_duplicates = [
    {
        "$group": {
            "_id": "$device_id",
            "count": {"$sum": 1}
        }
    },
    {
        "$match": {
            "count": {"$gt": 1}
        }
    }
]

duplicates = list(collection.aggregate(pipeline_duplicates))

for duplicate in duplicates:
    print(duplicate)

logging.info("Duplicate device detection completed")

# =========================================================
# QUERY 5:
# EXPORT HIGH TEMPERATURE RECORDS TO JSON
# =========================================================
print("\n=================================================")
print("EXPORTING HIGH TEMPERATURE RECORDS")
print("=================================================\n")

high_temp_records = collection.find(
    {
        "temperature": {"$gt": 35}
    },
    {
        "_id": 0,
        "device_id": 1,
        "latitude": 1,
        "longitude": 1,
        "temperature": 1
    }
)

high_temp_data = list(high_temp_records)

with open("high_temperature.json", "w") as json_file:
    json.dump(high_temp_data, json_file, indent=4)

print(f"Exported {len(high_temp_data)} records to high_temperature.json")

logging.info(
    f"Exported {len(high_temp_data)} high temperature records"
)

# =========================================================
# CLOSE MONGODB CONNECTION
# =========================================================
client.close()

logging.info("MongoDB connection closed")
logging.info("========== Pipeline Finished Successfully ==========")

print("\nPipeline execution completed successfully!\n")