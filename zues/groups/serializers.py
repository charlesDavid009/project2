from rest_framework import serializers
from .models import Group, MyBlog, Message, MyComment
from django.conf import settings

ACTIONS = settings.ACTIONS


class GroupSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    follower = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = '__all__'

    def get_likes(self, obj):
        return obj.likes.count()

    def get_follower(self, obj):
        return obj.follower.count()

    def get_users(self, obj):
        return obj.users.count()


class CreateGroupSerializer(serializers.Serializer):
    group_name = serializers.CharField(max_length = 100)
    description = serializers.CharField(required=False, allow_blank=True)
    picture = serializers.ImageField(required= False)
    owner = serializers.IntegerField()

    def create(self, validated_data):
        return Group.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.group_name = validated_data.get('group_name', instance.group_name)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class CreateBlogSerializer(serializers.Serializer):
    reference = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    picture = serializers.ImageField(required=False)

    def create(self, validated_data):
        return MyBlog.objects.create(**validated_data)

class BlogSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    comment = serializers.SerializerMethodField(read_only=True)
    parent = CreateBlogSerializer(read_only= True)

    class Meta:
        model = MyBlog
        fields = '__all__'

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comment(self, obj):
        return obj.comment.count()
    
    def get_content(self, obj):
        content = obj
        if obj.is_reblog:
            content = obj.parent.content
            return content


class MessageSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField(read_only=True)
    comment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Message
        fields = ["reference", "id", "comment", "like", "created_at"]

    def get_like(self, obj):
        return obj.like.count()

    def get_comment(self, obj):
        return obj.comment.count()



class CreateMessageSerializer(serializers.Serializer):
    reference = serializers.IntegerField()
    message = serializers.CharField()

    def  create(self, validated_data):
        return Message.objects.create(**validated_data)


class ActionBlogSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if value in ACTIONS:
            return value
        return serializers.ValidationError(status =400)


class CommentSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MyComment
        fields = ["reference", "id", "comment", "likes", "created_at"]

    def get_like(self, obj):
        return obj.like.count()



class CreateCommentSerializer(serializers.Serializer):
    reference = serializers.IntegerField()
    comment = serializers.CharField()

    def  create(self, validated_data):
        return MyComment.objects.create(**validated_data)



