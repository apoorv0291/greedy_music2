from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from models import *
from serializers import *
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.db.models import Q
from itertools import chain
from django.core import serializers
from greedy_music import utils
# Create your views here.

@csrf_exempt
def search_tracks(request):

    data = request.POST
    keyword = data.get('search_keyword')
    if keyword is None or keyword == '':
        message = "Keyword Cannot be left blank"
        data = {"success": False, "message": message}
        # data = json.dumps(data)
        # return HttpResponse(data, content_type="application/json")
    else:
        keyword = keyword.strip().lower()
        try:
            tracks = MusicTrack.objects.filter(music_title__icontains=keyword)
            track2 = MusicTrack.objects.filter(genre__genre_name__icontains=keyword)
            tracks = list(chain(tracks, track2))
            search_result_html = render_to_string("search_result.html", {"tracks": tracks})
            data = {"success": True, "message": "Tracks Searched", "tracks_html": search_result_html }
            # return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            print "Exception", e
            return HttpResponse(data, content_type="application/json")
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json")


#viewing all genres and adding a new genre
@csrf_exempt
def view_all_create_genre(request):

    user = request.user
    if request.method == 'GET':
        genres = Genre.objects.all()
        paginator = Paginator(genres, 5)  # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            genre_paginated = paginator.page(page)
        except PageNotAnInteger:
            genre_paginated = paginator.page(1)
        except EmptyPage:
            genre_paginated = paginator.page(paginator.num_pages)
        is_authenticated = user.is_authenticated()
        return render_to_response("genre.html", {"genres": genre_paginated, "curr_user": user, })
    elif request.method == 'POST':
        if user.is_authenticated():
            data = request.POST
            genre_id, genre_name = utils.data_from_post_genre(data)
            errors = []
            is_valid_genre, errors = utils.is_genre_details_valid(genre_name=genre_name)
            if is_valid_genre == 1:
                genre_name = genre_name.lower()
                try:
                    genre = Genre(genre_name=genre_name, user=user)
                    genre.save()
                    message = "Genre created and saved."
                    data = {"success": True, "message": message}
                except Exception, e:
                    print "Exception", e
                    message = "Genre already exists."
                    data = {"success": False, "message": message}

            else:
                data = {"success": False, "message": errors[0]}

        else:
            data = {"success": False, "message": "User is not authenticated"}
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
# for genre details and edit genre
def genre_details_edit(request, genre_id):

    if genre_id:
        genre_id = int(genre_id)
    user = request.user
    if request.method == 'GET':
        length = 0
        try:
            genre = Genre.objects.get(id=genre_id)
            length = len(genre.music_track.all())
        except Exception, e:
            print "Exception:",  e
            genre = None
        return render_to_response("genre_details.html", {"genre": genre, "length": length,  "curr_user": user})

    elif request.method == 'POST':

        if user.is_authenticated():
            data = request.POST
            genre_id, genre_name = utils.data_from_post_genre(data)
            errors = []
            is_valid_genre, errors = utils.is_genre_details_valid(genre_id=genre_id, genre_name=genre_name)
            if is_valid_genre == 1:
                genre_name = genre_name.strip().lower()
                try:
                    genre = Genre.objects.get(id=int(genre_id))
                    genre.genre_name = genre_name
                    genre.save()
                    message = "Genre renamed and saved."
                    data = {"success": True, "message": message}
                except Exception, e:
                    print "Exception", e
                    message = "Genre with this name already exists."
                    data = {"success": False, "message": message}
            else:
                    data = {"success": False, "message": errors[0]}
        else:
            data = {"success": False, "message": "User is not authenticated"}
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json")




@csrf_exempt
# for viewing all tracks and adding new tracks
def view_all_create_music_tracks(request):
    user = request.user
    if request.method == 'GET':
        music_tracks = MusicTrack.objects.all()
        paginator = Paginator(music_tracks, 5)
        page = request.GET.get('page')
        try:
            music_tracks_paginated = paginator.page(page)
        except PageNotAnInteger:
            music_tracks_paginated = paginator.page(1)
        except EmptyPage:
            music_tracks_paginated = paginator.page(paginator.num_pages)

        genres = Genre.objects.all()
        is_authenticated = user.is_authenticated()
        return render_to_response("track.html", {"tracks": music_tracks_paginated, "genres": genres, "curr_user": user})

    elif request.method == 'POST':
        if user.is_authenticated():
            data = request.POST
            track_id, music_title, artist_name, ratings, genres = utils.data_from_post_music_track(data)
            errors = []
            is_valid_track, errors = utils.is_track_details_valid(music_title=music_title, ratings=ratings,
                                          artist_name=artist_name, genres=genres)
            if is_valid_track == 1:
                music_title = music_title.lower()
                artist_name = artist_name.lower()
                ratings = int(ratings)
                try:
                     track = MusicTrack(user=user, music_title=music_title, artist_name=artist_name,
                                           ratings=ratings,)
                     track.save()
                     message = "Track saved without genre."
                     data = {"success": True, "message": message}
                     try:
                            for genre in genres:
                                genre = Genre.objects.get(id=int(genre))
                                track.genre.add(genre)
                            track.save()
                            message = "Track saved with  genres"
                            data = {"success": True, "message": message}

                     except Exception, e:
                            print "Exception", e
                            data = {"success": False, "message": "Error in adding genres to track"}

                except Exception, e:
                    print "Exception:", e
                    data = {"success": False, "message": "Genre Already exists"}
            else:
                data = {"success": False, "message": errors[0]}
        else:
            data = {"success": False, "message": "User is not authenticated"}
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
#for editing track and viewing specific  track
def track_details_edit(request, track_id):
    print "in track_details"
    track_id = int(track_id)
    user = request.user
    if request.method == 'GET':
        try:
            track = MusicTrack.objects.get(id=track_id)
        except Exception,e:
            print"Exception:",  e
            track = None
        return render_to_response("track_details.html", {"track": track,  "curr_user": user})

    elif request.method == 'POST':
        if user.is_authenticated():
            data = request.POST
            track_id, music_title, artist_name, ratings, genres = utils.data_from_post_music_track(data)
            errors = []
            is_valid_track, errors = utils.is_track_details_valid(music_title=music_title, ratings=ratings,
                                         track_id=track_id, artist_name=artist_name, genres=genres)
            # print "is_valid_track",is_valid_track
            if is_valid_track == 1:
                music_title = music_title.lower()
                artist_name = artist_name.lower()
                ratings = float(ratings)
                track = MusicTrack.objects.get(id=int(track_id))
                try:
                    track.genre.clear()
                    try:
                        for genre in genres:
                            genre = Genre.objects.get(id=int(genre))
                            track.genre.add(genre)
                        track.save()
                        message = "Genres Updated"
                        data = {"success": True, "message": message}
                    except Exception, e:
                        print e
                        message = "Track updated without  genres"
                        data = {"success": False, "message": message}
                    track.ratings = ratings
                    track.save()
                    track.music_title = music_title
                    track.artist_name = artist_name
                    track.save()
                    message = "Track updated with  genres."
                    data = {"success": True, "message": message}
                except Exception, e:
                    print "Exception", e
                    message = "Track and Artist Already Exists."
                    data = {"success": True, "message": message}
            else:
                data = {"success": False, "message": errors[0]}

        else:
            data = {"success": False, "message": "User is not authenticated"}

    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json")







@csrf_exempt
def register_user(request):

    data = request.POST
    email = str(data['email']).lower()
    first_name = data['user_name']
    last_name = data['user_name']
    password = data['password_su']
    try:
        user = User.objects.get(username = email)
        message = "User Already Registered"
    except Exception, e:
        print "Exception:", e
        user = User(username=email, first_name=first_name, last_name=last_name, email=email )
        user.set_password(password)
        user.save()
        message = "User Registered"

    user.backend = "django.contrib.auth.backends.ModelBackend"
    login(request, user)
    data =json.dumps({"success": True, "message": message})
    return HttpResponse(data, content_type="application/json")

@csrf_exempt
def login_user(request):

    data = request.POST
    username = str(data['email_si']).lower()
    password = data['password_si']
    user = authenticate(username=username, password=password)
    if user is None:
        message = "Invalid Credentials"
        data =json.dumps({"success": False, "message": message})
    else:
        message = "User Looged in"
        data =json.dumps({"success": True, "message": message})
        login(request, user)
    return HttpResponse(data, content_type="application/json")

@csrf_exempt
def logout_user(request):

    logout(request)
    return redirect('/greedymusic/tracks')
