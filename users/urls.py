from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_home, name = 'user_home'),

    path('gallery_detail/<slug:slug>/', views.gallery_detail, name = 'gallery_detail'),
    path('gallery_create/', views.gallery_create, name='gallery_create'),
    path('gallery_update/<slug:slug>/', views.gallery_update, name='gallery_update'),
    path('gallery_delete/<slug:slug>/', views.gallery_delete, name = 'gallery_delete'),
    path('gallery_into/<slug:slug>/', views.gallery_into, name = 'gallery_into'),
    

    path('register/', views.register, name = 'user_register'),
    path('login/', views.user_login, name = 'user_login'),
    path('logout/', views.user_logout, name = 'user_logout'),

    path('user_detail/', views.user_detail, name='user_detail'),
    path('user_update/', views.user_update, name='user_update'),
    path('user_update_username/', views.user_update_username, name='user_update_username'),
    path('user_delete_form/', views.user_delete_form, name='user_delete_form'),
    path('user_delete/', views.user_delete, name='user_delete'),


]