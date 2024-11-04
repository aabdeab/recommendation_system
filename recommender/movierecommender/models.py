from django.db import models

class Movie(models.Model):
    id = models.AutoField(primary_key=True) 
    imdb_id = models.TextField(blank=True, null=True, unique=True)
    genres = models.TextField(blank=True, null=True)
    original_language = models.TextField(blank=True, null=True)
    release_date = models.IntegerField(blank=True, null=True)  # Modifié en DateField
    original_title = models.TextField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    vote_count = models.IntegerField(blank=True, null=True)
    poster_path = models.TextField(blank=True, null=True)
    watched = models.BooleanField(default=False)  
    recommended = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'movie'
