from greedy_music.models import *

def data_from_post_genre(genre):
    genre_name = genre.get('genre_name')
    genre_id = genre.get('genre_id')
    return genre_id, genre_name


def data_from_post_music_track(track):

    track_id = track.get('track_id')
    artist_name = track.get('artist_name')
    music_title = track.get('music_title')
    ratings = track.get('ratings')
    genres = track.getlist('genres')
    return track_id, music_title, artist_name,  ratings, genres


def is_string_none_or_empty(name):
    if name is None or name.strip().lower() == '':
         return True


def is_rating_valid(rating):
    try:
        rating_int = int(rating)
        if rating_int >= 0 and rating_int <= 5:
            return True
        else:
            return False
    except Exception, e:
        print e
        return False


def is_track_details_valid(**track_details):

    track_id = track_details.get("track_id")
    music_title = track_details.get("music_title")
    artist_name = track_details.get("artist_name")
    ratings = track_details.get("ratings")
    genres = track_details.get('genres')
    errors = []
    if track_id:
        if track_id.isdigit():
            try:
                track = MusicTrack.objects.get(id=int(track_id))
            except Exception, e:
                print e
                err_msg = "No Such Track"
                errors.append(err_msg)

        else:
            err_msg = "Track's id should be numeric"
            errors.append(err_msg)

    if is_string_none_or_empty(music_title):
       err_msg = "Track's title is Required"
       errors.append(err_msg)

    if is_string_none_or_empty(artist_name):
        err_msg = "Artist Name is Required"
        errors.append(err_msg)

    if is_rating_valid(ratings) == False:
        err_msg = "Rating is Required"
        errors.append(err_msg)

    if len(genres) == 0:
        err_msg = "At least one genre is required"
        errors.append(err_msg)

    is_valid = False
    if len(errors) == 0:
        is_valid = True
    return is_valid, errors


def is_genre_details_valid(**genre_details):

    genre_id = genre_details.get("genre_id")
    genre_name = genre_details.get("genre_name")
    errors = []
    if genre_id:
        if genre_id.isdigit():
            try:
                track = Genre.objects.get(id=int(genre_id))
            except Exception, e:
                print e
                err_msg = "No Such Genre"
                errors.append(err_msg)

        else:
            err_msg = "Genre's id should be numeric"
            errors.append(err_msg)

    if is_string_none_or_empty(genre_name):
       err_msg = "Genre name is Required"
       errors.append(err_msg)

    is_valid = False
    if len(errors) == 0:
        is_valid = True
    return is_valid, errors
