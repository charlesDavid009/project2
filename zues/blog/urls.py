from django.urls import path, include
from blog import views

urlpatterns = [
    path('Blog/',  views.items_list),
    path('Blog/feeds',  views.blog_feeds),
    path('Blog/user',  views.blog_user_list),
    path('Blog/create', views.create_blog),
    path('Blog/action', views.actions),
    path('Blog/<int:pk>/details',  views.items_details),
    path('Blog/<str:tweet_id>/delete', views.items_delete),
    path('Blog/<str:blog_id>/blog_like_list/', views.blog_like_list),

    path('Blog/comment',  views.comment),
    path('Blog/comment_action', views.comment_actions),
    path('Blog/<str:blog_id>/comment_list/', views.comment_list),
    path('Blog/<str:comment_id>/comment_details/', views.comment_details),
    path('Blog/<str:comment_id>/comment_like_list/', views.comment_like_list),
    path('Blog/<str:comment_id>/comment_delete/', views.comment_delete),

    path('Blog/subcomment/', views.subcomment),
    path('Blog/subcomment_actions', views.subcomment_actions),
    path('Blog/<str:comment_id>/subcomment_list/', views.subcomment_list),
    path('Blog/<str:subcomment_id>/subcomment_details/', views.subcomment_details),
    path('Blog/<str:subcomment_id>/subcomment_delete/', views.subcomment_delete),
    path('Blog/<str:subcomment_id>/subcomment_like_list/',views.subcomment_like_list),

]
