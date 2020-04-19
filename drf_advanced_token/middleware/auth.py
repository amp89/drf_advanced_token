from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

class ProcessToken:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_token_str = request.META.get("HTTP_AUTHORIZATION", None)
        if request.user.is_anonymous and auth_token_str:
            try:
                new_user = Token.objects.get(key=auth_token_str.split(" ")[1]).user
            except (ObjectDoesNotExist, IndexError, AttributeError):
                new_user = None

            if "Token" == auth_token_str.split(" ")[0] and new_user:
                request.user = new_user
            else:
                return JsonResponse({"detail": "Authentication credentials were not provided."}, status=401)    

        response = self.get_response(request)


        return response