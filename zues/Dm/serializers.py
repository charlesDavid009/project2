from rest_framework import serializers
from .models import Blog, Comment, SubComment
from django.conf import settings

ACTIONS = settings.ACTIONS

class CreateBlogSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length= 200)
    content = serializers.CharField(max_length= 9000)
    #picture = serializers.ImageField(allow_blank = True, required = False)
    user_id = serializers.IntegerField(required = True)
    created = serializers.DateTimeField(read_only= True)
        
    def create(self, validated_data):
        return Blog.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance



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

class CreateCommentSerializer(serializers.Serializer):
    blog_id = serializers.IntegerField(required= True)
    user_id = serializers.IntegerField(required = True)
    text = serializers.CharField(required= True, max_length= 9000)
        
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.blog_id = validated_data.get('blog_id', instance.blog_id)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


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
        


