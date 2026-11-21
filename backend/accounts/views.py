from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, UserSerializer

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return Response(UserSerializer(user, context={"request":request}).data, status=201)
    return Response(serializer.errors, status=400)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    user = authenticate(request, username=request.data.get("username",""), password=request.data.get("password",""))
    if not user:
        return Response({"detail":"Username or password is incorrect."}, status=400)
    login(request, user)
    return Response(UserSerializer(user, context={"request":request}).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"detail":"You are signed out."})

@api_view(["GET","PATCH"])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def me(request):
    if not request.user.is_authenticated:
        return Response({"detail":"Authentication required."}, status=401)
    user = request.user
    if request.method == "PATCH":
        for field in ["first_name","last_name","email"]:
            if field in request.data: setattr(user, field, request.data[field])
        user.save()
        profile = user.profile
        if "bio" in request.data: profile.bio = request.data["bio"]
        if "avatar" in request.FILES: profile.avatar = request.FILES["avatar"]
        profile.save()
    return Response(UserSerializer(user, context={"request":request}).data)
