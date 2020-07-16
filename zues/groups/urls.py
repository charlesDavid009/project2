from django.urls import path, include
from groups import views

urlpatterns = [
    path('Group/',  views.group_list),
    path('Group/create', views.create_group),
    path('Group/action', views.group_actions),
    path('Group/admin_action', views.group_admins_actions),
    path('Group/owner_action', views.group_owner_actions),
    path('Group/<int:pk>/details',  views.group_list),
    path('Group/<int:id>/requests',  views.group_request_view),
    path('Group/<int:id>/follow',  views.group_follow_list),
    path('Group/<int:id>/users',  views.group_users_list),
    path('Group/<int:pk>/delete', views.group_delete),

    path('Group/blog',  views.create_blog),
    path('Group/<int:id>/blog_list/', views.blog_list),
    path('Group/<int:id>/blog_details/', views.blog_details),
    path('Group/<int:pk>/blog_delete/', views.blog_delete),
    path('Group/blog_actions', views.blog_actions),
    path('Group/<int:id>/likes/', views.blog_like_list),
    path('Group/<int:id>/view/', views.blog_report_view),
    path('Group/<int:id>/reports/', views.blog_report_users),
    path('Group/<int:id>/report_actions/', views.report_actions),

    path('Group/message',  views.message),
    path('Group/<int:id>/message_list/', views.message_list),
    path('Group/<int:pk>/message_details/', views.message_details),
    path('Group/message_actions', views.message_actions),
    path('Group/<int:id>/message_likes/', views.message_likes_list),

    path('Group/comment',  views.comment),
    path('Group/<int:id>/comment_list/', views.comment_list),
    path('Group/<int:id>/comment_details/', views.comment_details),
    path('Group/<int:pk>/comment_delete/', views.comment_delete),
    path('Group/comment_actions', views.comment_actions),
    path('Group/<int:id>/comments_likes/', views.comment_likes_list), 
]

