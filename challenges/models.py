from django.db import models
from django.utils import timezone
from authentication.models import User

from media.models import Photo
from users.models import Category


class Challenge(models.Model):
    name = models.CharField(max_length=24, null=False, unique=True)
    description = models.CharField(max_length=255, null=False)
    cover = models.OneToOneField(
        Photo, on_delete=models.CASCADE, null=False, blank=True, related_name='cover')
    category = models.ForeignKey(
        to=Category, on_delete=models.SET_NULL, null=True)
    value = models.IntegerField(default=0)
    time_created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name




class Pin(models.Model):
    challenge = models.ForeignKey(to=Challenge, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

class ChallengeImpression (models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # -discover -search
    activity = models.CharField(max_length=15)