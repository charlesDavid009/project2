from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save 

# Create your models here.

USER = get_user_model()


class Profile(models.Model):
    """
    This is the models for USER PROFILES
    """
    user = models.OneToOneField(USER, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=False, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=False, null=True)
    bio = models.TextField(blank=True, null=True)
    picture = models.ImageField(blank =True, null = True)
    dob = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=False, null=True)
    contact = models.IntegerField(blank=True, null=True)
    nationality = models.CharField(max_length=250, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    followers = models.ManyToManyField(USER, related_name="following", blank=True, through="Follow")

    def user_did_save(sender, instance, created, *args, **kwargs):
        if created:
            Profile.objects.get_or_created(user=instance)

    post_save.connect(user_did_save, sender=USER)

class Follow(models.Model):
    usernames = models.ForeignKey(USER, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user
