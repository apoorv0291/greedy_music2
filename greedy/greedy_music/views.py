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
# Create your views here.

@csrf_exempt
def search_tracks(request):

    data = request.POST
    keyword = data.get('search_keyword')
    if keyword is None or keyword == '':
        message = "Keyword Cannot be left blank"
        data = {"success": False, "message": message}
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")
    else:
        keyword = keyword.strip().lower()
        try:
            tracks = MusicTrack.objects.filter(music_title__icontains=keyword)
            track2 = MusicTrack.objects.filter(genre__genre_name__icontains=keyword)
            tracks = list(chain(tracks, track2))
            search_result_html = render_to_string("search_result.html", {"tracks": tracks})
            data = {"success": True, "message": "Tracks Searched", "tracks_html": search_result_html }
            return HttpResponse(json.dumps(data), content_type="application/json")

        except Exception, e:
            print "Exception", e






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


    user = request.user
    if user.is_authenticated():
        data = request.POST
        track_id = data.get("track_id")
        music_title = data.get("music_title")
        artist_name = data.get("artist_name")
        ratings = data.get("ratings")
        genres = data.getlist('genres')
        errors = []
        if music_title is None or music_title.strip() == '':
           err_msg = "Track's title is Required"
           errors.append(err_msg)

        if artist_name is None or artist_name.strip() == '':
            err_msg = "Artist Name is Required"
            errors.append(err_msg)

        if ratings is None or ratings.strip() == '':
            err_msg = "Rating is Required"
            errors.append(err_msg)

        if len(genres) == 0:
            err_msg = "At least one genre is required"
            errors.append(err_msg)

        if len(errors) == 0:
            music_title = music_title.lower()
            artist_name = artist_name.lower()
            ratings = float(ratings)
            track = MusicTrack.objects.get(id=int(track_id))
            old_music_title = track.music_title
            old_artist_name = track.artist_name
            #if name and artist are same in editing
            if old_artist_name == artist_name and old_music_title == music_title:
                track.ratings = ratings
                track.save()
                track.genre.clear()
                for genre in genres:
                    genre = Genre.objects.get(id=int(genre))
                    track.genre.add(genre)
                track.save()
                message = "Track updated with  genres"
                data = {"success": True, "message": message}
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
            else:
                try:
                    track = MusicTrack.objects.get(artist_name=artist_name, music_title=music_title)
                    message = "Track and Already Exists"
                    data = {"success": False, "message": message}
                    data = json.dumps(data)
                    return HttpResponse(data, content_type="application/json")

                except Exception, e:
                    print "Exception:", e
                    try:
                        track = MusicTrack.objects.get(id=int(track_id))
                        track.music_title = music_title
                        track.artist_name = artist_name
                        track.ratings = ratings
                        track.save()
                        try:
                            track.genre.clear()
                            for genre in genres:
                                genre = Genre.objects.get(id=int(genre))
                                track.genre.add(genre)
                            track.save()
                            message = "Track updated with  genres"
                            data = {"success": True, "message": message}
                            data = json.dumps(data)
                            return HttpResponse(data, content_type="application/json")

                        except Exception, e:
                            data = {"success": False, "message": "Error in adding genres to track"}
                            data = json.dumps(data)
                            return HttpResponse(data, content_type="application/json")

                    except Exception,e:
                        print "Exception:", e
                        message = "Track cannot be saved (without genres)"
                        data = {"success": False, "message": message}
                        data = json.dumps(data)
                        return HttpResponse(data, content_type="application/json")

        else:
            data = {"success": False, "message": errors[0]}
            data = json.dumps(data)
            return HttpResponse(data, content_type="application/json")

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
        pass
        errors = []
        if music_title is None or music_title.strip() == '':
            err_msg = "Track's title is Required"
            errors.append(err_msg)

        if artist_name is None or artist_name.strip() == '':
            err_msg = "Artist Name is Required"
            errors.append(err_msg)

        if ratings is None or ratings.strip() == '':
            err_msg = "Rating is Required"
            errors.append(err_msg)

        if len(genres) == 0:
            err_msg = "At least one genre is required"
            errors.append(err_msg)

        if len(request.FILES) > 1:
           err_msg = "More than one file not allowed"
           errors.append(err_msg)


        if len(errors) == 0:
            music_title = music_title.lower()
            artist_name = artist_name.lower()
            ratings = float(ratings)
            try:
                track = MusicTrack.objects.get(artist_name=artist_name, music_title = music_title)
                message = "Track Already Exists"
                data = {"success": False, "message": message}
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
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
                        data = json.dumps(data)
                        return HttpResponse(data, content_type="application/json")

                    except Exception, e:
                        print "Exception", e
                        data = {"success": False, "message": "Error in adding genres to track"}
                        data = json.dumps(data)
                        return HttpResponse(data, content_type="application/json")

                except Exception,e:
                    print "Exception:", e
                    message = "Track cannot be saved (without genres)"
                    data = {"success": False, "message": message}
                    data = json.dumps(data)
                    return HttpResponse(data, content_type="application/json")

        else:
            data = {"success": False, "message": errors[0]}
            data = json.dumps(data)
            return HttpResponse(data, content_type="application/json")

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
        if genre_name is None or genre_name.strip() == '':
            err_msg = "Genre Name is Required"
            errors.append(err_msg)

        if len(errors) == 0:
            genre_name = genre_name.strip().lower()
            try:
                genre = Genre.objects.get(genre_name=genre_name)
            except Exception, e:
                print "Exception:", e
                genre = Genre.objects.get(id=int(genre_id))
                genre.genre_name = genre_name
                genre.save()
                message = "Genre renamed and saved."
                data = {"success": True, "message": message}
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
                # redirect("/greedymusic/genre")

        else:
            data = {"success": False, "message": errors[0]}
            data = json.dumps(data)
            return HttpResponse(data, content_type="application/json")

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
        if genre_name is None or genre_name.strip() == '':
            err_msg = "Genre Name is Required"
            errors.append(err_msg)
        if len(errors) == 0:
            genre_name = genre_name.lower()
        try:
                genre = Genre.objects.get(genre_name=genre_name)
        except Exception, e:
                print "Exception", e
                try:
                    genre = Genre(genre_name=genre_name, user = user)
                    genre.save()
                except Exception,e:
                    print "Exception:", e
                    return
                message = "Genre created and saved."
                data = {"success": True, "message": message}
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
                # redirect("/greedymusic/genre")

        else:
            data = {"success": False, "message": errors[0]}
            data = json.dumps(data)
            return HttpResponse(data, content_type="application/json")

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
        return HttpResponse(data, content_type="application/json")
    else:
        message = "User Looged in"
        data =json.dumps({"success": True, "message": message})
        login(request, user)
        return HttpResponse(data, content_type="application/json")

@csrf_exempt
def logout_user(request):

    logout(request)
    return redirect('/greedymusic/tracks')
