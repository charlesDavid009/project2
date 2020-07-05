from rest_framework import serializers
from .models import Blog, Comment, SubComment
from django.conf import settings

ACTIONS = settings.ACTIONS


class CreateBlogSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    content = serializers.CharField()
    picture = serializers.ImageField(required = False)
    user_id = serializers.IntegerField(required=True)
    created = serializers.DateTimeField(read_only=True)

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
    parent = CreateBlogSerializer(read_only= True)

    class Meta:
        model = Blog
        fields = "__all__"

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        return obj.comments.count()

    def get_content(self, obj):
        content = obj.content
        if obj.is_reblog:
            content= obj.parent.content
            return content


class CreateCommentSerializer(serializers.Serializer):
    blog_id = serializers.IntegerField(required=True)
    text = serializers.CharField(required=True, max_length=9000)

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.blog_id = validated_data.get('blog_id', instance.blog_id)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField(read_only=True)
    comment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def get_like(self, obj):
        return obj.like.count()

    def get_comment(self, obj):
        return obj.comment.count()


class CreateSubCommentSerializer(serializers.Serializer):
    blog_id = serializers.IntegerField(required=True)
    text = serializers.CharField(required=True, max_length=9000)

    def create(self, validated_data):
        return SubComment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.blog_id = validated_data.get('blog_id', instance.blog_id)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance



class SubCommentSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SubComment
        fields = '__all__'

    def get_like(self, obj):
        return obj.like.count()


class ActionBlogSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    add = serializers.CharField(required=False, allow_blank=True)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in ACTIONS:
            raise serializers.ValidationError(status=400)
        return value
