# In urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_recommendation_view, name='movie_recommendation_view'),
    path('auth/', views.auth_view, name='auth_view'),
    path('mark_watched/<int:movie_id>/', views.mark_movie_watched, name='mark_watched'),
]