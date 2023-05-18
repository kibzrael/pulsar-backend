from rest_framework import serializers

from challenges.models import Challenge, Pin
from posts.models import Post

from media.serializers import PhotoSerializer


class ChallengeSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    cover = PhotoSerializer()
    pins = serializers.IntegerField(source="pin_set.count", read_only=True)
    posts = serializers.IntegerField(source="post_set.count", read_only=True)
    is_pinned = serializers.SerializerMethodField(method_name="is_pinned_method")
    is_joined = serializers.SerializerMethodField(method_name="is_joined_method")

    def is_pinned_method(self, instance):
        request_user_id = self.context.get("request_user_id")
        try:
            return Pin.objects.filter(
                challenge=instance, user__id=request_user_id
            ).exists()
        except:
            return False

    def is_joined_method(self, instance):
        request_user_id = self.context.get("request_user_id")
        try:
            return Post.objects.filter(
                challenge=instance, user__id=request_user_id
            ).exists()
        except:
            return False

    class Meta:
        model = Challenge
        fields = [
            "id",
            "name",
            "category",
            "description",
            "cover",
            "is_pinned",
            "is_joined",
            "pins",
            "posts",
            "value",
            "time_created",
        ]


class MinimialChallengeSerializer(serializers.ModelSerializer):
    cover = PhotoSerializer()

    class Meta:
        model = Challenge
        fields = ["id", "name", "cover"]
