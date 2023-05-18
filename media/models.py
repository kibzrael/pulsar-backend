from django.db import models


class Photo(models.Model):
    thumbnail = models.URLField()
    thumbnail_blob = models.CharField(max_length=255,null=True)
    medium = models.URLField()
    medium_blob = models.CharField(max_length=255,null=True)
    high = models.URLField()
    high_blob = models.CharField(max_length=255,null=True)





class Video(models.Model):
    low = models.URLField()
    low_blob = models.CharField(max_length=255,null=True)
    medium = models.URLField()
    medium_blob = models.CharField(max_length=255,null=True)
    high = models.URLField()
    high_blob = models.CharField(max_length=255,null=True)

