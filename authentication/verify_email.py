import random

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from media.serializers import PhotoSerializer
from pulsar.email import send_template_email
from users.models import User


@csrf_exempt
def verify_email(request):
    if request.method != "POST":
        return JsonResponse(
            status=405, data={"message": "The method you're using is invalid"}
        )

    email = request.POST.get("email")
    username = request.POST.get("username")

    if not email:
        return JsonResponse(status=401, data={"message": "Please enter a valid email"})

    try:
        user: User = User.objects.filter(Q(email=email) | Q(username = username)).get()
    except ObjectDoesNotExist:
        return JsonResponse(
            status=404, data={"message": "The user you've entered does not exist."}
        )
    except MultipleObjectsReturned:
        return JsonResponse(
            status=409, data={"message": "The email already exists."}
        )

    token = user.generate_token()

    code: int = random.randint(1000, 9999)

    #   Send code to email/phone
    send_template_email(
        email if username else user.email ,
        "Email Verification",
        "verify_email",
        {"code": code, "full_name": user.fullname},
    )

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
