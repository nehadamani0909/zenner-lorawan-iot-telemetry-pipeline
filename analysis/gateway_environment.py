import json
import os


def get_gateway_environment(collection, logger):
    result = list(collection.aggregate([
        {
            "$group": {
                "_id": "$gateway_id",
                "avg_temperature": {"$avg": "$temperature"},
                "avg_humidity": {"$avg": "$humidity"}
            }
        }
    ]))

    os.makedirs("output", exist_ok=True)

    with open("output/gateway_environment.json", "w") as file:
        json.dump(result, file, indent=4)

    logger.info("Average temperature and humidity per gateway:")

    for item in result:
        logger.info(item)

    return result