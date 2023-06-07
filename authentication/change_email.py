from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from pulsar.decorators.jwt_required import jwt_required
from users.models import User


@csrf_exempt
@jwt_required()
def change_email(request, **kwargs):
    if request.method != "POST":
        return JsonResponse(
            status=405, data={"message": "The method you're using is invalid"}
        )

    user_id = kwargs.get("request_user")

    email = request.POST.get("email", "")
    if not email or len(email) < 1:
        return JsonResponse(
            status=422,
            data={
                "message": "The email you've entered is not valid. "
                "Please enter a valid email"
            },
        )

    try:
        user = User.objects.get(id=user_id)
        if user.email == email:
            return JsonResponse(
                status=201,
                data={
                    "message": "The email you've provided is your current email. "
                    "Try another one if you're willing to change."
                },
            )
        user.email = email
        user.save()
    except ObjectDoesNotExist:
        return JsonResponse(
            status=404,
            data={
                "message": "The user you're trying to update does not exist. Please try a valid user"
            },
        )
    except IntegrityError:
        return JsonResponse(
            status=404,
            data={
                "message": "The email you've provided already exists. Please try a unique email"
            },
        )
    return JsonResponse(
        status=200, data={"message": "Your email has been changed successfully"}
    )
