from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from media.serializers import PhotoSerializer
from users.models import User
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def recover_account(request):

    if request.method != "POST":
        return JsonResponse(
            status=405, data={"message": "The method you're using is invalid"}
        )

    info = request.POST.get("info")

    if not info:
        return JsonResponse(
            status=401, data={"message": "Please enter valid information"}
        )

    try:
        user: User = User.objects.filter(
            Q(username=info)
            | Q(email=info)
            # | Q(phone=info)
        ).get()
    except ObjectDoesNotExist:
        return JsonResponse(
            status=404, data={"message": "The user you've entered does not exist."}
        )

    token = user.generate_token()

    code: int = 2495

    #   Send code to email/phone

    return JsonResponse(
        status=200,
        data={
            "message": f"A code has been sent to {user.email}",
            "code": code,
            "user": {
                "id": user.id,
                "username": user.username,
                "category": user.category.user,
                "profile_pic": PhotoSerializer(instance=user.profile_pic).data,
                "email": user.email,
                "jwtToken": token,
            },
        },
    )
