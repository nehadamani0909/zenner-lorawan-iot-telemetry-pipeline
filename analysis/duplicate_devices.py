import json
import os


def get_duplicate_devices(collection, logger):
    result = list(collection.aggregate([
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
    ]))

    os.makedirs("output", exist_ok=True)

    with open("output/duplicate_devices.json", "w") as file:
        json.dump(result, file, indent=4)

    logger.info("Duplicate device IDs:")

    for item in result:
        logger.info(item)

    return result