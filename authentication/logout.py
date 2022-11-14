from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from users.models import Device
from pulsar.decorators.jwt_required import jwt_required


@jwt_required()
@csrf_exempt
def logout(request, device, **kwargs):
    user = kwargs.get("request_user")
    try:
        device: Device = Device.objects.filter(device=device, user=user).get()
        device.delete()
    except ObjectDoesNotExist:
        return JsonResponse(
            status=404, data={"message": "The device you've entered does not exist."}
        )
    else:
        return JsonResponse(status=200, data={"message": "Logged out successfully"})
