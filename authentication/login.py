from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

#
from users.models import Device, User
from users.serializers import UserSerializer
from users.interests import get_interests


@csrf_exempt
def log_in(request):
    if request.method != "POST":
        return JsonResponse(
            status=405, data={"message": "The method you're using is invalid"}
        )

    info = request.POST.get("info")
    password = request.POST.get("password")

    device_token = request.POST.get("device")

    # # user_info not none, null
    if not password or not info:
        return JsonResponse(
            status=422, data={"message": "Please enter valid credentials to login."}
        )

    try:
        user = (
            User.objects.filter(
                Q(username=info)
                | Q(email=info)
                # | Q(phone=info)
            )
            .values()
            .get()
        )
        user.pop("password", None)

    except ObjectDoesNotExist:
        return JsonResponse(
            status=404,
            data={
                "message": "Sorry the user you've entered does not exist. Please try a valid user."
            },
        )

    authenticated_user = authenticate(username=user["username"], password=password)

    if not authenticated_user:
        return JsonResponse(
            status=401,
            data={
                "message": "The password you've entered is incorrect. "
                "It does not match the user you are trying to login."
            },
        )

    login(request, authenticated_user)
    if device_token:
        device = Device(user=authenticated_user, token=device_token)
        device.save()
    user_info = UserSerializer(instance=authenticated_user).data

    user_info["interests"] = get_interests(authenticated_user)

    jwt_token = authenticated_user.generate_token()
    user_info["jwtToken"] = jwt_token

    return JsonResponse(
        status=200,
        data={
            "message": "Login successful",
            "user": user_info,
        },
    )
