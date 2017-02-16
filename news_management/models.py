from django.db import models
from user.models import Staff
from django.utils.timesince import timesince
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True)
    is_main = models.BooleanField(default=False)  # whether be navigation
    is_source = models.BooleanField(default=False)  # show which department create the post

    def __str__(self):
        return self.name


class BasePost(models.Model):
    """
    Abstract Post model, including article, album and video
    """
    title = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    issuing_time = models.DateTimeField(null=True, blank=True)
    last_modify_time = models.DateTimeField(auto_now=True)
    is_checked = models.BooleanField()
    view_number = models.IntegerField(default=0)
    like_number = models.IntegerField(default=0)
    cover = models.CharField(max_length=100)

    def _get_humanize_time(self):
        return timesince(self.create_time, timezone.now())

    humaniza_create_time = property(_get_humanize_time)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Article(BasePost):
    """
    checked article, display on the web site
    """
    content = models.TextField()
    author = models.CharField(max_length=20, null=True, blank=True)
    photographer = models.CharField(max_length=20, null=True, blank=True)
    create_staff = models.ForeignKey(
        Staff,
        related_name='created_articles',
        null=True,
        blank=True
    )
    checked_staff = models.ForeignKey(
        Staff,
        related_name='checked_articles',
        null=True,
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='marked_articles',
    )






