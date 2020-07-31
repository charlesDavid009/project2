from rest_framework import serializers
from .models import Profile, Follow
from django.conf import settings


ACTIONS = settings.ACTIONS

class ProfileSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Profile
        fields = '__all__'

    def get_followers(self, obj):
        return obj.followers.count()


class CreateProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100 )
    middle_name = serializers.CharField(max_length=100, required= False) 
    last_name = serializers.CharField(max_length=100)
    bio = serializers.CharField(required=False)
    picture = serializers.ImageField(required=False)
    dob = serializers.IntegerField(required=False)
    email = serializers.EmailField()
    contact = serializers.IntegerField(required=False)
    nationality = serializers.CharField(max_length=250)

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.bio = validated_data.get('bio ', instance.bio)
        instance.email = validated_data.get('email ', instance.email)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.nationality = validated_data.get('nationality ', instance.nationality)
        instance.save()
        return instance


class ActionProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if value in ACTIONS:
            return value
        return serializers.ValidationError(status=400)


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'
