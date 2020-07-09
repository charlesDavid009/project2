from django.urls import path, include
from profiles import views

urlpatterns = [
    path('Profile/',  views.user_profile),
    path('Profile/create', views.create_profile),
    path('Profile/action', views.actions),
    path('Profile/<str:username>/profile',  views.view_user),
]
