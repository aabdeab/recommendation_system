from django.urls import path   
from . import views 
 
urlpatterns  = [
    path("",views.index,name="index"),
    path("recommendation/", views.movie_recommendation_view, name="recommendation"),
]