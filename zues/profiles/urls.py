from django.urls import path, include
from profiles import views

urlpatterns = [
    path('Profile/',  views.user_profile),
    path('Profile/create', views.create_profile),
    path('Profile/action', views.actions),
    path('Profile/<int:id>/',  views.get_user),
    path('Profile/followers',  views.user_followers),
    path('Profile/following',  views.user_following),
]
