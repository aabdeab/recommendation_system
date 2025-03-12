
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


from .models import Movie

def index(request) :
    return HttpResponse("Hello world , success !!!")
def movie_recommendation_view(request):
    if request.method == 'GET' :
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context =generate_movies(request)
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


def generate_movies(request):
    context = {}
    search_term = request.GET.get('search', '').strip().lower()  

    # Récupérer tous les titres et les résumés des films
    all_movies = Movie.objects.all()
    movie_titles = [movie.original_title for movie in all_movies]  # Utilisation de original_title ici
    movie_overviews = [movie.overview for movie in all_movies]

    if search_term:
        # Ajouter le terme de recherche à la liste des titres et résumés
        search_query = [search_term] + movie_overviews

        # Appliquer le TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(search_query)

        # Calculer la similarité cosinus entre le terme de recherche et les résumés des films
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        movie_indices = cosine_sim[0].argsort()[::-1]

        # Convert the QuerySet into a list of movies based on similarity
        movies = [all_movies[int(i)] for i in movie_indices[:30]]
    else:
        # If no search term, use top 30 movies based on vote count
        movies = all_movies.order_by('-vote_count')[:30]

    # Manually convert movie instances to dictionaries
    movie_list = [{'id': movie.id, 'original_title': movie.original_title, 'overview': movie.overview, 'vote_count': movie.vote_count,'poster_path':movie.poster_path} for movie in movies]

    context['movie_list'] = movie_list
    return context


def recommended_movies():
    context=dict()
    return context



