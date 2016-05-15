from rest_framework import serializers
from models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class GenreSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Genre

class GenreSerializerCompact(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('genre_name', )


class MusicTrackSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    user = UserSerializer()
    class Meta:
        model = MusicTrack
        # fields=('user','music_title','music_track','artist_name','ratings','genre')


class MusicTrackSerializerCompact(serializers.ModelSerializer):
    genre = GenreSerializerCompact()

    class Meta:
        model = MusicTrack
        fields = ('music_title', 'artist_name', 'ratings', 'genre')
