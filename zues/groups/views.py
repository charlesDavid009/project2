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
    RequestSerializer,
    FollowsSerializer,
    UsesSerializer,
    MyBlogLikesSerializer,
    MessageLikesSerializer,
    CommentLikesSerializer,
    AdminSerializer,
    ReportSerializer,
    ReportListSerializer
)
from .models import (
    Group,
    MyBlog,
    Message,
    MyComment,
    Request, 
    Follows, 
    Uses,
    CommentsLikes,
    MessageLikes,
    MyBlogLikes,
    Admin,
    Reports
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
            obj = serializer.save()
            vs = obj.id
            qs = Group.objects.filter(id= vs)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            objs = qs.first()
            objs.follower.add(request.user)
            objs.users.add(request.user)
            return Response(objs, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)



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

    qs= Group.objects.filter(owner=request.user)
    if qs.exists():
        obj = qs.first()
        if request.method == 'DELETE':
            item.delete()
            return Response(status=status.HTTP_2OO_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


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
            blog_id = data.get("id_")
            action = data.get("action")
            qs = Group.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_401_UNAUTHORIZED)
            obj = qs.first()
            if action == "follow":
                obj.follower.add(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "unfollow":
                obj.follower.remove(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "exit":
                obj.users.remove(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "join":
                obj.request.add(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "invite":
                obj.like.remove(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def group_admins_actions(request, *args, **kwargs):
    """
    IF ACTION PASSED IS VALID RUN ACTIONS API
    ID IS REQUIRED
    ACTIONS = LIKE, UNLIKE, RE_BLOG
    """
    if request.method == 'POST':
        qs = Group.objects.filter(users=request.user)
        if not qs.exists():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        vs = qs.first()
        serializer = ActionBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            request_id = data.get("id_")
            action = data.get("action")
            qs = Group.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_401_UNAUTHORIZED)
            obj = qs.first()
            qs = Group.objects.filter(request=request_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            ms = qs.first()
            if action == "confirm":
                obj.users.add(ms)
                vd = Group.objects.filter(follower=ms)
                if not vs.exists():
                    obj.follower.add(ms)
                    serializer = GroupSerializer(obj)
                    return Response(serializer.data)
                serializer = GroupSerializer(obj)
                return Response(serializer.data) 

            elif action == "reject":
                obj.request.remove(ms)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)

            elif action == "remove":
                obj.users.remove(ms)
                vs = Group.objects.filter(follower=ms)
                if vs.exists():
                    obj.follower.remove(ms)
                    serializer = GroupSerializer(obj)
                    return Response(serializer.data)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def group_request_view(request, id, *args, **kwargs):
    """
    LIST OF REQUEST ON GROUP ASSOCIATED TO GROUP ID 
    """
    qs = Group.objects.filter(admin=request.user)
    if not qs.exists():
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    vs = qs.first()
    if request.method == 'GET':
        item = Request.objects.filter(group= id).order_by('-created_at')
        serializer = RequestSerializer(item, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def group_follow_list(request, id, *args, **kwargs):
    """
    LIST OF REQUEST ON GROUP ASSOCIATED TO GROUP ID 
    """
    qs = Group.objects.filter(admin=request.user)
    if not qs.exists():
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    vs = qs.first()
    if request.method == 'GET':
        item = Follows.objects.filter(groups= id).order_by('-created_at')
        serializer = FollowsSerializer(item, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def group_users_list(request, id, *args, **kwargs):
    """
    LIST OF REQUEST ON GROUP ASSOCIATED TO GROUP ID 
    """
    qs = Group.objects.filter(follower=request.user)
    if not qs.exists():
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    vs = qs.first()
    if request.method == 'GET':
        item = Uses.objects.filter(members= id).order_by('-created_at')
        serializer = AdminSerializer(item, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def group_admin_list(request, id, *args, **kwargs):
    """
    LIST OF REQUEST ON GROUP ASSOCIATED TO GROUP ID 
    """
    qs = Group.objects.filter(follower=request.user)
    if not qs.exists():
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    vs = qs.first()
    if request.method == 'GET':
        item = Admin.objects.filter(container= id).order_by('-created_at')
        serializer = AdminSerializer(item, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def group_owner_actions(request, *args, **kwargs):
    """
    IF ACTION PASSED IS VALID RUN ACTIONS API
    ID IS REQUIRED
    ACTIONS = LIKE, UNLIKE, RE_BLOG
    """
    if request.method == 'POST':
        qs = Group.objects.filter(owner=request.user)
        if not qs.exists():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        vs = qs.first()
        serializer = ActionBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            users_id = data.get("id_")
            action = data.get("action")
            qs = Group.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            qs = Group.objects.filter(users=users_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            ms = qs.first()
            if action == "add":
                obj.admin.add(ms)
                vs = Group.objects.filter(follower=ms)
                if not vs.exists():
                    obj.follower.add(ms)
                    serializer = GroupSerializer(obj)
                    return Response(serializer.data)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)


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
                picture= picture, 
                
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
def blog_like_list(request, id, *args, **kwargs):
    """
    LIST OF REQUEST ON GROUP ASSOCIATED TO GROUP ID 
    """
    qs = Group.objects.filter(follower=request.user)
    if not qs.exists():
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    vs = qs.first()
    if request.method == 'GET':
        item = MyBlogLikes.objects.filter(blog=id).order_by('-created_at')
        serializer = MyBlogLikesSerializer(item, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blog_report_view(request, id, *args, **kwargs):
    """
    LIST OF REQUEST ON GROUP ASSOCIATED TO GROUP ID 
    """
    qs = Group.objects.filter(admin=request.user)
    if not qs.exists():
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    vs = qs.first()
    if request.method == 'GET':
        item = MyBlog.objects.filter(reference= id).order_by('-created_at')
        serializer = ReportSerializer(item, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blog_report_users(request, id, *args, **kwargs):
    """
    LIST OF REQUEST ON GROUP ASSOCIATED TO GROUP ID 
    """
    qs = Group.objects.filter(admin=request.user)
    if not qs.exists():
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    vs = qs.first()
    if request.method == 'GET':
        item = Reports.objects.filter(blog= id).order_by('-created_at')
        serializer = ReportListSerializer(item, many=True)
        return Response(serializer.data)



@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def blog_details(request, pk, *args, **kwargs):
    """
    THIS PRINTS OUT THE DETAILS WHEN CLICKED
    """
    vs = Group.objects.filter(follower=request.user)
    if  vs.exists():
        try:
            item = MyBlog.objects.get(pk=pk)
        except MyBlog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':  
            serializers = BlogSerializer(item)
            return Response(serializers.data)
        
        qs= MyBlog.objects.filter(owner=request.user)
        if qs.exists():
            obj = qs.first()
            if request.method == 'DELETE':
                item.delete()
                return Response(status=status.HTTP_203_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def blog_delete(request, pk, *args, **kwargs):
    """
    THIS DELETE IF THE USERS OWNS THE POST
    """
    if request.method == 'DELETE':
        qs= MyBlog.objects.filter(user__id = request.user)
        if not qs.exists():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        obj = qs.first()
        try:
            item = MyBlog.objects.get(pk=pk)
        except MyBlog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_2OO_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


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
            blog_id = data.get("id_")
            action = data.get("action")
            til = data.get("title")
            add = data.get("add")
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
            elif action == "report":
                obj.report.add(request.user)
                serializer = ReportSerializer(obj)
                return Response(serializer.data)
            elif action == "reblog":
                vs = obj.reference
                new_blog = MyBlog.objects.create(
                    owner=request.user,
                    parent=obj,
                    reference= vs,
                    title= til,
                    content= add
                )
                serializer = BlogSerializer(new_blog)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_actions(request, *args, **kwargs):
    """
    IF ACTION PASSED IS VALID RUN ACTIONS API
    ID IS REQUIRED
    ACTIONS = LIKE, UNLIKE, RE_BLOG
    """
    if request.method == 'POST':
        vs = Group.objects.filter(admin=request.user)
        if not vs.exists():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ActionBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("id_")
            action = data.get("action")
            qs = MyBlog.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "pass":
                obj.report.remove(request.user)
                serializer = RequestSerializer(obj)
                return Response(serializer.data)
            elif action == "remove":
                obj.delete(obj)
                serializer = BlogSerializer(obj)
                return Response(serializer.data)
            

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def message(request, *args, **kwargs):
    """
    ADD MESSAGE TO BLOG
    """
    if request.method == 'POST':
        vs = Group.objects.filter(users=request.user)
        if not vs.exists():
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
                message= content, 
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
        if not vs.exists():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        qs = MyBlog.objects.filter(reference=id).order_by('-created_at')
        serializer = MessageSerializer(qs, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_likes_list(request, id, *args, **kwargs):
    """
    LIST OF REQUEST ON GROUP ASSOCIATED TO GROUP ID 
    """
    qs = Group.objects.filter(follower=request.user)
    if not qs.exists():
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    vs = qs.first()
    if request.method == 'GET':
        item = MessageLikes.objects.filter(post= id).order_by('-created_at')
        serializer = MessageLikesSerializer(item, many=True)
        return Response(serializer.data)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def message_details(request, pk, *args, **kwargs):
    """
    THIS PRINTS OUT THE DETAILS WHEN CLICKED
    """
    vs = Group.objects.filter(follower=request.user)
    if  vs.exists():
        try:
            item = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':  
            serializers = MessageSerializer(item)
            return Response(serializers.data)
        
        qs= Message.objects.filter(owner=request.user)
        if qs.exists():
            obj = qs.first()
            if request.method == 'DELETE':
                item.delete()
                return Response(status=status.HTTP_203_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_403_FORBIDDEN)


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
        if not vs.exists():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ActionBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("id")
            action = data.get("action")
            qs = Message.objects.filter(id=blog_id)
            if not qs.exists():
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
        if not vs.exists():
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
        if not vs.exists():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        qs = MyComment.objects.filter(reference=id).order_by('-created_at')
        serializer = CommentSerializer(qs, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_likes_list(request, id, *args, **kwargs):
    """
    LIST OF REQUEST ON GROUP ASSOCIATED TO GROUP ID 
    """
    qs = Group.objects.filter(follower=request.user)
    if not qs.exists():
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    vs = qs.first()
    if request.method == 'GET':
        item = CommentsLikes.objects.filter(post= id).order_by('-created_at')
        serializer = CommentLikesSerializer(item, many=True)
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
    vs = Group.objects.filter(follower=request.user)
    if vs.exists():
        try:
            item = MyComment.objects.get(pk=pk)
        except MyComment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializers = MyCommentSerializer(item)
            return Response(serializers.data)

        qs = MyComment.objects.filter(owner=request.user)
        if qs.exists():
            obj = qs.first()
            if request.method == 'DELETE':
                item.delete()
                return Response(status=status.HTTP_203_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_403_FORBIDDEN)


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
        if not vs.exists():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)  
        serializer = ActionBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("id")
            action = data.get("action")
            qs = MyComment.objects.filter(id=blog_id)
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
