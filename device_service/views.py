from django.shortcuts import render

# Create your views here.
import boto3

from .models import get_data_table
from .serializers import DeviceSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# need to change the custom name of AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY so that it doesn't conflict with the default env name of AWS Lambda
# https://github.com/Miserlou/Zappa/issues/1043#issuecomment-322010594
db_table = get_data_table()


class CreateDeviceAPI(APIView):
    """
    Create a new instance of the Device table
    """

    def post(self, request):
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            device = db_table.get_item(Key={"id": data.get("id"), })

            if "Item" in device:
                return Response(status=status.HTTP_409_CONFLICT, data={'message': f'Item already exists with this id: {data.get("id")}.'})
            db_table.put_item(Item=data)
            return Response(status=status.HTTP_201_CREATED, data={'message': 'Item created successfully.'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class GetDeviceAPI(APIView):
    """
    Get all the information of an instance of the Device table with Device<pk>
    """
    def get(self, request, pk):
        try:
            device = db_table.get_item(Key={"id": f"/devices/id{pk}", })

            if "Item" in device:
                serializer = DeviceSerializer(device["Item"])
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'This item does not exist.'})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': 'Internal Server Error.'})


