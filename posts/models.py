from django.db import models
from django.utils import timezone

from authentication.models import User
from challenges.models import Challenge
from media.models import Photo, Video

# _default_thumb = "https://firebasestorage.googleapis.com/v0/b/pulsar-2217f.appspot.com/o/posts%2Fthumbnails%2F1-2022-01-06%2010%3A04%3A26.560246-high.jpg?alt=media&token=5675ad60-9f57-42da-ae06-d3cafe2ceab9"


class Post(models.Model):
    source = models.OneToOneField(Video, on_delete=models.CASCADE, null=False)
    thumbnail = models.OneToOneField(Photo, on_delete=models.CASCADE, null=False)
    caption = models.CharField(max_length=80, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")

    challenge = models.ForeignKey(
        Challenge, on_delete=models.SET_NULL, null=True, blank=True
    )

    allow_comments = models.BooleanField(default=True)
    time = models.DateTimeField(default=timezone.now)

    # to be removed
    filter_name = models.CharField(max_length=24, null=True)

    ratio = models.FloatField(null=False, default=1.0)

    def __str__(self) -> str:
        return self.user.username + " : " + str(self.id)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_liker")

    def __str__(self) -> str:
        return self.user.username + ": " + str(self.post.id)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comment"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_commenter"
    )
    comment = models.CharField(max_length=255, null=False)
    time = models.DateTimeField(default=timezone.now)
    reply_to = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, related_name="comment_reply"
    )

    def __str__(self) -> str:
        return self.user.username + ": " + str(self.comment)


class CommentLike(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="comment_like"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_liker"
    )


class Repost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_repost")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_reposter"
    )


class Tag(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, null=True)
    tag = models.CharField(max_length=15, null=False)
    explicit = models.BooleanField(default=False)


class Mention(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=15, null=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)


class PostImpression(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # -view -profile -discover -challenge
    activity = models.CharField(max_length=15)


# when the video is watched past 10s
class View(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
