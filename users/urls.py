from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_home, name = 'user_home'),

    path('gallery_detail/<slug:slug>/', views.gallery_detail, name = 'gallery_detail'),
    path('gallery_create/', views.gallery_create, name='gallery_create'),
    path('gallery_update/<slug:slug>/', views.gallery_update, name='gallery_update'),
    path('gallery_delete/<slug:slug>/', views.gallery_delete, name = 'gallery_delete'),

    path('register/', views.register, name = 'user_register'),
    path('login/', views.user_login, name = 'user_login'),
    path('logout/', views.user_logout, name = 'user_logout')

]