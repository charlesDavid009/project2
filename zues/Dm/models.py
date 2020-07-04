from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings

USER = get_user_model()

# Create your models here.


class Blog(models.Model):
    """
    API FOR USER TO CREATE THEIR OWN BLOG POST
    """
    #parent = models.ForeignKey('self', on_delete = models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=True)
    content = models.CharField(max_length=8000, blank=False, null=True)
    picture = models.ImageField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.ManyToManyField(
        User, related_name='Blog_comments', blank=True, through='Comment')
    likes = models.ManyToManyField(
        User, related_name='Blog_likes', blank=True, through='BlogLikes')
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class BlogLikes(models.Model):
    """
    GETS THE TIME LIKES HAPPENED 
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class Comment(models.Model):
    """
    MODELS FOR COMMENTS 
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    text = models.TextField()
    like = models.ManyToManyField(
        USER, related_name='Commnets_likes', through="CommentLikes")
    comment = models.ManyToManyField(USER, related_name='Commnets_count')

    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class CommentLikes(models.Model):
    """
    GETS THE TIME LIKES HAPPENED 
    """
    blog = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class SubComment(models.Model):
    """
    MODELS FOR SUB COMMENTS  
    """
    blog = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    text = models.TextField()
    like = models.ManyToManyField(
        USER, related_name='SubCommnets_likes', through="SubCommentLikes")
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class SubCommentLikes(models.Model):
    """
    GETS THE TIME LIKES HAPPENED 
    """
    blog = models.ForeignKey(SubComment, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user
