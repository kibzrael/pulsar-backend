from django.http.response import JsonResponse
from django.core.handlers.wsgi import WSGIRequest


def post(func):
    def wrapper(*args, **kwargs):
        is_request: bool = type(args[0]) is WSGIRequest
        request = args[0] if is_request else args[1]
        if request.method != "POST":
            return JsonResponse(
                status=405, data={"message": "The method you're using is invalid"}
            )
        f = func(*args, **kwargs)
        return f

    return wrapper
