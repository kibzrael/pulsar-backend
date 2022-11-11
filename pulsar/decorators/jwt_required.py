from django.http.response import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
import jwt

from authentication.models import User


def jwt_required():
    def decorator(func):
        def wrapper(*args, **kwargs):
            is_request: bool = type(args[0]) is WSGIRequest
            request = args[0] if is_request else args[1]
            user_jwt = request.headers.get('Authorization')
            if not user_jwt:
                return JsonResponse(status=403, data={'message': 'You are not authorized to access this endpoint'})
            try:
                request_user = jwt.decode(
                    str(user_jwt), key='rs-pulsar', algorithms="HS256")

                User.objects.filter(id=request_user['id']).get()
            except:
                return JsonResponse(status=403, data={'message': 'You are not authorized to access this endpoint'})
            f = func(*args, **kwargs, request_user=request_user['id'])
            return f

        return wrapper
    return decorator
