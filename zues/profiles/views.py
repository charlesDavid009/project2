from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from .serializers import(
    ProfileSerializer,
    CreateProfileSerializer,
    ActionProfileSerializer,
    FollowSerializer
)
from .models import (
    Profile,
    Follow
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
def user_followers(request, *args, **kwargs):
    qs = Profile.objects.filter(user=request.user)
    if not qs.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    obj = qs.first()
    
    if request.method == 'GET':
        item = Follow.objects.filter(profiles= obj).order_by('-created_at')
        serializer = FollowSerializer(item, many=True)
        return Response(serializer.data)


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
def get_user(request, id, *args, **kwargs):
    try:
        user = Profile.objects.get(user__id=id)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_following(request,  *args, **kwargs):
    if request.method == 'GET':
        user = request.user
        qs = Follow.objects.following_feed(users)
        serializer = FollowSerializer(qs, many=True)
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
def actions(request,  *args, **kwargs):
    """
    IF ACTION PASSED IS VALID RUN ACTIONS API
    ID IS REQUIRED
    ACTIONS = Follow
    """
    if request.method == 'POST':
        serializer = ActionProfileSerializer(data=request.data)
        me = request.user 
        if serializer.is_valid():
            data = serializer.validated_data
            profile = data.get("id")
            qs = Profile.objects.filter(user__id=profile)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if me == obj:
                counted.qs = profile.following.all()
                return Response({"following":counted.qs.count()}, status=status.HTTP_200_OK )
            action = data.get("action")
            if action == "follow":
                obj.followers.add(me)
                serializer = ProfileSerializer(obj)
                return Response(serializer.data)
            elif action == "unfollow":
                obj.followers.remove(me)
                serializer = ProfileSerializer(obj)
                return Response(serializer.data)
            else:
                pass
