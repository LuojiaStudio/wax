from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, authentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission
from .models import Activity, Group, Item, Vote
from user.models import Student, Staff
from news_management.views import get_ip
from datetime import date


class StaffPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            student = Student.objects.filter(user=request.user)
            staff = Staff.objects.filter(student=student)
        except:
            return False
        return True


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'name', 'starting_time', 'end_time', 'least_vote_num', 'most_vote_num')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields =  ('id', 'activity', 'id_in_activity', 'name')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'cover', 'content', 'id_in_group', 'id_in_activity', 'vote_num')


class ActivitySet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [StaffPermission]


class GroupSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [StaffPermission]


class ItemSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [StaffPermission]


class ListAndCreateVote(APIView):
    authentication_classes = (authentication.TokenAuthentication,)

    def check_vote_num(self, user, item):
        """
        check has voted today and whether exceed limit
        :param user:
        :param item:
        :return:
        """
        vote_set = Vote.objects.filter(time__day=date.today(), item__group=item.group)
        group = item.group

        group_most_vote_num = group.most_vote_num

        if len(vote_set) >= group_most_vote_num:
            return False
        for vote in vote_set:
            if vote.item == item:
                return False
        return True

    def post(self, request):
        ip = get_ip(request)
        user = request.user
        item = request.data['item']
        item_instance = Item.objects.get(pk=item)

        if self.check_vote_num(request.user, item_instance):
            vote = Vote(item=item_instance, ip=ip, user=Student.objects.get(user=user))
            vote.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


















































