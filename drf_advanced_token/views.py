from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import QueryDict
# Create your views here.
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

class GetToken(APIView):
    def post(self, request, *args, **kwargs):
        authentication_classes = []
        permission_classes = ()
        req_dict = QueryDict.dict(request.data)
        try:

            user = authenticate(username=req_dict["username"], password=req_dict["password"])
            if user:
                try:
                    token = Token.objects.get(user=user)
                    if not token.key or (token.key and token.key.strip() == ""):
                        token.delete()
                        raise ObjectDoesNotExist
                except ObjectDoesNotExist:
                    token = Token.objects.create(user=user, key=f"{str(uuid.uuid4())}")
                key = token.key
                return Response({"token":key}, 200)
            else:
                return Response(None, 401)
        except Exception as e:
            print(e)
            return Response(None, 403)
        
        

class TokenAuth(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        if request.user:
            return Response(None, 200)

    def put(self, request, *args, **kwargs):
        if hasattr(settings,"PREVENT_TOKEN_API_CHANGE") and settings.PREVENT_TOKEN_API_CHANGE == True:
            return Response(None, 405)
        else:
            old_token = Token.objects.get(user=request.user)
            old_token.delete()
            token = Token.objects.create(user=request.user, key=f"{str(uuid.uuid4())}")
            return Response({"token":token.key}, 200)
    
class Logout(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        if hasattr(settings,"PREVENT_TOKEN_LOGOUT") and settings.PREVENT_TOKEN_LOGOUT == True:
            return Response(None, 405)
        else:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response(None, 200)

 