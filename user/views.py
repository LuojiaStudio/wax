from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Student
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User


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

    def get(self, request, pk):
        return JsonResponse({
            'username': request.user.username,
            'name': request.user.get_full_name(),
            'avatar': self.get_student_object(request.user).avatar_path,
        })

