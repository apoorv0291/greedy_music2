from django.contrib import admin
from models import *




class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'genre_name', 'user']

class MusicAdmin(admin.ModelAdmin):
    list_display = ['id', 'music_title', 'artist_name', 'user', 'music_track']

# Register your models here.
admin.site.register(Genre, GenreAdmin)
admin.site.register(MusicTrack, MusicAdmin)
