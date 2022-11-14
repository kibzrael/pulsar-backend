from authentication.username_functions import not_username_exists, validate_username
from users.models import User
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from pulsar.decorators.jwt_required import jwt_required


@csrf_exempt
@jwt_required()
def change_username(request, **kwargs):
    if request.method != "POST":
        return JsonResponse(
            status=405, data={"message": "The method you're using is invalid"}
        )

    user_id = kwargs.get("request_user")

    username = request.POST.get("username", "")
    if not username or len(username) < 1:
        return JsonResponse(
            status=422,
            data={
                "message": "The username  you've entered is not valid. "
                "Please enter a valid username"
            },
        )
    if not validate_username(username):
        return JsonResponse(
            status=422,
            data={
                "message": "The username  you've entered is not valid. "
                "The username can only contain letters, numbers and ._ with a maximum of 15 characters"
            },
        )

    try:
        user = User.objects.get(id=user_id)
        if user.username == username:
            return JsonResponse(
                status=201,
                data={
                    "message": "The username you've provided is your current username. "
                    "Try another one if you're willing to change."
                },
            )
        if not not_username_exists(username):
            return JsonResponse(
                status=400,
                data={
                    "message": "The username you've provided already exists. Please try a unique username"
                },
            )
        user.username = username
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
                "message": "The username you've provided already exists. Please try a unique username"
            },
        )
    return JsonResponse(
        status=200, data={"message": "Your username has been changed successfully"}
    )
