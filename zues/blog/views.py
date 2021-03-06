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
    ActionBlogSerializer,
    BlogLikesSerializer,
    CommentLikesSerializer,
    SubCommentLikesSerializer
)
from .models import (
    Blog,
    Comment,
    SubComment,
    BlogLikes,
    CommentLikes,
    SubCommentLikes
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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def items_list(request, *args, **kwargs):
    """
    list of items or create a new line
    """
    if request.method == 'GET':
        item = Blog.objects.order_by('-created').order_by("-created")
        serializer = BlogSerializer(item, many=True)
        return Response(serializer.data)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blog_feeds(request, *args, **kwargs):
    """
    BLOG FEEDS OF USER AND USERS FOLLOWED
    """
    if request.method == 'GET':
        user = request.user
        qs = Blog.objects.feed(user)
        serializer = BlogSerializer(qs, many=True)
        return Response(serializer.data)

@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
def blog_user_list(request, *args, **kwargs):
    """
    BLOG OD USER ONLY
    """
    if request.method == 'GET':
        item = Blog.objects.filter(user=request.user).order_by('-created')
        serializer = BlogSerializer(item, many=True)
        return Response(serializer.data)
    
    qs= Blog.objects.filter(user=request.user)
    if qs.exists():
        obj = qs.first()
        if request.method == 'DELETE':
            data.get("id_") or {}
            qs = Blog.objects.filter(id= id)
            if not qs.exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
            item= qs.first()
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


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
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blog_like_list(request, blog_id, *args, **kwargs):
    """
    LIST OF REQUEST ON GROUP ASSOCIATED TO GROUP ID 
    """
    if request.method == 'GET':
        item = BlogLikes.objects.filter(blog= blog_id).order_by('-created')
        serializer = BlogLikesSerializer(item, many=True)
        return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def items_delete(request, tweet_id,  *args, **kwargs):
    """
    THIS DELETE IF THE USERS OWNS THE POST
    """
    qs = Blog.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    qs= Blog.objects.filter(user=request.user)
    if qs.exists():
        obj = qs.first()
        if request.method == 'DELETE':
            obj.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)

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
            elif action == "report":
                obj.reports.add(request.user)
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
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_list(request, blog_id, *args, **kwargs):
    """
    TO RETURN COMMENT BASED ON THE comment reference
    """
    try:
        item = Comment.objects.filter(blog= blog_id).order_by('-created')
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = CommentSerializer(item, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_details(request, comment_id, *args, **kwargs):
    """
    TO RETURN COMMENT BASED ON THE comment reference
    """

    if request.method == 'GET':
        qs= Comment.objects.filter(id=comment_id)
        if not qs.exists():
            return Response(status= status.HTTP_404_NOT_FOUND)
        item= qs.first()
        serializer = CommentSerializer(item)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_like_list(request, comment_id, *args, **kwargs):
    """
    LIST OF REQUEST ON GROUP ASSOCIATED TO GROUP ID 
    """
    if request.method == 'GET':
        item = CommentLikes.objects.filter(blog= comment_id).order_by('-created')
        serializer = CommentLikesSerializer(item, many=True)
        return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_id,  *args, **kwargs):
    """
    THIS DELETE IF THE USERS OWNS THE COMMENT
    """
    qs = Comment.objects.filter(user=request.user)
    if not qs.exists():
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    obj = qs.first()
    if request.method == 'DELETE':
        try:
            item = Comment.objects.get(id= comment_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)



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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subcomment_list(request, comment_id, *args, **kwargs):
    """
    TO RETURN COMMENT BASED ON THE comment reference
    """

    if request.method == 'GET':
        qs = SubComment.objects.filter(blog= comment_id).order_by('-created')
        serializer = SubCommentSerializer(qs, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subcomment_details(request, subcomment_id, *args, **kwargs):
    """
    TO RETURN COMMENT BASED ON THE comment reference
    """

    if request.method == 'GET':
        qs = SubComment.objects.filter(id=subcomment_id)
        if not qs.exists():
            return Response(status= status.HTTP_404_NOT_FOUND)
        item= qs.first()
        print(item)
        serializer = SubCommentSerializer(item)
        print(serializer)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subcomment_like_list(request, subcomment_id, *args, **kwargs):
    """
    LIST OF REQUEST ON GROUP ASSOCIATED TO GROUP ID 
    """
    if request.method == 'GET':
        item = SubCommentLikes.objects.filter(blog= subcomment_id).order_by('-created')
        serializer = SubCommentLikesSerializer(item, many=True)
        return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def subcomment_delete(request, subcomment_id,  *args, **kwargs):
    """
    THIS DELETE IF THE USERS OWNS THE COMMENT
    """
    
    qs = SubComment.objects.filter(id=subcomment_id)
    if not qs.exists():
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    qs = SubComment.objects.filter(user=request.user)
    if qs.exists():
        obj = qs.first()
        if request.method == 'DELETE':
            obj.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)

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

