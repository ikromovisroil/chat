from django.urls import path
from .views import *

urlpatterns = [
    path('chat2/<int:id>', chat2, name='chat2'),
    path('chat/<int:id>', chat, name='chat'),
    path('profil', profil, name='profil'),
    path('main', main, name='main'),
    path('main2', main2, name='main2'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('', login, name='login'),

]
