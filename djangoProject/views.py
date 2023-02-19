from django.shortcuts import render
from requests import request


def index(request):
    print(request.get_host())
    print(request.build_absolute_uri() + 'swagger-ui/')
    return render(request=request, template_name='index.html', context={
        'swagger_url': request.build_absolute_uri() + 'swagger-ui/',
        'openapi_url': request.build_absolute_uri() + 'openapi',
        'get_device_url': request.build_absolute_uri() + 'api/devices/id1/',
        'create_device_url': request.build_absolute_uri() + 'api/devices/',
    })