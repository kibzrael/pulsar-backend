from django.db import models

from authentication.models import User

class Category(models.Model):
    name = models.CharField(max_length=24, null= False, unique=True , verbose_name='Category')
    user =  models.CharField(max_length=24, null= False)
    # plural eg. band for musician
    users =  models.CharField(max_length=24, null= True)
    # use for subcategories eg. painting as a subcategory of art
    parent =  models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True,blank=True, related_name='subcategoryId')
    
    def __str__(self):
        return self.name
    
class Interest(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followedId')
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followerId')

    def save(self, *args, **kwargs):
        if self.user == self.follower:
            return
        else:
            super().save(*args, **kwargs)


class Block(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blockedId')
    blocking = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blockingId')

    def save(self, *args, **kwargs):
        if self.user == self.blocking:
            return
        else:
            super().save(*args, **kwargs)


class PostNotification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='trackedId')
    notify = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifyId')
    email = models.BooleanField(default=True)
    push = models.BooleanField(default=True)
    sms = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.user == self.notify:
            return
        else:
            super().save(*args, **kwargs)


class Device(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    token = models.CharField(null=False, max_length=255)