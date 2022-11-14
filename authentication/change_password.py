from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from pulsar.decorators.jwt_required import jwt_required


@csrf_exempt
@jwt_required()
def change_password(request, **kwargs):
    if request.method != 'POST':
        return JsonResponse(status=405, data={'message': 'The method you\'re using is invalid'})

    user_id = kwargs.get('request_user')

    old_password = request.POST.get('oldPassword')
    new_password = request.POST.get('password')

    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return JsonResponse(status=404, data={
            'message': 'The user you\'re trying to update does not exist. Please try a valid user.'})

    authenticated_user = authenticate(
        username=user.username, password=old_password)
    if not authenticated_user:
        return JsonResponse(status=403,
                            data={'message': 'The password you\'ve provided does not match your current password'})

    authenticated_user.set_password(new_password)
    authenticated_user.save()

    return JsonResponse(status=200, data={'message': 'Password changed successfully'})
