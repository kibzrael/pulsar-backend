from django.db import models
from django.utils import timezone

from authentication.models import User, Category
from media.models import Photo


class Interest(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self) -> str:
        return self.user.username + ": " + str(self.category.name)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followedId")
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followerId"
    )

    def save(self, *args, **kwargs):
        if self.user == self.follower:
            return
        else:
            super().save(*args, **kwargs)


class Block(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blockedId")
    blocking = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blockingId"
    )

    def save(self, *args, **kwargs):
        if self.user == self.blocking:
            return
        else:
            super().save(*args, **kwargs)


class PostNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trackedId")
    notify = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifyId")
    email = models.BooleanField(default=True)
    push = models.BooleanField(default=True)
    sms = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.user == self.notify:
            return
        else:
            super().save(*args, **kwargs)


class Activity(models.Model):
    receipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receipientId"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userId")
    media = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=255)
    link = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=24)
    time = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(null=False, max_length=255)
