from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from django.http import JsonResponse

from pulsar.decorators.jwt_required import jwt_required


@csrf_exempt
@jwt_required()
def reset_password(request, **kwargs):
    if request.method != "POST":
        return JsonResponse(
            status=405, data={"message": "The method you're using is invalid"}
        )

    user_id = kwargs.get("request_user")

    new_password = request.POST.get("password")

    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return JsonResponse(
            status=404,
            data={
                "message": "The user you're trying to update does not exist. Please try a valid user."
            },
        )

    user.set_password(new_password)
    user.save()

    return JsonResponse(status=200, data={"message": "Password changed successfully"})
