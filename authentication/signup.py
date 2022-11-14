from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from users.models import Device, User, UserSerializer
from users.interests import get_interests


@csrf_exempt
def sign_up(request):
    if request.method != "POST":
        return JsonResponse(
            status=405, data={"message": "The method you're calling is invalid"}
        )

    username = request.POST.get("username")
    email = request.POST.get("email")
    category = request.POST.get("category")
    password = request.POST.get("password")
    is_super = request.POST.get("super")

    device_token = request.POST.get("device")

    try:
        if is_super:
            user = User.objects.create_superuser(
                username=username, email=email, password=password, category=category
            )
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password, category=category
            )

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

    # return available interests and suggested username(s)
    # if the format is pulse23434
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
