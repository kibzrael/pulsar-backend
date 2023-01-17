from datetime import datetime
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http.response import JsonResponse

from authentication.models import Provider, User
from pulsar.settings import DEBUG
from pulsar.decorators.post import post
from users.interests import get_interests
from users.serializers import UserSerializer
from users.models import Device


def link_provider(user: User, provider_id, access_token):
    # Link user with provider
    provider = Provider(
        user=user,
        name="facebook",
        provider_id=provider_id,
        access_token=access_token,
    )
    provider.save()
    return provider


@csrf_exempt
@post
def sign_in(request):
    provider_id = request.POST.get("id")
    access_token = request.POST.get("access_token")

    email = request.POST.get("email")
    device_token = request.POST.get("device")

    provider = None
    linked = False

    try:
        provider = Provider.objects.filter(name="facebook").get(provider_id=provider_id)
    except ObjectDoesNotExist:
        try:
            user = User.objects.get(email=email)
            # link user with additional provider
            provider = link_provider(user, provider_id, access_token)
            # return the user with linked message
            linked = True
        except ObjectDoesNotExist:
            pass
        except IntegrityError:
            return JsonResponse(
                status=422, data={"message": "The user is already linked to an account"}
            )

    if provider:
        if device_token:
            device = Device(user=provider.user, token=device_token)
            device.save()
        user_info = UserSerializer(instance=provider.user).data

        user_info["interests"] = get_interests(provider.user)

        jwt_token = provider.user.generate_token()
        user_info["jwtToken"] = jwt_token

        return JsonResponse(
            status=200,
            data={
                "message": "Signin successful",
                "linked": linked,
                "user": user_info,
            },
        )
    # return null
    return JsonResponse(
        status=404,
        data={
            "message": "There's no user with the given credentials",
        },
    )


@csrf_exempt
@post
def sign_up(request):
    provider_id = request.POST.get("id")
    access_token = request.POST.get("access_token")

    username = request.POST.get("username")
    email = request.POST.get("email")
    birthday = request.POST.get("birthday")
    device_token = request.POST.get("device")

    # use access token to fetch birthday

    # create new user
    try:
        user: User = User.objects.create_user(username=username, email=email)
        if birthday:
            user.date_of_birth = datetime.strptime(birthday, "%m/%d/%Y").date()
            user.save()
    except ValueError as e:
        return JsonResponse(status=422, data={"message": str(e)})

    except Exception as e:
        return JsonResponse(
            status=500,
            data={
                "message": str(e)
                if DEBUG
                else "Sorry, there has been a problem with our server. "
                "Please try again. If these persists please try again later",
            },
        )

    link_provider(user, provider_id, access_token)

    login(request, user)
    if device_token:
        device = Device(user=user, token=device_token)
        device.save()
    user_info = UserSerializer(instance=user).data

    user_info["interests"] = get_interests(user)

    jwt_token = user.generate_token()
    user_info["jwtToken"] = jwt_token

    return JsonResponse(
        status=201,
        data={
            "message": "User created successfully",
            "user": user_info,
        },
    )
