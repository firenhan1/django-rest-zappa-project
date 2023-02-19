import os

import boto3
import botocore
from dotenv import load_dotenv

load_dotenv()

def create_devices_table():
    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.create_table(
        TableName="devices",
        KeySchema=[
            {
                "AttributeName": "id",
                "KeyType": "HASH"
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "id",
                "AttributeType": "S"
            },
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 2
        },
    )
    return table


if __name__ == "__main__":
    try:
        devices_table = create_devices_table()
        devices_table.wait_until_exists()

        # my_table.meta.client.get_waiter("table_exists").wait(TableName="Device_DB")
        print("Table was created successfully. Table size: ", devices_table.item_count)

    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "ResourceInUseException":
            print("Error: This table already exists. please change the table name.")
        else:
            raise error
