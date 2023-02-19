from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APISimpleTestCase

# Create your tests here.
client = APIClient()


class TestGetDevice(APISimpleTestCase):
    # def test_get_device(self):
    #     response = self.client.get("http://127.0.0.1:8000/api/devices/id1")
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_get_device_return_error(self):
    #     response = self.client.get("http://127.0.0.1:8000/api/devices/id100")
    #     self.assertEqual(response.status_code, 404)
    def test1_get_device_valid(self):
        response = client.get("http://127.0.0.1:8000/api/devices/id1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test2_get_device_invalid(self):
        response = client.get("http://127.0.0.1:8000/api/devices/id567/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestCreateDevice(APISimpleTestCase):
    def setUp(self):
        self.payload1_valid = {
            "id": "/devices/id5",
            "deviceModel": "/models/id5",
            "name": "Sensor5",
            "note": "Testing a sensor5.",
            "serial": "A020000105",
        }

        self.payload2_invalid = {
            "id": "", # id required field
            "deviceModel": "/models/id9",
            "name": "", # name required field
            "note": "Testing a sensor2.",
            # serial required field
        }

        self.payload3_invalid = {
            "id": "6", # id format is invalid : must be in this format => /devices/id<pk>
            "deviceModel": "/models/id6",
            "name": "Sensor6",
            "note": "Testing a sensor 6.",
            "serial": "A020000106",
        }

    def test1_create_device_return_success(self):
        response = client.post("http://127.0.0.1:8000/api/devices", self.payload1_valid)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test2_create_device_missing_field(self):
        response = client.post("http://127.0.0.1:8000/api/devices", self.payload2_invalid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test3_create_device_invalid_id(self):
        response = client.post("http://127.0.0.1:8000/api/devices", self.payload3_invalid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test4_create_device_duplicate_item(self):
        response = client.post("http://127.0.0.1:8000/api/devices", self.payload1_valid)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)  # item already exist
