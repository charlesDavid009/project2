from django.urls import path, include
from groups import views

urlpatterns = [
    path('Group/',  views.group_list),
    path('Group/create', views.create_group),
    path('Group/action', views.group_actions),
    path('Group/<int:pk>/details',  views.group_list),
    path('Group/<int:pk>/delete', views.group_delete),

    path('Group/blog',  views.create_blog),
    path('Group/<int:id>/blog_list/', views.blog_list),
    path('Group/<int:id>/blog_details/', views.blog_details),
    path('Group/<int:pk>/blog_delete/', views.blog_delete),
    path('Group/blog_actions', views.blog_actions),

    path('Group/message',  views.message),
    path('Group/<int:id>/message_list/', views.message_list),
    path('Group/<int:pk>/message_details/', views.message_details),
    path('Group/message_actions', views.message_actions),

    path('Group/comment',  views.comment),
    path('Group/<int:id>/comment_list/', views.comment_list),
    path('Group/<int:id>/comment_details/', views.comment_details),
    path('Group/<int:pk>/comment_delete/', views.comment_delete),
    path('Group/comment_actions', views.comment_actions),
]

