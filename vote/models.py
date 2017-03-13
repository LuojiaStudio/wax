from django.db import models
from user.models import Student


class Activity(models.Model):
    name = models.CharField(max_length=100)
    starting_time = models.DateTimeField()
    end_time = models.DateTimeField()
    least_vote_num = models.IntegerField(default=0)
    most_vote_num = models.IntegerField()

    def __str__(self):
        return self.name


class Group(models.Model):
    activity = models.ForeignKey(
        'Activity',
        related_name='groups'
    )
    id_in_activity = models.IntegerField()
    name = models.CharField(max_length=50)

    most_vote_num = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Item(models.Model):
    group = models.ForeignKey(
        'Group',
        related_name='group'
    )
    name = models.CharField(max_length=50)
    cover = models.URLField(null=True, default=None)
    content = models.TextField()
    id_in_group = models.IntegerField()
    id_in_activity = models.IntegerField()

    def _get_vote(self):
        votes = Vote.objects.filter(item=self)
        return len(votes)

    vote_num = property(_get_vote)

    def __str__(self):
        return self.name


class Vote(models.Model):
    item = models.ForeignKey(
        'Item',
        related_name='votes'
    )
    time = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    user = models.ForeignKey(
        Student,
        related_name='votes'
    )