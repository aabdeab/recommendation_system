from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


from .models import Movie

def index(request) :
    return HttpResponse("Hello world , success !!!")

# Create your views here.
def movie_recommendation_view(request):
    if request.method == 'GET' :
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context =generate_movies()
            return JsonResponse(context)
        
        context =generate_movies_context()
        return render(request ,'index.html',context)
   
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
# Method to calculate Jaccard Similarity
def jaccard_similarity(list1: list, list2: list) -> float:
    s1 = set(list1)
    s2 = set(list2)
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))
# Calculate the similarity between two movies
def similarity_between_movies(movie1: Movie, movie2: Movie) -> float:
    #if check_valid_genres(movie1.genres) and check_valid_genres(movie2.genres):
        m1_generes = movie1.genres.split()
        m2_generes = movie2.genres.split()
        return jaccard_similarity(m1_generes, m2_generes)
    #else:
        return 0

