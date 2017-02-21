from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import oss2
import uuid


@csrf_exempt
def upload_to_OSS(request):
    auth = oss2.Auth('LTAI73ZjdVlqmMUx', 'Pqwo3P15hEV2PR8EncWFBucq2M8GVv')
    bucket = oss2.Bucket(auth, 'oss-cn-beijing.aliyuncs.com', 'whusuoss')
    print(request.FILES)
    bucket.put_object('test/' + request.FILES['wangEditorH5File'].name, request.FILES['wangEditorH5File'])
    response = HttpResponse('http://whusuoss.oss-cn-beijing.aliyuncs.com/test/' + request.FILES['wangEditorH5File'].name)

    return response
