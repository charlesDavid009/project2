from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from .serializers import (
    GroupSerializer,
    CreateGroupSerializer,
    CreateBlogSerializer,
    BlogSerializer,
    MessageSerializer,
    CreateMessageSerializer,
    ActionBlogSerializer,
    CommentSerializer,
    CreateCommentSerializer,
)
from .models import (
    Group,
    MyBlog,
    Message,
    MyComment
)
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from django.http import Http404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings


ACTIONS = settings.ACTIONS

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request, *args, **kwargs):
    """
    CREATE GROUP API
    """
    if request.method == 'POST':
        serializer = CreateGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def group_list(request, *args, **kwargs):
    """
    list of groups avaliable
    """
    if request.method == 'GET':
        item = Group.objects.all()
        serializer = GroupSerializer(item, many=True)
        return Response(serializer.data)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def group_delete(request, pk, *args, **kwargs):
    """
    THIS DELETE IF THE USERS OWNS THE POST
    """
    try:
        item = Group.objects.get(pk=pk)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GroupSerializer(item)
        return Response(serializer.data)

    if request.method == 'DELETE':
        QS = item.objects.filter(owner=request.user)
        if QS.exists():
            QS.delete()
            return Response(status=status.HTTP_2OO_NO_CONTENT)
        return Response(status=status.HTTP_401_NOT_AUTHORISED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def group_actions(request, *args, **kwargs):
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
            qs = Group.objects.filter(id=blog_id)
            if not qs.exsits():
                return Response({}, status=status.HTTP_401_UNAUTHORIZED)
            obj = qs.first()
            if action == "like":
                obj.likes.add(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "unlike":
                obj.likes.remove(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "follow":
                obj.follower.add(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "unfollow":
                obj.follower.remove(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "add":
                obj.users.add(request.user)
                vs = Group.objects.filter(follower=request.user)
                if not vs.exsits():
                    obj.follower.add(request.user)
                    serializer = GroupSerializer(obj)
                    return Response(serializer.data)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "remove":
                obj.users.remove(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "exit":
                obj.users.remove(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "join":
                obj.users.send(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "invite":
                obj.like.remove(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_blog(request, *args, **kwargs):
    """
    CREATE GROUP BLOG API
    """

    if request.method == 'POST':
        vs = Group.objects.filter(users=request.user)
        if not vs.exists():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)     
        serializer = CreateBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("reference")
            title = data.get("title")
            content = data.get("content")
            picture = data.get("picture")
            qs = Group.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            my_comment = MyBlog.objects.create(
                owner=request.user,
                reference=obj,
                title=title,
                content= content, 
                picture= picture
            )
            serializer = BlogSerializer(my_comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blog_list(request, id, *args, **kwargs):
    """
    list of blogs in a group
    """
    if request.method == 'GET':
        vs = Group.objects.filter(follower=request.user)
        if not vs.exists():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        qs = MyBlog.objects.filter(reference=id).order_by('-created_at')
        serializer = BlogSerializer(qs, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blog_details(request, pk, *args, **kwargs):
    """
    THIS PRINTS OUT THE DETAILS WHEN CLICKED
    """
    
    try:
        item = MyBlog.objects.get(pk=pk)
    except MyBlog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        vs = Group.objects.filter(follower=request.user)
        if not vs.exists():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        serializers = BlogSerializer(item)
        return Response(serializers.data)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def blog_delete(request, pk, *args, **kwargs):
    """
    THIS DELETE IF THE USERS OWNS THE POST
    """
    try:
        item = MyBlog.objects.get(pk=pk)
    except MyBlog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        QS = item.objects.filter(owner=request.user)
        if QS.exists():
            QS.delete()
            return Response(status=status.HTTP_2OO_NO_CONTENT)
        return Response(status=status.HTTP_401_NOT_AUTHORISED)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def blog_actions(request, *args, **kwargs):
    """
    IF ACTION PASSED IS VALID RUN ACTIONS API
    ID IS REQUIRED
    ACTIONS = LIKE, UNLIKE, RE_BLOG
    """
    if request.method == 'POST':
        vs = Group.objects.filter(users=request.user)
        if not vs.exists():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ActionBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("id")
            action = data.get("action")
            qs = MyBlog.objects.filter(id=blog_id)
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
                new_blog = MyBlog.objects.create(
                    user=request.user,
                    parent=obj,
                )
                serializer = BlogSerializer(new_blog)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def message(request, id, *args, **kwargs):
    """
    ADD MESSAGE TO BLOG
    """
    if request.method == 'POST':
        vs = Group.objects.filter(users=request.user)
        if not vs.exsits():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CreateMessageSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("reference")
            content = data.get("message")
            qs = MyBlog.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            my_comment = Message.objects.create(
                owner=request.user,
                reference=obj,
                content= content, 
            )
            serializer = MessageSerializer(my_comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_list(request, id, *args, **kwargs):
    """
    TO RETURN COMMENT BASED ON THE comment reference
    """

    if request.method == 'GET':
        vs = Group.objects.filter(follower=request.user)
        if not vs.exsits():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        qs = MyBlog.objects.filter(reference=id).order_by('-created_at')
        serializer = MessageSerializer(qs, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_details(request, pk, *args, **kwargs):
    """
    THIS PRINTS OUT THE DETAILS WHEN CLICKED
    """
    try:
        item = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        vs = Group.objects.filter(follower=request.user)
        if not vs.exsits():
            return Response({}, status=status.HTTP_404_NOT_FOUND)  
        serializers = MessageSerializer(item)
        return Response(serializers.data)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def message_delete(request, pk, *args, **kwargs):
    """
    THIS DELETE IF THE USERS OWNS THE POST
    """
    try:
        item = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessageSerializer(item)
        return Response(serializer.data)

    if request.method == 'DELETE':
        QS = item.objects.filter(owner=request.user)
        if QS.exists():
            QS.delete()
            return Response(status=status.HTTP_2OO_NO_CONTENT)
        return Response(status=status.HTTP_401_NOT_AUTHORISED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def message_actions(request, *args, **kwargs):
    """
    IF ACTION PASSED IS VALID RUN ACTIONS API
    ID IS REQUIRED
    ACTIONS = LIKE, UNLIKE, RE_BLOG
    """
    if request.method == 'POST':
        vs = Group.objects.filter(follower=request.user)
        if not vs.exsits():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ActionBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("id")
            action = data.get("action")
            qs = Message.objects.filter(id=blog_id)
            if not qs.exsits():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "like":
                obj.like.add(request.user)
                serializer = MessageSerializer(obj)
                return Response(serializer.data)
            elif action == "unlike":
                obj.like.remove(request.user)
                serializer = MessageSerializer(obj)
                return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment(request, id, *args, **kwargs):
    """
    ADD A SUB COMMENT MESSAGE
    """
    if request.method == 'POST':
        vs = Group.objects.filter(follower=request.user)
        if not vs.exsits():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)  
        serializer = CreateCommentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("reference")
            content = data.get("comment")
            qs = Message.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            my_comment = MyComment.objects.create(
                owner=request.user,
                reference=obj,
                content=content,
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

    if request.method == 'GET':
        vs = Group.objects.filter(follower=request.user)
        if not vs.exsits():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        qs = MyComment.objects.filter(reference=id).order_by('-created_at')
        serializer = CommentSerializer(qs, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_details(request, pk, *args, **kwargs):
    """
    THIS PRINTS OUT THE DETAILS WHEN CLICKED
    """
    try:
        item = MyComment.objects.get(pk=pk)
    except MyComment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        vs = Group.objects.filter(follower=request.user)
        if not vs.exsits():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)  
        serializers = CommentSerializer(item)
        return Response(serializers.data)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, pk, *args, **kwargs):
    """
    THIS DELETE IF THE USERS OWNS THE POST
    """
    try:
        item = MyComment.objects.get(pk=pk)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CommentSerializer(item)
        return Response(serializer.data)

    if request.method == 'DELETE':
        QS = item.objects.filter(owner=request.user)
        if QS.exists():
            QS.delete()
            return Response(status=status.HTTP_2OO_NO_CONTENT)
        return Response(status=status.HTTP_401_NOT_AUTHORISED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_actions(request, *args, **kwargs):
    """
    IF ACTION PASSED IS VALID RUN ACTIONS API
    ID IS REQUIRED
    ACTIONS = LIKE, UNLIKE, RE_BLOG
    """
    if request.method == 'POST':
        vs = Group.objects.filter(follower=request.user)
        if not vs.exsits():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)  
        serializer = ActionBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("id")
            action = data.get("action")
            qs = MyComment.objects.filter(id=blog_id)
            if not qs.exsits():
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
