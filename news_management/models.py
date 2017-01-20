from django.db import models
from user.models import Staff


class Tag(models.Model):
    name = models.CharField(max_length=10)
    is_main = models.BooleanField(default=False)  # whether be navigation
    is_source = models.BooleanField(default=False)  # show which department create the post

    def __str__(self):
        return self.name


class BasePost(models.Model):
    """
    Abstract Post model, including article, album and video
    """
    title = models.CharField(max_length=50)
    author = models.ForeignKey(
        Staff,
        related_name='created_posts',
        on_delete=models.SET_NULL,
        null=True
    )
    editor = models.ForeignKey(
        Staff,
        related_name='checked_posts',
        on_delete=models.SET_NULL,
        null=True
    )
    create_time = models.DateTimeField(auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(
        Tag,
        related_name='marked_posts',

    )

    view_number = models.IntegerField(default=0)
    like_number = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class BaseArticle(BasePost):
    content = models.TextField()
    subtitle = models.CharField(max_length=50, blank=True)

    class Meta:
        abstract = True


class UncheckedArticle(BaseArticle):
    """
    unchecked article
    """
    author = models.ForeignKey(
        Staff,
        related_name='created_unchecked_articles',
        on_delete=models.SET_NULL,
        null=True
    )
    editor = models.ForeignKey(
        Staff,
        related_name='checked_unchecked_articles',
        on_delete=models.SET_NULL,
        null=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='marked_unchecked_articles',

    )


class Article(BaseArticle):
    """
    checked article, display on the web site
    """
    author = models.ForeignKey(
        Staff,
        related_name='created_articles',
        on_delete=models.SET_NULL,
        null=True
    )
    editor = models.ForeignKey(
        Staff,
        related_name='checked_articles',
        on_delete=models.SET_NULL,
        null=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='marked_articles',

    )






