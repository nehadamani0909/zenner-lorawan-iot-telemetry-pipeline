import json
import os


def get_top_10_devices(collection, logger):
    result = list(collection.aggregate([
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
    ]))

    os.makedirs("output", exist_ok=True)

    with open("output/top_10_devices.json", "w") as file:
        json.dump(result, file, indent=4)

    logger.info("Top 10 devices with highest uplinks:")

    for item in result:
        logger.info(item)

    return result