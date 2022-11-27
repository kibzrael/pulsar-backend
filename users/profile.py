from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http.response import JsonResponse
from django.views import View
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.decorators import method_decorator
from media.serializers import Photo

from users.models import User
from users.serializers import UserSerializer
from users.category import Category
from pulsar.decorators.jwt_required import jwt_required
from media.photo import upload_photo
from users.interests import get_interests, save_interests


@method_decorator(csrf_exempt, name="dispatch")
class Profile(View):
    @jwt_required()
    def get(self, request, user_id, **kwargs):
        request_user_id = kwargs.get("request_user")

        try:
            user = User.objects.get(id=user_id)
            user_info = UserSerializer(
                instance=user, context={"request_user_id": kwargs.get("request_user")}
            ).data
            if user_id == request_user_id:
                fetched_interests = get_interests(user)
                user_info["interests"] = fetched_interests
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={
                    "message": "The user you've provided does not exist. Please try a valid user"
                },
            )

        return JsonResponse(
            status=200,
            data={
                "user": user_info,
            },
        )

    @jwt_required()
    def post(self, request, user_id, **kwargs):
        request_user_id = kwargs.get("request_user")
        if user_id != request_user_id:
            return JsonResponse(
                status=403,
                data={"message": "You are not authorized to access this endpoint"},
            )

        try:
            user: User = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={
                    "message": "The user you're trying to update does not exist. Please try a valid user."
                },
            )

        category_name = request.POST.get("category")
        fullname = request.POST.get("fullname", user.fullname)
        bio = request.POST.get("bio", user.bio)
        # Y-M-D
        date_of_birth = request.POST.get("DOB", user.date_of_birth)
        portfolio = request.POST.get("portfolio", user.portfolio)
        interests = request.POST.get("interests", "")

        remove_profile_pic = request.POST.get("removeProfilePic", False)

        if remove_profile_pic:
            pass
        else:
            profile_pic: InMemoryUploadedFile = request.FILES.get("profilePic")

            profile_pic_media = Photo.objects.filter(user__id=user.id).first()

            if profile_pic:
                (
                    thumbnail,
                    medium,
                    high,
                    thumbnail_blob,
                    medium_blob,
                    high_blob,
                ) = upload_photo(
                    profile_pic,
                    f"profile pictures/{user_id}",
                    previous_links=[
                        profile_pic_media.thumbnail,
                        profile_pic_media.medium,
                        profile_pic_media.high,
                    ]
                    if profile_pic_media
                    else [],
                )
                if profile_pic_media:
                    profile_pic_media.thumbnail = thumbnail
                    profile_pic_media.medium = medium
                    profile_pic_media.high = high
                else:
                    profile_pic_media = Photo(
                        thumbnail=thumbnail,
                        medium=medium,
                        high=high,
                        thumbnail_blob=thumbnail_blob,
                        medium_blob=medium_blob,
                        high_blob=high_blob,
                    )
                profile_pic_media.save()

        category = user.category

        if category_name:
            try:
                category_query = Category.objects.filter(
                    name__iexact=category_name
                ).get()
                category = category_query
            except ObjectDoesNotExist:
                pass

        try:
            User.objects.filter(id=user_id).update(
                category=category,
                bio=bio,
                date_of_birth=date_of_birth,
                portfolio=portfolio,
                fullname=fullname,
                profile_pic=profile_pic_media,
            )
        except ValidationError:
            return JsonResponse(
                status=422,
                data={
                    "message": "The date you've entered is not a valid date. "
                    "Please format it as %Y-%M-%D"
                },
            )

        user = User.objects.get(id=user_id)
        save_interests(user, interests)

        user_info = UserSerializer(instance=user).data

        fetched_interests = get_interests(user)
        user_info["interests"] = fetched_interests

        return JsonResponse(
            status=200,
            data={
                "user": user_info,
                # 'profile Pic': profile_pic
            },
        )
