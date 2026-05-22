# LoRaWAN Sensor Insights Pipeline

## Project Overview

This project implements a complete IoT data ingestion and analytics pipeline for LoRaWAN uplink sensor data using Python and MongoDB.

The system processes sensor telemetry data stored in a CSV file, imports it into MongoDB, performs multiple aggregation-based analytics queries, and exports critical temperature alerts into JSON format.

The project simulates a real-world IoT telemetry processing workflow commonly used in:

- Smart cities
- Industrial monitoring
- Agriculture systems
- Environmental sensing systems

---

# Objective

The objective of this project is to:

- Ingest LoRaWAN sensor uplink data from CSV into MongoDB
- Analyze device communication and signal quality
- Monitor environmental sensor readings
- Detect duplicate device records
- Export high-temperature alerts for monitoring systems
- Implement logging, error handling, and scheduling support
- Containerize the project using Docker

---

# Technologies Used

| Technology | Purpose                         |
| ---------- | ------------------------------- |
| Python     | Data processing and ETL         |
| Pandas     | CSV ingestion and preprocessing |
| MongoDB    | NoSQL database storage          |
| PyMongo    | MongoDB connectivity            |
| Docker     | Containerization                |
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
output/high_temperature.json
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
output/pipeline.log
```

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
lorawan_project/
│
├── output/
│   ├── high_temperature.json
│   ├── output_report.md
│   └── pipeline.log
│
├── Dockerfile
├── docker-compose.yml
├── main.py
├── README.md
├── requirements.txt
├── lorawan_uplink_devices.csv
└── .gitignore
```

---

# Docker Setup

## Build and Run the Project

```bash
docker compose up --build
```

---

## Run Again

```bash
docker compose up
```

---

## Stop Containers

```bash
docker compose down
```

---

## Remove Containers + Volumes

```bash
docker compose down -v
```

---

# Local Setup (Without Docker)

## 1. Create Virtual Environment

```bash
python3 -m venv venv
```

---

## 2. Activate Environment

### macOS/Linux

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Start MongoDB

```bash
brew services start mongodb/brew/mongodb-community
```

Verify MongoDB:

```bash
mongosh
```

---

## 5. Run the Pipeline

```bash
python main.py
```

---

# Output Files

All outputs are stored inside the `output/` folder.

| File                  | Description                    |
| --------------------- | ------------------------------ |
| high_temperature.json | High temperature alert records |
| pipeline.log          | Execution logs                 |
| output_report.md      | Markdown output report         |

---

# Output Section

## Standard Output

```text
Pipeline executed successfully.
CSV data imported into MongoDB.
MongoDB collection used: uplinks
All analysis queries executed successfully.
High temperature records exported successfully.
```

---

## Logs

```text
2026-05-22 10:10:15 - INFO - LoRaWAN Pipeline Started
2026-05-22 10:10:16 - INFO - Connected to MongoDB successfully
2026-05-22 10:10:17 - INFO - CSV loaded successfully
2026-05-22 10:10:18 - INFO - Records inserted into MongoDB
2026-05-22 10:10:20 - INFO - Aggregation queries executed
2026-05-22 10:10:21 - INFO - High temperature records exported
2026-05-22 10:10:22 - INFO - Pipeline completed successfully
```

---

## High Temperature JSON Export

```json
[
  {
    "device_id": "DEV_1001",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "temperature": 37.5
  }
]
```

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

# Future Improvements

Potential enhancements:

- Real-time MQTT ingestion
- Kafka streaming pipeline
- Dashboard visualization using Grafana
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
- Docker containerization
- Automated scheduling

The system is scalable and can be extended for real-world IoT monitoring applications.
