import json
import os


def get_avg_rssi_snr(collection, logger):
    result = list(collection.aggregate([
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
    ]))

    os.makedirs("output", exist_ok=True)

    with open("output/avg_rssi_snr.json", "w") as file:
        json.dump(result, file, indent=4)

    logger.info("Average RSSI and SNR per device:")

    for item in result:
        logger.info(item)

    return result