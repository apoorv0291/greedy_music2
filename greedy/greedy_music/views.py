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




@csrf_exempt
def genre_details(request, genre_id):

    genre_id = int(genre_id)
    user = request.user
    length = 0
    try:
        genre = Genre.objects.get(id=genre_id)
        length = len(genre.music_track.all())
    except Exception, e:
        print "Exception:",  e
        genre = None
    return render_to_response("genre_details.html", {"genre": genre, "length": length,  "curr_user": user})


@csrf_exempt
def track_details(request, track_id):

    track_id = int(track_id)
    user = request.user
    try:
        track = MusicTrack.objects.get(id=track_id)
    except Exception,e:
        print"Exception:",  e
        track = None
    return render_to_response("track_details.html", {"track": track,  "curr_user": user})


@csrf_exempt
def edit_track(request):
    print "in edit_track"
    user = request.user
    if user.is_authenticated():
        data = request.POST
        track_id = data.get("track_id")
        music_title = data.get("music_title")
        artist_name = data.get("artist_name")
        ratings = data.get("ratings")
        genres = data.getlist('genres')
        errors = []
        is_valid_track, errors = utils.is_track_details_valid(music_title=music_title, ratings=ratings,
                                     track_id=track_id, artist_name=artist_name, genres=genres)
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
                # print "Saving artist and title"
                track.save()
                message = "Track updated with  genres."
                # print "message::", message
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
def add_track(request):

    user = request.user
    if user.is_authenticated():
        data = request.POST
        music_track = request.FILES
        music_title = data.get('music_title')
        artist_name = data.get("artist_name")
        ratings = data.get("ratings")
        genres = data.getlist('genres')
        errors = []
        is_valid_track, errors = utils.is_track_details_valid(music_title=music_title, ratings=ratings,
                                      artist_name=artist_name, genres=genres)
        if is_valid_track == 1:
            music_title = music_title.lower()
            artist_name = artist_name.lower()
            ratings = float(ratings)
            try:
                track = MusicTrack.objects.get(artist_name=artist_name, music_title = music_title)
                message = "Track Already Exists"
                data = {"success": False, "message": message}
            except Exception, e:
                print "Exception:", e
                try:
                    track = MusicTrack(user=user, music_title=music_title, artist_name=artist_name,
                                       ratings=ratings, music_track=music_track)
                    track.save()
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


                except Exception,e:
                    print "Exception:", e
                    message = "Track cannot be saved (without genres)"
                    data = {"success": False, "message": message}


        else:
            data = {"success": False, "message": errors[0]}


    else:
        data = {"success": False, "message": "User is not authenticated"}
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def edit_genre(request):

    user = request.user
    if user.is_authenticated():
        data = request.POST
        genre_id = data.get("genre_id")
        genre_name = data.get("genre_name")
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
                print e
                message = "Genre with this name already exists."
                data = {"success": False, "message": message}
        else:
            data = {"success": False, "message": errors[0]}
    else:
        data = {"success": False, "message": "User is not authenticated"}
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def add_genre(request):

    user = request.user
    if user.is_authenticated():
        data = request.POST
        genre_name = data.get("genre_name")
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


def view_all_genre(request):

    user = request.user
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


def view_all_music_tracks(request):

    user = request.user
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
        user = User(username=   email, first_name=first_name, last_name=last_name, email=email )
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
