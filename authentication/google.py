from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse

from authentication.models import Provider, User
from users.interests import get_interests
from users.models import Device
from users.serializers import UserSerializer


def link_provider(user: User, provider_id, auth_code, access_token):
    refresh_token = None
    if auth_code:
        # exchange code for refresh token and new access token
        pass

    # Link user with provider
    provider = Provider(
        user=user,
        name="google",
        provider_id=provider_id,
        access_token=access_token,
        refresh_token=refresh_token,
    )
    provider.save()


@csrf_exempt
def sign_in(request):
    provider_id = request.POST.get("id")
    access_token = request.POST.get("access_token")
    auth_code = request.POST.get("auth_code")

    email = request.POST.get("email")
    device_token = request.POST.get("device")

    user = None
    linked = False

    try:
        provider = Provider.objects.filter(name="google").get(provider_id=provider_id)
        if provider.refresh_token:
            # refresh access_token
            pass
        # return the user
        user = provider.user
    except ObjectDoesNotExist:
        try:
            user = User.objects.get(email=email)
            # link user with additional provider
            link_provider(user, provider_id, auth_code, access_token)
            # return the user with linked message
            linked = True
        except ObjectDoesNotExist:
            pass

    if user:
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
def sign_up(request):
    provider_id = request.POST.get("id")
    access_token = request.POST.get("access_token")
    auth_code = request.POST.get("auth_code")

    username = request.POST.get("username")
    email = request.POST.get("email")
    device_token = request.POST.get("device")

    # use access token to fetch birthday
    # create new user
    try:
        user: User = User.objects.create_user(username=username, email=email)
    except ValueError as e:
        return JsonResponse(status=422, data={"message": str(e)})

    except Exception as e:
        return JsonResponse(
            status=500,
            data={
                "message": str(e)
                # 'message': 'Sorry, there has been a problem with our server. '
                #            'Please try again. If these persists please try again later',
            },
        )

    link_provider(user, provider_id, auth_code, access_token)
