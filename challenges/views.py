from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from challenges.models import Challenge
from challenges.serializers import ChallengeSerializer

from pulsar.decorators.jwt_required import jwt_required


@method_decorator(csrf_exempt, name="dispatch")
class ChallengeView(View):
    @jwt_required()
    def get(self, request, challenge_id, *args, **kwargs):
        request_user_id = kwargs.get("request_user")
        try:
            challenge = Challenge.objects.get(id=challenge_id)
            data = ChallengeSerializer(
                instance=challenge, context={"request_user_id": request_user_id}
            ).data
            return JsonResponse(status=200, data={"challenge": data})
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={"message": "The challenge you've entered does not exist."},
            )
