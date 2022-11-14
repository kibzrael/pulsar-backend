from datetime import datetime
from typing import List
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from challenges.models import Challenge
from media.serializers import Photo, Video

from posts.models import Post, Tag
from posts.serializers import PostSerializer
from users.models import User
from users.category import Category
from pulsar.decorators.jwt_required import jwt_required
from media.photo import upload_photo
from media.video import upload_video


@csrf_exempt
@jwt_required()
def create_post(request, **kwargs):

    if request.method != "POST":
        return JsonResponse(
            status=405,
            data={"message": "The method you are trying to accessed is not allowed"},
        )

    user_id = kwargs.get("request_user")
    source: InMemoryUploadedFile = request.FILES.get("source")
    thumb: InMemoryUploadedFile = request.FILES.get("thumbnail")

    source_medium: InMemoryUploadedFile = request.FILES.get("sourceMedium")
    source_low: InMemoryUploadedFile = request.FILES.get("sourceLow")

    if not source or not thumb:
        return JsonResponse(
            status=401, data={"message": "You need to provide a video and a thumbnail"}
        )

    caption: str = request.POST.get("caption", "")
    challenge = request.POST.get("challenge")
    allow_comments_input = request.POST.get("allowComments", "True")
    allow_comments: bool = allow_comments_input in ["True", "true"]

    filter_name = request.POST.get("filter")
    ratio = request.POST.get("ratio")

    tags = request.POST.get("tags", "")

    try:
        user: User = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return JsonResponse(
            status=403,
            data={"message": "You are not authorized to access this endpoint"},
        )

    challenge_object = None
    if challenge:
        try:
            challenge_object = Challenge.objects.get(id=int(challenge))
            Post.objects.get(user=user, challenge=challenge_object)
        except ObjectDoesNotExist:
            pass
        else:
            challenge_object = None

    (
        thumbnail,
        medium_thumb,
        high_thumb,
        thumbnail_blob,
        medium_thumb_blob,
        high_thumb_blob,
    ) = upload_photo(thumb, f"posts/thumbnails/{user_id}-{datetime.now()}", [])
    low, medium, high, low_blob, medium_blob, high_blob = upload_video(
        source, f"posts/videos/{user_id}-{datetime.now()}", source_medium, source_low
    )

    thumbnail_media = Photo(
        thumbnail=thumbnail,
        medium=medium_thumb,
        high=high_thumb,
        thumbnail_blob=thumbnail_blob,
        medium_blob=medium_thumb_blob,
        high_blob=high_thumb_blob,
    )
    thumbnail_media.save()

    source_media = Video(
        low=low,
        medium=medium,
        high=high,
        low_blob=low_blob,
        medium_blob=medium_blob,
        high_blob=high_blob,
    )
    source_media.save()

    post = Post(
        source=source_media,
        thumbnail=thumbnail_media,
        caption=caption,
        user=user,
        challenge=challenge_object,
        allow_comments=allow_comments,
        filter_name=filter_name,
    )
    post.save()

    hashtags = save_hashtags(post, caption)
    save_tags(post, tags)
    save_mentions(post, caption)

    post_info = PostSerializer(instance=post).data
    return JsonResponse(
        status=201,
        data={
            "message": "Post created successfully",
            "post": post_info,
            "hashtags": hashtags,
        },
    )


def save_hashtags(post: Post, caption: str, comment=None):
    allowed_characters = "abcdefghijklmnopqrstuvwxyz1234567890_"

    words: List = caption.split(" ")
    hashtags = []

    for word in words:

        if word.startswith("#"):
            hashtag: str = ""
            spoilt = False
            for i in range(len(word)):
                letter = word[i]

                if (
                    (
                        letter in allowed_characters
                        or letter.lower() in allowed_characters
                    )
                    and len(hashtag) < 15
                    and not spoilt
                ):
                    hashtag += letter.lower()
                else:
                    if letter != "#":
                        spoilt = True
                    elif letter == "#" and hashtag != "":
                        hashtags.append(hashtag)
                        hashtag = ""

            hashtags.append(hashtag)
            tag = Tag(post=post, tag=hashtag, comment=comment)
            tag.save()

    return hashtags


def save_tags(post: Post, tag: str):
    # Delete existing interests
    tagList: List = tag.split(",")
    for tagString in tagList:
        try:
            category = Category.objects.get(name__iexact=tagString)
        except ObjectDoesNotExist:
            pass
        else:
            interest = Tag(post=post, tag=tagString, explicit=True)
            interest.save()


def save_mentions(post: Post, caption: str):
    pass
