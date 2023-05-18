from datetime import date
import requests

from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http.response import JsonResponse

from authentication.models import Provider, User
from pulsar.decorators.post import post
from pulsar.settings import GOOGLE_CLIENT_SECRET, GOOGLE_CLIENT_ID, DEBUG
from users.interests import get_interests
from users.models import Device
from users.serializers import UserSerializer

endpoint = "https://oauth2.googleapis.com/token"


def link_provider(user: User, provider_id, auth_code, acc_token):
    refresh_token = None
    access_token = acc_token
    if auth_code:
        # exchange code for refresh token and new access token
        response = requests.post(
            endpoint,
            data={
                "code": auth_code,
                "grant_type": "authorization_code",
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
            },
        )
        data = response.json()
        refresh_token = data.get("refresh_token")
        access_token = data.get("access_token", acc_token)

    # Link user with provider
    provider = Provider(
        user=user,
        name="google",
        provider_id=provider_id,
        access_token=access_token,
        refresh_token=refresh_token,
    )
    provider.save()
    return provider


def refresh_token(provider: Provider):
    response = requests.post(
        endpoint,
        data={
            "refresh_token": provider.refresh_token,
            "grant_type": "refresh_token",
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
        },
    )
    data = response.json()
    print(data)
    provider.access_token = data.get("access_token", provider.access_token)
    provider.save()


@csrf_exempt
@post
def sign_in(request):
    provider_id = request.POST.get("id")
    access_token = request.POST.get("access_token")
    auth_code = request.POST.get("auth_code")

    email = request.POST.get("email")
    device_token = request.POST.get("device")

    provider = None
    linked = False

    try:
        provider = Provider.objects.filter(name="google").get(provider_id=provider_id)
    except ObjectDoesNotExist:
        try:
            user = User.objects.get(email=email)
            # link user with additional provider
            provider = link_provider(user, provider_id, auth_code, access_token)
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
    auth_code = request.POST.get("auth_code")

    username = request.POST.get("username")
    email = request.POST.get("email")
    device_token = request.POST.get("device")

    # use access token to fetch birthday
    response = requests.get(
        " https://people.googleapis.com/v1/people/me?personFields=birthdays",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json()
    birthdays = data.get("birthdays")
    dob = None
    if birthdays:
        if len(birthdays) > 0:
            d = birthdays[0].get("date")
            dob = date(day=d.get("day"), month=d.get("month"), year=d.get("year"))

    # create new user
    try:
        user: User = User.objects.create_user(username=username, email=email)
        if dob:
            user.date_of_birth = dob
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

    link_provider(user, provider_id, auth_code, access_token)

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
