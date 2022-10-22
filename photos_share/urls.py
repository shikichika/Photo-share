from django.urls import path

from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),

    path('photo_add/', views.photo_add, name='photo_add'),
    path('photo_detail/<str:pk>/', views.photo_detail, name='photo_detail'),
    path('photo_update/<str:pk>/', views.photo_update, name='photo_update'),
    path('photo_delete/<str:pk>/', views.photo_delete, name='photo_delete'),

    path('categories_list/', views.categories_list, name='categories_list'),
    path('category_update/<str:pk>/', views.category_update, name='category_update'),

    path('gallery_login/', views.gallery_login, name = 'gallery_login'),
    path('gallery_logout/', views.gallery_logout, name='gallery_logout')

]