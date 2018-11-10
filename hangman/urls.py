from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('play', views.play, name='play'),
    path('vote', views.vote, name='vote'),
    path('admin', views.admin, name='admin'),
    path('register', views.register, name='register'),
    path('create', views.create, name='create'),
    path('ranking', views.ranking, name='ranking'),
    path('ranking<int:num>', views.ranking, name='ranking')
]
