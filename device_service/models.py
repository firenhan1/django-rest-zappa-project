import os

import boto3
from django.db import models

# Create your models here.
from dynamorm import DynaModel
from marshmallow import fields
from dotenv import load_dotenv

load_dotenv()


class Devices(DynaModel):
    class Table:
        name = "devices"
        hash_key = "id"
        read = 25
        write = 5

    class Schema:
        id = fields.String()
        deviceModel = fields.String()
        name = fields.String()
        note = fields.String()
        serial = fields.String()


def get_data_table():
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=os.getenv("MY_AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("MY_AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("MY_AWS_DEFAULT_REGION"),
    )
    table = dynamodb.Table("devices")
    return table
