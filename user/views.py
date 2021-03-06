from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Student, Staff
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User
import re
import requests
from django.views.decorators.csrf import csrf_exempt


# login
@api_view(['POST'])
def login(request):
    login_token = request.data['login_token']
    password = request.data['password']

    user_login_by_username = authenticate(username=login_token, password=password)
    user_login_by_student_number = authenticate(student_number=login_token, password=password)

    if user_login_by_username:
        user = user_login_by_username
    else:
        user = user_login_by_student_number

    if user is not None:
        data = {
            'token': create_token(user)
        }

        return Response(data=data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def create_token(user):
    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        token = Token.objects.create(user=user)
    return token.key


class StudentNumberAuthenticateBackend(object):
    """
    login by student number
    """
    def authenticate(self, student_number=None, password=None):
        try:
            user = Student.objects.get(student_number=student_number).user
        except Student.DoesNotExist:
            return None
        password_valid = check_password(password, user.password)
        if password_valid:
            return user
        else:
            return None


# change password
@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def change_password(request):
    user = request.user
    user.password = make_password(request.data['new_pwd'])
    user.save()
    return Response(status=status.HTTP_200_OK)


class Profile(APIView):

    def get_student_object(self, user):
        try:
            return Student.objects.get(user=user)
        except Student.DoesNotExist:
            raise Http404

    def get_staff_object(self, student):
        try:
            return Staff.objects.get(student=student)
        except Staff.DoesNotExist:
            raise Http404

    def get(self, request):
        student = self.get_student_object(request.user)
        staff = self.get_staff_object(student)
        return JsonResponse({
            'username': request.user.username,
            'name': request.user.get_full_name(),
            'student_number': student.student_number,
            'avatar': student.avatar_path,
            'email': request.user.email,
            'tel': student.tel,
            'wechat': student.wechat,
            'qq': student.qq,
            'birthday': student.birthday,
            'job_title': staff.job_title.__str__(),
            'school': student.school.__str__()
        })

    def put(self, request):
        student = self.get_student_object(request.user)
        request.user.email = request.data['email']
        student.wechat = request.data['wechat']
        student.qq = request.data['qq']
        student.tel = request.data['tel']
        request.user.save()
        student.save()

        return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def has_perm(request):
    if (request.user.has_perm(request.GET['perm'])):
        return JsonResponse({'result': True})
    else:
        return JsonResponse({'result': False})


@api_view(['POST'])
def check_whu_student(request):
    """
    check whether request user is whu student
    :param request:
    :return:
    """
    sid = request.data['sid']
    password = request.data['password']

    proxies = {"http": "http://58.243.0.162:9999"}

    r = requests.get('http://cas.whu.edu.cn/authserver/login', proxies=proxies)
    lt = re.findall('name="lt" value="(.*)"', r.text)
    dllt = re.findall('name="dllt" value="(.*)"', r.text)
    execution = re.findall('name="execution" value="(.*)"', r.text)
    _eventId = re.findall('name="_eventId" value="(.*)"', r.text)
    rmShown = re.findall('name="rmShown" value="(.*)"', r.text)

    route = r.cookies['route']
    jsession_id = r.cookies['JSESSIONID_ids1']

    headers = {
        'host': 'cas.whu.edu.cn',
        'Origin': 'http://cas.whu.edu.cn',
        'Referer': 'http://cas.whu.edu.cn/authserver/login',
        'Content-Type': 'application/x-www-form-urlencoded'
    }



    try:
        payload = {
            'username': sid,
            'password': password,
            'lt': lt[0],
            'dllt': dllt[0],
            'execution': execution[0],
            '_eventId': _eventId[0],
            'rmShown': rmShown[0]
        }
        cookies = {
            'route': route,
            'JSESSIONID_ids1': jsession_id,
        }
        r = requests.post('http://cas.whu.edu.cn/authserver/login', data=payload, cookies=cookies, headers=headers, proxies=proxies)

        if re.search('安全退出', r.text):
            return JsonResponse({'result': True, 'msg': '验证成功'})
        else:
            return JsonResponse({'result': False, 'msg': '学号或密码错误'})
    except:
        return JsonResponse({'result': False, 'msg': '但这是服务器的锅'})


@api_view(['POST'])
def login_or_register(request):
    """
    login user, if user do not exist, register it
    :param request:
    :return:
    """
    sid = request.data['sid']
    password = request.data['password']

    try:
        student = Student.objects.get(student_number=sid)
    except Student.DoesNotExist:
        user = User.objects.create_user(
            sid,
            sid + '@whu.edu.cn',
            password
        )
        student = Student(
            user=user,
            student_number=sid
        )
        student.save()
    user = student.user

    data = {
        'token': create_token(user)
    }

    return Response(data=data, status=status.HTTP_202_ACCEPTED)


def tt(request):
    r = requests.get('http://cas.whu.edu.cn/authserver/login')
    return Response(data=r.text)



































