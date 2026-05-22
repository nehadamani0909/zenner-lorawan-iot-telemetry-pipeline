import json


def export_high_temperature_records(collection, logger):
    result = list(collection.find(
        {"temperature": {"$gt": 35}},
        {
            "_id": 0,
            "device_id": 1,
            "latitude": 1,
            "longitude": 1,
            "temperature": 1
        }
    ))

    with open("output/high_temperature.json", "w") as file:
        json.dump(result, file, indent=4)

    logger.info(f"{len(result)} high temperature records exported")

    return result