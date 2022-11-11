
from rest_framework import serializers

from posts.models import Comment, Like, Post, Repost
from challenges.serializers import MinimialChallengeSerializer
from media.serializers import PhotoSerializer, VideoSerializer
from users.serializers import MinimalUserSerializer

class PostSerializer (serializers.ModelSerializer):
    user = MinimalUserSerializer()
    source = VideoSerializer()
    thumbnail = PhotoSerializer()
    challenge = MinimialChallengeSerializer()

    likes = serializers.IntegerField(source='post_like.count', read_only=True)
    comments = serializers.IntegerField(
        source='post_comment.count', read_only=True)
    reposts = serializers.IntegerField(
        source='post_repost.count', read_only=True)

    is_liked = serializers.SerializerMethodField(method_name='is_liked_method')
    is_reposted = serializers.SerializerMethodField(
        method_name='is_reposted_method')

    def is_liked_method(self, instance):
        request_user_id = self.context.get('request_user_id')
        try:
            return Like.objects.filter(post=instance, user__id=request_user_id).exists()
        except:
            return False

    def is_reposted_method(self, instance):
        request_user_id = self.context.get('request_user_id')
        try:
            return Repost.objects.filter(post=instance, user__id=request_user_id).exists()
        except:
            return False

    class Meta:
        model = Post
        fields = ['id',  'caption', 'source',
                  'thumbnail', 'user', 'challenge', 'allow_comments',
                  'time', 'is_liked', 'is_reposted', 'likes', 'comments', 'reposts']
        
        
class CommentSerializer (serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    user = MinimalUserSerializer()
    reply_to = serializers.PrimaryKeyRelatedField(read_only=True)
    likes = serializers.IntegerField(source='comment_like.count', read_only=True)
    replies = serializers.IntegerField(
        source='comment_reply.count', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'time', 'reply_to',  'post', 'user', 'likes', 'replies']