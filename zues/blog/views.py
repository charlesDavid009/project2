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
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.permissions import IsAuthenticated
from django.conf import settings


ACTIONS = settings.ACTIONS


# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
def items_user_list(request):
    """
    list of items or create a new line
    """
    if request.method == 'GET':
        item = Blog.objects.filter(user=request.user).order_by('-created')
        serializer = BlogSerializer(item, many=True)
        return Response(serializer.data)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def items_details(request, pk,  *args, **kwargs):
    """
    THIS PRINTS OUT THE DETAILS WHEN CLICKED
    AND YOU CAN GET A PARTICULAR POST OR DELETE
    """
    try:
        item = Blog.objects.get(id=pk)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':  
        serializers = BlogSerializer(item)
        return Response(serializers.data)
    
    qs= Blog.objects.filter(user=request.user)
    if qs.exists():
        obj = qs.first()
        if request.method == 'DELETE':
            item.delete()
            return Response(status=status.HTTP_203_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)



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
    
    try:
        qs = qs.objects.filter(user=request.user)
    except qs.DoesNotExist:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'DELETE':
        obj = qs.first()
        obj.delete()
        return Response(status=status.HTTP_2O1_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
            details = data.get("add")
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
                    content=details
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
            data = serializer.validated_data
            blog_id = data.get("blog_id")
            comments = data.get("text")
            qs = Blog.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            my_comment= Comment.objects.create(
                user=request.user,
                blog=obj,
                text=comments
            )
            serializer = CommentSerializer(my_comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_list(request, id, *args, **kwargs):
    """
    TO RETURN COMMENT BASED ON THE comment reference
    """
    try:
        item = Comment.objects.filter(blog=id).order_by('-created')
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = CommentSerializer(item, many=True)
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

    if request.method == 'GET':
        serializers = CommentSerializer (item)
        return Response(serializers.data)

    qs = Comment.objects.filter(user=request.user)
    if qs.exists():
        obj = qs.first()
        if request.method == 'DELETE':
            item.delete()
            return Response(status=status.HTTP_203_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_actions(request, *args, **kwargs):
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
            qs = Comment.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "like":
                obj.like.add(request.user)
                serializer = CommentSerializer(obj)
                return Response(serializer.data)
            elif action == "unlike":
                obj.like.remove(request.user)
                serializer = CommentSerializer(obj)
                return Response(serializer.data)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subcomment(request, *args, **kwargs):
    """
    ADD A SUB COMMENT TO A COMMENT
    """
    if request.method == 'POST':
        serializer = CreateSubCommentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("blog_id")
            comments = data.get("text")
            qs = Comment.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            my_comment = SubComment.objects.create(
                user=request.user,
                blog=obj,
                text=comments
            )
            serializer = SubCommentSerializer(my_comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
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
        item =SubComment.objects.get(pk=pk)
    except SubComment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializers = SubCommentSerializer(item)
        return Response(serializers.data)

    qs = SubComment.objects.filter(user=request.user)
    if qs.exists():
        obj = qs.first()
        if request.method == 'DELETE':
            item.delete()
            return Response(status=status.HTTP_203_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subcomment_actions(request, *args, **kwargs):
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
            qs = SubComment.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "like":
                obj.like.add(request.user)
                serializer = SubCommentSerializer(obj)
                return Response(serializer.data)
            elif action == "unlike":
                obj.like.remove(request.user)
                serializer = SubCommentSerializer(obj)
                return Response(serializer.data)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

