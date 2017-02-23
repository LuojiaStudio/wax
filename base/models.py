from django.db import models


class Application(models.Model):
    name = models.CharField(max_length=10)
    path = models.CharField(max_length=10)
    icon = models.URLField()

    def __str__(self):
        return self.name

