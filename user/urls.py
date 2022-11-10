from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('profile', views.profile),
    path('profile/<str:username>', views.profile, name="profile_user"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
]