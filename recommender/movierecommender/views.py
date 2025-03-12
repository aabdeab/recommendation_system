# views.py (Updated)
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.views.decorators.csrf import csrf_exempt
from .models import Movie
import numpy as np
import pandas as pd

def index(request):
    return HttpResponse("Hello world, success!!!")

def movie_recommendation_view(request):
    if request.method == 'GET':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = generate_movies(request)
            return JsonResponse(context)
                
        context = generate_movies_context()
        return render(request, 'index.html', context)

def auth_view(request):
    if request.method == 'GET':
        return render(request, 'auth.html')

def generate_movies_context():
    context = {}
    movies = Movie.objects.filter(watched=False).order_by('-vote_count')[:30]
    context['movie_list'] = list(movies.values())
    return context

def generate_movies(request):
    context = {}
    search_term = request.GET.get('search', '').strip().lower()
    all_movies = Movie.objects.all()
    
    if search_term:
        movie_data = [
            {
                'id': movie.id,
                'text': f"{movie.original_title} {movie.overview} {movie.genres}".lower(),
                'movie': movie
            }
            for movie in all_movies
        ]
        
        vectorizer = TfidfVectorizer(stop_words='english')
        texts = [item['text'] for item in movie_data]
        texts.insert(0, search_term)
        
        if len(texts) > 1:
            tfidf_matrix = vectorizer.fit_transform(texts)
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
            movie_indices = cosine_sim[0].argsort()[-12:][::-1]
            movies = [movie_data[i]['movie'] for i in movie_indices]
        else:
            movies = all_movies.order_by('-vote_count')[:12]
    else:
        movies = all_movies.order_by('-vote_count')[:12]
    
    context['movie_list'] = list(movies.values())
    return context

@csrf_exempt
def mark_movie_watched(request, movie_id):
    if request.method == 'POST':
        try:
            movie = Movie.objects.get(id=movie_id)
            movie.watched = True
            movie.save()
            update_recommendations(movie)
            return JsonResponse({'status': 'success'})
        except Movie.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Movie not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def update_recommendations(watched_movie):
    Movie.objects.all().update(recommended=False)
    watched_movies = Movie.objects.filter(watched=True)
    
    if not watched_movies.exists():
        top_movies = Movie.objects.filter(watched=False).order_by('-vote_average')[:20]
        Movie.objects.filter(id__in=[m.id for m in top_movies]).update(recommended=True)
        return
    
    df = pd.DataFrame(
        [
            {
                'id': movie.id,
                'genres': movie.genres.replace('[', '').replace(']', '').replace("'", '').split(', ') if movie.genres else [],
                'vote_average': movie.vote_average,
                'watched': movie.watched
            }
            for movie in Movie.objects.all()
        ]
    )
    
    watched_genres = set()
    for _, movie in df[df['watched'] == True].iterrows():
        watched_genres.update(movie['genres'])
    
    recommendations = [
        {
            'id': movie['id'],
            'score': 0.7 * (len(set(movie['genres']).intersection(watched_genres)) / max(1, len(watched_genres))) + 0.3 * (movie['vote_average'] / 10)
        }
        for _, movie in df[df['watched'] == False].iterrows()
    ]
    
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    top_movies = [rec['id'] for rec in recommendations[:20]]
    Movie.objects.filter(id__in=top_movies).update(recommended=True)
