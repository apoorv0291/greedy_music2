from django.db import models
from django.contrib.auth.models import User
from time import gmtime, strftime
# Create your models here.

class Genre(models.Model):

    genre_name = models.CharField(max_length=50, unique=True, null=False)
    user = models.ForeignKey(User, null=True, blank=True,  related_name="user_genre")

    class Meta:
        verbose_name_plural = 'Genres'
        ordering = ['genre_name']

    def __unicode__(self):
        return self.genre_name


def get_track_url(instance, filename):
    time_stamp = strftime("%Y_%m_%d_%H_%M_%S/", gmtime())
    url = instance.user.username + '/' + time_stamp + "/" + filename + "/"
    print "URL for file is->", url
    return url



class MusicTrack(models.Model):

    user = models.ForeignKey(User, null=False, related_name="user_music_track")
    music_title = models.CharField(max_length=100, null=False )
    music_track = models.FileField(upload_to=get_track_url)
    artist_name = models.CharField(max_length=100 , null=False)
    ratings = models.DecimalField(max_digits=2, decimal_places=1, null=False)
    genre = models.ManyToManyField(Genre, related_name="music_track")

    class Meta:
        verbose_name_plural = 'MusicTracks'
        ordering = ['artist_name', 'music_track']
        unique_together = ('music_title', 'artist_name')

    def __unicode__(self):
        return self.music_title + "--Artist is " + self.artist_name



