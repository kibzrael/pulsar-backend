from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from django.core.files.uploadedfile import InMemoryUploadedFile
from challenges.models import Challenge
from challenges.serializers import ChallengeSerializer
from media.serializers import Photo
from users.category import Category
from media.photo import upload_photo
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_challenge(request, **kwargs):
    if request.method != "POST":
        return JsonResponse(
            status=405,
            data={"message": "The method you are trying to accessed is not allowed"},
        )

    name = request.POST.get("name")
    description = request.POST.get("description")
    category = request.POST.get("category")
    cover: InMemoryUploadedFile = request.FILES.get("cover")

    if not cover or not name or not description:
        return JsonResponse(
            status=422,
            data={
                "message": "Please enter the name, description and cover of the challenge."
            },
        )

    if len(name) > 24:
        return JsonResponse(
            status=422,
            data={"message": "Please enter a name that has 24 characters or less."},
        )
    if len(description) > 255:
        return JsonResponse(
            status=422,
            data={
                "message": "Please enter a description that has 255 characters or less."
            },
        )

    category_object = None

    try:
        category_object = Category.objects.filter(name__iexact=category).get()
    except ObjectDoesNotExist:
        return JsonResponse(
            status=404, data={"message": "The category you've entered does not exist."}
        )

    thumbnail, medium, high, thumbnail_blob, medium_blob, high_blob = upload_photo(
        cover, f"challenges/{name}-{datetime.now()}", []
    )
    cover_media = Photo(
        thumbnail=thumbnail,
        medium=medium,
        high=high,
        thumbnail_blob=thumbnail_blob,
        medium_blob=medium_blob,
        high_blob=high_blob,
    )
    cover_media.save()

    challenge = Challenge(
        name=name, description=description, category=category_object, cover=cover_media
    )

    challenge.save()

    challenge_info = ChallengeSerializer(instance=challenge).data

    return JsonResponse(
        status=201,
        data={
            "message": "Challenge Created successfully.",
            "challenge": challenge_info,
        },
    )
