from django.contrib import admin
from .models import (
    Group,
    Uses,
    Follows,
    GroupLikes,
    MyBlog,
    MyBlogLikes,
    MyComment,
    CommentsLikes,
    Message,
    MessageLikes
)

# Register your models here.


class MessageLikesAdmin(admin.TabularInline):
    model = MessageLikes


class MessageAdmin(admin.ModelAdmin):
    inlines = [MessageLikesAdmin]
    list_display = ['reference', 'owner']

    search_feild = ['reference']

    class Meta:
        model = Message


class CommentsLikesAdmin(admin.TabularInline):
    model = CommentsLikes


class CommentAdmin(admin.ModelAdmin):
    inlines = [CommentsLikesAdmin]
    list_display = ['reference', 'owners']

    search_feild = ['reference']

    class Meta:
        model = MyComment


class BlogLikesAdmin(admin.TabularInline):
    model = MyBlogLikes


class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogLikesAdmin]
    list_display = ['reference','title', 'created_at', 'owner']

    search_feild = ['reference']

    class Meta:
        model = MyBlog


class FollowsAdmin(admin.TabularInline):
    model = Follows

class UsesAdmin(admin.TabularInline):
    model = Uses


class GroupLikesAdmin(admin.TabularInline):
    model = GroupLikes

class GroupAdmin(admin.ModelAdmin):
    inlines = [FollowsAdmin, UsesAdmin, GroupLikesAdmin]
    list_display = ['group_name', 'created_at', 'owner']

    search_feild = ['group_name']

    class Meta:
        model = Group

admin.site.register(Group, GroupAdmin)
admin.site.register(MyBlog, BlogAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(MyComment, CommentAdmin)

