from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from posts.models import Post
from posts.serializers import PostSerializer
from pulsar.decorators.jwt_required import jwt_required


@method_decorator(csrf_exempt, name="dispatch")
class InappropriateView(View):
    @jwt_required()
    def get(self, request, **kwargs):
        pass

    @jwt_required()
    def post(self, request, **kwargs):
        pass
