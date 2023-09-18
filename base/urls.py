from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.home, name='home'),
    path('user/<str:pk>', views.user_profile, name='user_profile'),

    path('room/', views.room, name='room'),
    path('room/<int:pk>', views.room, name='room'),
    path('create-room/', views.create_room, name='create_room'),
    path('update-room/<int:pk>', views.update_room, name='update_room'),
    path('delete-room/<int:pk>', views.delete_room, name='delete_room'),
    path('delete-message/<int:pk>', views.delete_message, name='delete_message'),
]
