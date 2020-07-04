from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from .serializers import(
    CreateBlogSerializer,
    BlogSerializer,
    CreateCommentSerializer,
    CommentSerializer,
    CreateSubCommentSerializer,
    SubCommentSerializer,
    ActionBlogSerializer
)
from .models import (
    Blog,
    Comment,
    SubComment,
)
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from django.http import Http404
from rest_framework.decorators import (api_view,
                                       authentication_classes,
                                       permission_classes
                                       )
from rest_framework.permissions import IsAuthenticated
from django.conf import settings


ACTIONS = settings.ACTIONS


# Create your views here.


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def create_blog(request, *args, **kwargs):
    """
    CREATE BLOG API
    """
    if request.method == 'POST':
        serializer = CreateBlogSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def items_list(request):
    """
    list of items or create a new line
    """
    if request.method == 'GET':
        item = Blog.objects.order_by('-created').order_by("-created")
        serializer = BlogSerializer(item, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def items_details(request, pk,  *args, **kwargs):
    """
    THIS PRINTS OUT THE DETAILS WHEN CLICKED
    AND YOU CAN GET A PARTICULAR POST OR DELETE
    """
    try:
        item = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializers = BlogSerializer(item)
        return Response(serializers.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def items_delete(request, pk,  *args, **kwargs):
    """
    THIS DELETE IF THE USERS OWNS THE POST
    """
    try:
        qs = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        qs = qs.filter(user=request.user)
        if not qs.exists():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        obj = qs.first()
        obj.delete()
        return Response(status=status.HTTP_2O1_NO_CONTENT)


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def actions(request, *args, **kwargs):
    """
    IF ACTION PASSED IS VALID RUN ACTIONS API
    ID IS REQUIRED
    ACTIONS = LIKE, UNLIKE, RE_BLOG
    """
    if request.method == 'POST':
        serializer = ActionBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("id")
            action = data.get("action")
            details = data.get("details")
            qs = Blog.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "like":
                obj.likes.add(request.user)
                serializer = BlogSerializer(obj)
                return Response(serializer.data)
            elif action == "unlike":
                obj.likes.remove(request.user)
                serializer = BlogSerializer(obj)
                return Response(serializer.data)
            elif action == "reblog":
                new_blog = Blog.objects.create(
                    user=request.user,
                    parent=obj,
                    details=details
                )
                serializer = BlogSerializer(new_blog)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment(request, *args, **kwargs):
    """
    ADD COMMENT TO BLOG
    """

    if request.method == 'POST':
        serializer = CreateCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_list(request, id, *args, **kwargs):
    """
    TO RETURN COMMENT BASED ON THE comment reference
    """

    if request.method == 'GET':
        qs = Comment.objects.filter(blog=id).order_by('-created')
        serializer = CommentSerializer(qs, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_details(request, id, *args, **kwargs):
    """
    TO RETURN COMMENT BASED ON THE comment reference
    """

    if request.method == 'GET':
        item = Comment.objects.filter(id=id)
        serializer = CommentSerializer(item)
        return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, pk,  *args, **kwargs):
    """
    THIS DELETE IF THE USERS OWNS THE COMMENT
    """
    try:
        item = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        user = item.filter(user=request.user)
        if not user.exists():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        item.delete()
        return Response(status=status.HTTP_2OO_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_subcomment(request, id, *args, **kwargs):
    """
    ADD A SUB COMMENT TO A COMMENT
    """
    try:
        item = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = CreateSubCommentSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subcomment_list(request, id, *args, **kwargs):
    """
    TO RETURN COMMENT BASED ON THE comment reference
    """

    if request.method == 'GET':
        qs = SubComment.objects.filter(blog=id).order_by('-created')
        serializer = CommentSerializer(qs, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subcomment_details(request, id, *args, **kwargs):
    """
    TO RETURN COMMENT BASED ON THE comment reference
    """

    if request.method == 'GET':
        item = SubComment.objects.filter(id=id)
        serializer = SubCommentSerializer(item)
        return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def subcomment_delete(request, pk,  *args, **kwargs):
    """
    THIS DELETE IF THE USERS OWNS THE COMMENT
    """
    try:
        item = SubComment.objects.get(pk=pk)
    except SubComment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        user = item.filter(user=request.user)
        if not user.exists():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        item.delete()
        return Response(status=status.HTTP_2OO_NO_CONTENT)
