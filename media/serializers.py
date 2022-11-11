from rest_framework import serializers

from media.models import Photo, Video

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        exclude = ['id','thumbnail_blob','medium_blob','high_blob']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        exclude = ['id','low_blob','medium_blob','high_blob']