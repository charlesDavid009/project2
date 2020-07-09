from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from .serializers import(
    ProfileSerializer,
    CreateProfileSerializer,
    ActionProfileSerializer
)
from .models import (
    Profile
)
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings


ACTIONS = settings.ACTIONS


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, *args, **kwargs):
    qs = Profile.objects.filter(user=request.user)
    if not qs.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    obj = qs.first()

    if request.method == 'GET':
        serializer = ProfileSerializer(obj)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_user(request, username, *args, **kwargs):
    try:
        user = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(user)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_profile(request, *args, **kwargs):

    if request.method == 'POST':
        serializer = CreateProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def actions(request, *args, **kwargs):
    """
    IF ACTION PASSED IS VALID RUN ACTIONS API
    ID IS REQUIRED
    ACTIONS = Follow
    """
    if request.method == 'POST':
        serializer = ActionProfileSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            profile = data.get("id")
            action = data.get("action")
            qs = Profile.objects.filte(user_id=profile)
            if not qs.exsits():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "follow":
                obj.followers.add(obj)
                serializer = ProfileSerializer(obj)
                return Response(serializer.data)
            elif action == "unfollow":
                obj.followers.remove(obj)
                serializer = ProfileSerializer(obj)
                return Response(serializer.data)
            else:
                pass
