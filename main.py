import os
import logging
import pandas as pd

from analysis.top_10_devices import get_top_10_devices
from analysis.avg_rssi_snr import get_avg_rssi_snr
from analysis.gateway_environment import get_gateway_environment
from analysis.duplicate_devices import get_duplicate_devices
from analysis.high_temperature import export_high_temperature_records

from database.mongodb_connection import get_mongodb_collection


os.makedirs("output", exist_ok=True)


logging.basicConfig(
    filename="output/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def import_csv_to_mongodb(collection):
    df = pd.read_csv("lorawan_uplink_devices.csv")

    logger.info(f"CSV loaded successfully with {len(df)} records")

    collection.delete_many({})

    records = df.to_dict(orient="records")

    if records:
        collection.insert_many(records)

    logger.info(f"{len(records)} records inserted into MongoDB")


def generate_output_report():
    with open("output/output_report.md", "w") as report:
        report.write("# LoRaWAN Pipeline Output Report\n\n")

        report.write("## Standard Output\n\n")
        report.write("```text\n")
        report.write("Pipeline executed successfully.\n")
        report.write("CSV data imported into MongoDB.\n")
        report.write("MongoDB collection used: uplinks\n")
        report.write("All analysis functions executed successfully.\n")
        report.write("Separate output files generated inside output folder.\n")
        report.write("```\n\n")

        report.write("## Generated Output Files\n\n")
        report.write("```text\n")
        report.write("output/top_10_devices.json\n")
        report.write("output/avg_rssi_snr.json\n")
        report.write("output/gateway_environment.json\n")
        report.write("output/duplicate_devices.json\n")
        report.write("output/high_temperature.json\n")
        report.write("output/pipeline.log\n")
        report.write("```\n\n")

        report.write("## Logs\n\n")
        report.write("```text\n")

        try:
            with open("output/pipeline.log", "r") as log_file:
                report.write(log_file.read())
        except FileNotFoundError:
            report.write("No logs found.\n")

        report.write("```\n")


def main():
    try:
        logger.info("========== LoRaWAN Pipeline Started ==========")

        collection = get_mongodb_collection(logger)

        import_csv_to_mongodb(collection)

        get_top_10_devices(collection, logger)
        get_avg_rssi_snr(collection, logger)
        get_gateway_environment(collection, logger)
        get_duplicate_devices(collection, logger)
        export_high_temperature_records(collection, logger)

        generate_output_report()

        logger.info("========== LoRaWAN Pipeline Completed ==========")

        print("Pipeline executed successfully.")
        print("Check the output folder for logs and reports.")

    except Exception as error:
        logger.error(f"Pipeline failed: {error}")
        print(f"Pipeline failed: {error}")
        raise


if __name__ == "__main__":
    main()