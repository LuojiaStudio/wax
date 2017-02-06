from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import Student
from django.contrib.auth import authenticate
from rest_framework.test import APIRequestFactory
from .views import create_token, login, change_password
from rest_framework.test import force_authenticate


class LoginTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            'test_user',
            'test@test.com',
            'test123test'
        )
        Student.objects.create(
            user=user,
            student_number='2014301500228'
        )
        self.factory = APIRequestFactory()
        self.user = user

    def test_login_by_username_func(self):
        user = User.objects.get(username='test_user')
        return_user = authenticate(username='test_user', password='test123test')
        self.assertEqual(return_user, user)

    def test_login_by_student_number_func(self):
        user = Student.objects.get(student_number='2014301500228').user
        return_user = authenticate(student_number='2014301500228', password='test123test')
        self.assertEqual(return_user, user)

    def test_create_token_func(self):
        user = User.objects.get(username='test_user')
        token = create_token(user=user)
        self.assertEqual(token is not None, True)

    def test_login_api(self):
        path = '/user/login/'
        request_username = self.factory.post(path, {
            'login_token': 'test_user',
            'password': 'test123test'
        }, format='json')

        request_student_number = self.factory.post(path, {
            'login_token': 'test_user',
            'password': 'test123test'
        }, format='json')

        response_username = login(request_username)
        response_student_number = login(request_student_number)

        self.assertEqual(response_username.status_code, 202)
        self.assertEqual(response_student_number.status_code, 202)

    def test_change_pwd(self):
        path = '/user/change_pwd/'
        content = {
            'new_pwd': 'test456test'
        }
        request = self.factory.post(path, content, format='json')
        force_authenticate(request, user=self.user)
        response = change_password(request)

        self.assertEqual(response.status_code, 200)



