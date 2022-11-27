from rest_framework import serializers
from authentication.models import User
from media.serializers import PhotoSerializer

from users.models import Follow


class UserSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field="user")
    profile_pic = PhotoSerializer()
    followers = serializers.IntegerField(source="followedId.count", read_only=True)
    posts = serializers.IntegerField(source="user_post.count", read_only=True)

    is_following = serializers.SerializerMethodField(method_name="is_following_method")

    def is_following_method(self, instance):
        request_user_id = self.context.get("request_user_id")
        try:
            return Follow.objects.filter(
                user=instance, follower__id=request_user_id
            ).exists()
        except:
            return False

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "category",
            "profile_pic",
            "fullname",
            "email",
            "bio",
            "portfolio",
            "is_following",
            "posts",
            "followers",
            "date_of_birth",
            "date_joined",
            "is_superuser",
        ]


class MinimalUserSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field="user")
    profile_pic = PhotoSerializer()
    is_following = serializers.SerializerMethodField(method_name="is_following_method")

    def is_following_method(self, instance):
        request_user_id = self.context.get("request_user_id")
        print(f"{instance.id}-{request_user_id}")
        try:
            return Follow.objects.filter(
                user=instance, follower__id=request_user_id
            ).exists()
        except:
            return False

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "category",
            "profile_pic",
            "fullname",
            "is_following",
        ]
