from rest_framework import serializers
from .models import Blog, Comment, SubComment
from django.conf import settings

ACTIONS = settings.ACTIONS

class CreateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [ 'title', 'content', 'picture', 'user_id']
        
    def create(self, validated_data):
        return Blog.objects.create(**validated_data)


class BlogSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Blog
        fields = "__all__"
    
    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        return obj.comments.count()

class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['text']
        
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField(read_only=True)
    commnets = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        return obj.comments.count()


class CreateSubCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubComment
        fields = ['text']

    def create(self, validated_data):
        return SubComment.objects.create(**validated_data)


class SubCommentSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SubComment
        fields = '__all__'

    def get_likes(self, obj):
        return obj.likes.count()

class ActionBlogSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    add = serializers.CharField(required= False, allow_blank= True)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in ACTIONS:
            raise serializers.ValidationError(status=400)
        return value
        


