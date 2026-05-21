# LoRaWAN Sensor Insights Pipeline

## Project Overview

This project implements a complete IoT data ingestion and analytics pipeline for LoRaWAN uplink sensor data using Python and MongoDB.

The system processes sensor telemetry data stored in a CSV file, imports it into MongoDB, performs multiple aggregation-based analytics queries, and exports critical temperature alerts into JSON format.

The project simulates a real-world IoT telemetry processing workflow commonly used in smart cities, industrial monitoring, agriculture, and environmental sensing systems.

---

# Objective

The objective of this project is to:

- Ingest LoRaWAN sensor uplink data from CSV into MongoDB
- Analyze device communication and signal quality
- Monitor environmental sensor readings
- Detect duplicate device records
- Export high-temperature alerts for monitoring systems
- Implement logging, error handling, and scheduling support

---

# Technologies Used

| Technology | Purpose                         |
| ---------- | ------------------------------- |
| Python     | Data processing and ETL         |
| Pandas     | CSV ingestion and preprocessing |
| MongoDB    | NoSQL database storage          |
| PyMongo    | MongoDB connectivity            |
| JSON       | Exporting alert data            |
| Logging    | Monitoring and debugging        |
| Cron       | Daily task scheduling           |

---

# Dataset

Dataset used:

```text
lorawan_uplink_devices.csv
```

The dataset contains LoRaWAN uplink telemetry information collected from 5,000+ IoT devices.

---

# Dataset Fields

| Field               | Description                        |
| ------------------- | ---------------------------------- |
| device_id           | Unique sensor/device identifier    |
| dev_eui             | Device EUI identifier              |
| dev_addr            | Device network address             |
| timestamp           | Uplink timestamp                   |
| temperature         | Temperature reading                |
| humidity            | Humidity reading                   |
| barometric_pressure | Atmospheric pressure               |
| analog_in_1         | Analog sensor input 1              |
| analog_in_2         | Analog sensor input 2              |
| rssi                | Received Signal Strength Indicator |
| snr                 | Signal-to-Noise Ratio              |
| latitude            | GPS latitude                       |
| longitude           | GPS longitude                      |
| gateway_id          | Receiving gateway identifier       |
| frequency           | Transmission frequency             |
| spreading_factor    | LoRa spreading factor              |
| bandwidth           | Communication bandwidth            |

---

# Features Implemented

## 1. CSV Ingestion into MongoDB

- Read CSV dataset using Pandas
- Convert records into JSON-like documents
- Insert records into MongoDB collection `uplinks`

---

## 2. Top 10 Devices by Uplink Count

Aggregation pipeline used to:

- Group records by `device_id`
- Count total uplinks
- Sort in descending order
- Display top 10 active devices

---

## 3. Average RSSI and SNR Analysis

Computed:

- Average RSSI per device
- Average SNR per device

Purpose:

- Detect weak network connections
- Identify devices with poor signal quality

Devices are sorted by lowest RSSI.

---

## 4. Gateway-wise Environmental Analysis

Calculated:

- Average temperature per `gateway_id`
- Average humidity per `gateway_id`

Purpose:

- Gateway-level environmental monitoring
- Regional sensor aggregation

---

## 5. Duplicate Device Detection

Aggregation query used to:

- Identify device IDs with more than one record
- Detect repeated telemetry entries

---

## 6. High Temperature JSON Export

Filtered all records where:

```text
temperature > 35°C
```

Exported fields:

- device_id
- latitude
- longitude
- temperature

Generated file:

```text
high_temperature.json
```

---

## 7. Logging and Error Handling

Implemented:

- Logging using Python `logging` module
- Exception handling using `try-except`
- CSV validation checks
- MongoDB connection error handling

Generated log file:

```text
pipeline.log
```

---

## 8. MongoDB Indexing

Indexes created on:

- `device_id`
- `gateway_id`
- `temperature`

Purpose:

- Improve query performance
- Optimize aggregation operations

---

# MongoDB Configuration

## Database

```text
lorawan_db
```

## Collection

```text
uplinks
```

---

# Project Structure

```text
Task1_LoRaWAN_Pipeline/
│
├── main.py
├── README.md
├── requirements.txt
├── high_temperature.json
├── pipeline.log
├── lorawan_uplink_devices.csv
└── screenshots/
```

---

# Setup Instructions

## 1. Clone or Download Project

Place all project files into a local folder.

---

## 2. Create Virtual Environment

```bash
python3 -m venv venv
```

---

## 3. Activate Virtual Environment

### macOS/Linux

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install pandas pymongo
```

OR

```bash
pip install -r requirements.txt
```

---

## 5. Start MongoDB

```bash
brew services start mongodb/brew/mongodb-community
```

Verify MongoDB:

```bash
mongosh
```

---

## 6. Run the Pipeline

```bash
python main.py
```

---

# Aggregation Queries Used

## Top Devices Query

Used:

- `$group`
- `$sort`
- `$limit`

---

## RSSI/SNR Analysis

Used:

- `$avg`
- `$group`
- `$sort`

---

## Duplicate Detection

Used:

- `$match`
- `$group`

---

# IoT Concepts Used

## LoRaWAN

LoRaWAN is a low-power wide-area networking protocol designed for IoT communication.

---

## Uplink

An uplink is a message sent from an IoT device to a gateway.

Flow:

```text
Device → Gateway → Network Server → Database
```

---

## RSSI

RSSI (Received Signal Strength Indicator) measures radio signal strength.

Typical range:

```text
-30 dBm → Excellent
-120 dBm → Very Weak
```

---

## SNR

SNR (Signal-to-Noise Ratio) measures communication quality between signal and background noise.

Higher SNR indicates better signal quality.

---

# Output Files

| File                  | Description                    |
| --------------------- | ------------------------------ |
| high_temperature.json | High temperature alert records |
| pipeline.log          | Execution logs                 |
| main.py               | Main ETL pipeline script       |

---

# Scheduling (Bonus Task)

Daily automation can be configured using cron.

Open cron editor:

```bash
crontab -e
```

Example cron job:

```bash
0 1 * * * /usr/bin/python3 /Users/username/lorawan_project/main.py
```

This executes the pipeline daily at 1:00 AM.

---

# Future Improvements

Potential enhancements:

- Real-time MQTT ingestion
- Kafka streaming pipeline
- Dashboard visualization using Grafana
- Docker containerization
- Apache Airflow orchestration
- Machine learning anomaly detection
- REST API integration

---

# Conclusion

This project demonstrates a complete IoT telemetry ingestion and analytics workflow using Python and MongoDB.

The implementation covers:

- ETL pipeline creation
- NoSQL data storage
- Aggregation analytics
- Signal quality analysis
- Environmental monitoring
- Logging and error handling
- Automated scheduling

The system is scalable and can be extended for real-world IoT monitoring applications.
