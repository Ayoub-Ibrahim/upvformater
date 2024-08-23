from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('multichoice/', views.multichoice, name='multichoice'),
    path('numeric/', views.numerical, name='numeric'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout' ),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('help/', views.help, name='help'),
    path('about/', views.about, name='about'),
]

