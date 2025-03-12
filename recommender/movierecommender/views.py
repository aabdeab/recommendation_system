# In views.py
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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
        
    # Get all movie titles and overviews
    all_movies = Movie.objects.all()
    
    if search_term:
        # Create a list of all movie data for processing
        movie_data = []
        for movie in all_movies:
            # Combine title, overview and genres for better matching
            combined_text = f"{movie.original_title} {movie.overview} {movie.genres}".lower()
            movie_data.append({
                'id': movie.id,
                'text': combined_text,
                'movie': movie
            })
            
        # Apply TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        texts = [item['text'] for item in movie_data]
        texts.insert(0, search_term)  # Add search term at the beginning
        
        try:
            tfidf_matrix = vectorizer.fit_transform(texts)
            
            # Calculate cosine similarity
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
            
            # Sort movies by similarity
            movie_indices = cosine_sim[0].argsort()[-12:][::-1]  # Top 12 results
            movies = [movie_data[i]['movie'] for i in movie_indices]
        except Exception as e:
            # Fallback if TF-IDF fails
            movies = all_movies.order_by('-vote_count')[:12]
    else:
        # If no search term, return top rated movies
        movies = all_movies.order_by('-vote_count')[:12]
    
    context['movie_list'] = list(movies.values())
    return context

def mark_movie_watched(request, movie_id):
    """Mark a movie as watched and update recommendations"""
    if request.method == 'POST':
        try:
            movie = Movie.objects.get(id=movie_id)
            movie.watched = True
            movie.save()
            
            # Update recommendations based on this watch
            update_recommendations(movie)
            
            return JsonResponse({'status': 'success'})
        except Movie.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Movie not found'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def update_recommendations(watched_movie):
    """Update movie recommendations based on a newly watched movie"""
    # First, reset all recommended flags
    Movie.objects.all().update(recommended=False)
    
    # Get all movies
    all_movies = Movie.objects.all()
    watched_movies = Movie.objects.filter(watched=True)
    
    if not watched_movies.exists():
        # If no watched movies, recommend top rated
        top_movies = Movie.objects.filter(watched=False).order_by('-vote_average')[:20]
        for movie in top_movies:
            movie.recommended = True
            movie.save()
        return
    
    # Create feature vectors from genres
    movie_data = []
    for movie in all_movies:
        # Convert genres string to list
        genres = movie.genres.replace('[', '').replace(']', '').replace('\'', '').split(', ') if movie.genres else []
        movie_data.append({
            'id': movie.id,
            'genres': genres,
            'vote_average': movie.vote_average,
            'original_language': movie.original_language,
            'watched': movie.watched
        })
    
    # Convert to DataFrame for easier processing
    df = pd.DataFrame(movie_data)
    
    # Get genres of watched movies
    watched_genres = set()
    for _, movie in df[df['watched'] == True].iterrows():
        watched_genres.update(movie['genres'])
    
    # Score unwatched movies based on genre overlap and rating
    recommendations = []
    for _, movie in df[df['watched'] == False].iterrows():
        # Calculate genre overlap
        common_genres = set(movie['genres']).intersection(watched_genres)
        genre_score = len(common_genres) / max(1, len(watched_genres))
        
        # Combined score (70% genre similarity, 30% rating)
        combined_score = 0.7 * genre_score + 0.3 * (movie['vote_average'] / 10)
        
        recommendations.append({
            'id': movie['id'],
            'score': combined_score
        })
    
    # Sort by score and mark top 20 as recommended
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    for rec in recommendations[:20]:
        try:
            movie = Movie.objects.get(id=rec['id'])
            movie.recommended = True
            movie.save()
        except Movie.DoesNotExist:
            continue