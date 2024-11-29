
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


from .models import Movie

def index(request) :
    return HttpResponse("Hello world , success !!!")


def movie_recommendation_view(request):
    if request.method == 'GET' :
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context =generate_movies()
            return JsonResponse(context)
        
        context =generate_movies_context()
        return render(request ,'index.html',context)
def auth_view(request):
    if request.method =='GET' :
        return render(request,'auth.html')
    
   
def generate_movies_context():  
    context = {}
    
    recommended_count = Movie.objects.filter(
        recommended=True
    ).count()
    
    if recommended_count == 0:
        movies = Movie.objects.filter(
            watched=False
        ).order_by('-vote_count')[:30]
    else:
        movies = Movie.objects.filter(
            watched=False
        ).filter(
            recommended=True
        ).order_by('-vote_count')[:30]
        movies = list(movies.values())
        context['movie_list'] = movies
    return context

def generate_movies():
    context ={}
    movies =list(((Movie.objects.all()).order_by('-vote_count')).values())
    context['movie_list']=movies
    return context

def recommended_movies():
    context=dict()
    return context




