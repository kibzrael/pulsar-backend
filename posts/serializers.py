from rest_framework import serializers

from posts.models import Comment, CommentLike, Like, Mention, Post, Repost, Tag
from challenges.serializers import MinimialChallengeSerializer
from media.serializers import PhotoSerializer, VideoSerializer
from users.serializers import MinimalUserSerializer

from django.db.models import Count

points_calculation = (
    Count("post_like", distinct=True) * 5
    + Count("post_comment", distinct=True) * 10
    + Count("post_repost", distinct=True) * 20
)


class PostSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer()
    source = VideoSerializer()
    thumbnail = PhotoSerializer()
    challenge = MinimialChallengeSerializer()

    likes = serializers.IntegerField(source="post_like.count", read_only=True)
    comments = serializers.IntegerField(source="post_comment.count", read_only=True)
    reposts = serializers.IntegerField(source="post_repost.count", read_only=True)

    is_liked = serializers.SerializerMethodField(method_name="is_liked_method")
    is_reposted = serializers.SerializerMethodField(method_name="is_reposted_method")

    points = serializers.SerializerMethodField(method_name="points_method")

    tags = serializers.SerializerMethodField(method_name="tags_method")
    mentions = serializers.SerializerMethodField(method_name="mentions_method")

    def is_liked_method(self, instance):
        request_user_id = self.context.get("request_user_id")
        try:
            return Like.objects.filter(post=instance, user__id=request_user_id).exists()
        except:
            return False

    def is_reposted_method(self, instance):
        request_user_id = self.context.get("request_user_id")
        try:
            return Repost.objects.filter(
                post=instance, user__id=request_user_id
            ).exists()
        except:
            return False

    def points_method(self, instance):
        try:
            post = (
                Post.objects.annotate(points=points_calculation)
                .values("points")
                .get(id=instance.id)
            )
            return post.get("points")
        except:
            return 0

    def tags_method(self, instance):
        try:
            tags = Tag.objects.filter(post=instance, explicit=True)
            return list(map(lambda x: x.tag, tags))
        except:
            return []

    def mentions_method(self, instance):
        request_user_id = self.context.get("request_user_id")
        try:
            mentions = Mention.objects.filter(post=instance)
            return list(
                map(
                    lambda x: MinimalUserSerializer(
                        x.user, context={"request_user_id": request_user_id}
                    ).data,
                    mentions,
                )
            )
        except:
            return []

    class Meta:
        model = Post
        fields = [
            "id",
            "caption",
            "source",
            "thumbnail",
            "user",
            "challenge",
            "allow_comments",
            "time",
            "is_liked",
            "is_reposted",
            "likes",
            "comments",
            "filter_name",
            "ratio",
            "reposts",
            "points",
            "tags",
            "mentions",
        ]


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    user = MinimalUserSerializer()
    reply_to = serializers.PrimaryKeyRelatedField(read_only=True)
    likes = serializers.IntegerField(source="comment_like.count", read_only=True)
    replies = serializers.IntegerField(source="comment_reply.count", read_only=True)
    is_liked = serializers.SerializerMethodField(method_name="is_liked_method")

    def is_liked_method(self, instance):
        request_user_id = self.context.get("request_user_id")
        try:
            return CommentLike.objects.filter(
                comment=instance, user__id=request_user_id
            ).exists()
        except:
            return False

    class Meta:
        model = Comment
        fields = [
            "id",
            "comment",
            "time",
            "reply_to",
            "post",
            "user",
            "likes",
            "is_liked",
            "replies",
        ]
