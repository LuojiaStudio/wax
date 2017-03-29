from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, authentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission
from .models import Activity, Group, Item, Vote
from user.models import Student, Staff
from news_management.views import get_ip
import datetime
from django.utils import timezone
import django_filters.rest_framework


class StaffPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        try:
            student = Student.objects.filter(user=request.user)
            staff = Staff.objects.filter(student=student)
        except:
            return False
        return True


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'uuid', 'name', 'content', 'starting_time', 'end_time', 'least_vote_num', 'most_vote_num')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields =  ('id', 'activity', 'id_in_activity', 'name')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'group', 'name', 'cover', 'content', 'id_in_group', 'id_in_activity', 'vote_num')


class ActivitySet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [StaffPermission]
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter
    )
    filter_fields = ('uuid',)


class GroupSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [StaffPermission]
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter
    )
    filter_fields = ('activity',)

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class ItemSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [StaffPermission]
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter
    )
    pagination_class = LargeResultsSetPagination
    filter_fields = ('group',)


class ListAndCreateVote(APIView):
    authentication_classes = (authentication.TokenAuthentication,)

    def check_vote_num(self, user, item):
        """
        check has voted today and whether exceed limit
        :param user:
        :param item:
        :return:
        """
        vote_set = Vote.objects.filter(date=datetime.date.today(), item__group=item.group, user=user)
        group = item.group

        group_most_vote_num = group.most_vote_num

        if len(vote_set) >= group_most_vote_num:
            return {'result': False, 'msg': '投票失败，超过本组投票数量上限'}
        for vote in vote_set:
            if vote.item == item:
                return {'result': False, 'msg': '投票失败，今日已投过这个选项啦'}
        return {'result': True, 'msg': ''}

    def check_time(self, item):
        """
        check time
        :return:
        """
        result = timezone.now() < item.group.activity.end_time and timezone.now() > item.group.activity.starting_time

        if result:
            msg = ''
        else:
            msg = '投票失败，活动时间不符'
        return {'result': result, 'msg': msg}

    def post(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        user = request.user
        item = request.data['item']
        item_instance = Item.objects.get(pk=item)
        student = Student.objects.get(user=user)

        time_check = self.check_time(item_instance)

        msg = time_check['msg']

        if time_check['result']:

            check = self.check_vote_num(student, item_instance)

            msg = check['msg']

            if check['result']:
                vote = Vote(
                    item=item_instance,
                    ip=ip,
                    user=Student.objects.get(user=user),
                )
                vote.save()
                return Response(status=status.HTTP_201_CREATED, data={'msg': '投票成功'})
            else:
                return Response(status=status.HTTP_200_OK, data={'msg': msg})
        else:
            return Response(status=status.HTTP_200_OK, data={'msg': msg})





















































