from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from models import *
from serializers import *
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,authenticate
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.db.models import Q
from django.core import serializers
# Create your views here.

@csrf_exempt
def search_tracks(request):

    print "@@in search_tracks@@", request.user
    data = request.POST
    print data
    keyword = data.get('search_keyword')
    print "keyword:", keyword
    if keyword is None or keyword == '':
        message = "Keyword Cannot be left blank"
        print message
        data = {"success": False, "message": message}
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")
    else:
        keyword = keyword.strip().lower()
        print "keyword:", keyword
        try:
            tracks = MusicTrack.objects.filter(Q(music_title__icontains=keyword)
                                        | Q(genre__genre_name__icontains=keyword))
            print tracks
            # tracks_json = serializers.serialize('json', tracks, fields=('music_title', 'artist_name', 'ratings' ) )
            tracks_serialzed = MusicTrackSerializer(tracks, many=True)
            tracks_json = JSONRenderer().render(tracks_serialzed.data)
            # print "Track_JSON", tracks_json
            # data = {"success": True, "message": "Tracks Serialized", "tracks_j": tracks_serialzed}
            # return HttpResponse(json.dumps(data), content_type="application/json")
            # return HttpResponse(tracks_json, content_type="application/json")
            print "apoorv"
            search_result_html = render_to_string("search_result.html", {"tracks": tracks})
            data = {"success": True, "message": "Tracks Searched", "tracks_html": search_result_html }
            return HttpResponse(json.dumps(data), content_type="application/json")

        except Exception, e:
            print "@@Excpetion@@", e






@csrf_exempt
def genre_details(request, genre_id):

    print "@@in genre_details@@", request.user
    genre_id = int(genre_id)
    genre = Genre.objects.get(id=genre_id)
    print "Genre is ::", genre_id
    print "track related to genre are  :", genre.music_track.all()
    return render_to_response("genre_details.html", {"genre": genre})


@csrf_exempt
def track_details(request, track_id):

    print "@@in track_details@@", request.user
    track_id = int(track_id)
    track = MusicTrack.objects.get(id=track_id)
    print "track is :", track.genre.all()
    return render_to_response("track_details.html", {"track": track})


@csrf_exempt
def edit_track(request):

    print "@@In Edit track@@"
    user = request.user
    print "user:::", user
    if user.is_authenticated:
        data = request.POST
        track_id = data.get("track_id")
        music_title = data.get("music_title")
        artist_name = data.get("artist_name")
        ratings = data.get("ratings")
        genres = data.getlist('genres')
        print "Genre_names::", genres
        print "music_title::", music_title
        print "artist_name::", artist_name
        print "ratings::", ratings
        errors = []

        if music_title is None or music_title.strip() == '':
            print "Track's title is Required"
            err_msg = "Track's title is Required"
            errors.append(err_msg)

        if artist_name is None or artist_name.strip() == '':
            print "Artist Name is Required"
            err_msg = "Artist Name is Required"
            errors.append(err_msg)

        if ratings is None or ratings.strip() == '':
            print "Ratings is Required"
            err_msg = "Rating is Required"
            errors.append(err_msg)

        if len(genres) == 0:
            print "At least one genre is required"
            err_msg = "At least one genre is required"
            errors.append(err_msg)

        if len(errors) == 0:
            print "@#In len(errors)==@@"
            music_title = music_title.lower()
            artist_name = artist_name.lower()
            ratings = float(ratings)
            print "music_title::", music_title
            print "artist_name::", artist_name
            print "ratings::", ratings
            # print "Genre_name::",genre_name

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
                print "Track updated with  genres"
                message = "Track updated with  genres"
                data = {"success": True, "message": message}
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
            else:
                try:
                    track = MusicTrack.objects.get(artist_name=artist_name, music_title=music_title)
                    print "Track and artist Already Exists"
                    message = "Track and Already Exists"
                    data = {"success": False, "message": message}
                    data = json.dumps(data)
                    return HttpResponse(data, content_type="application/json")

                except Exception, e:
                    print "@@Excpetion@@", e
                    try:
                        track = MusicTrack.objects.get(id=int(track_id))
                        track.music_title = music_title
                        track.artist_name = artist_name
                        track.ratings = ratings
                        track.save()
                        print "Track updated without genres"

                        try:
                            track.genre.clear()
                            for genre in genres:
                                genre = Genre.objects.get(id=int(genre))
                                track.genre.add(genre)
                            track.save()
                            print "Track updated with  genres"
                            message = "Track updated with  genres"
                            data = {"success": True, "message": message}
                            data = json.dumps(data)
                            return HttpResponse(data, content_type="application/json")

                        except Exception, e:
                            print "Exception", e
                            print "Error in adding genres to track"
                            data = {"success": False, "message": "Error in adding genres to track"}
                            data = json.dumps(data)
                            return HttpResponse(data, content_type="application/json")

                    except Exception,e:
                        print "$$$Exception$$", e
                        print "Track cannot be saved (without genres)"
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
    print "@@In add_track@@"
    user = request.user
    print user
    if user.is_authenticated:
        data = request.POST
        music_track = request.FILES
        print "Data::", data
        print "Music_track_File", music_track
        music_title = data.get('music_title')
        artist_name = data.get("artist_name")
        ratings = data.get("ratings")
        genres = data.getlist('genres')
        print "Genre_names::", genres
        print "music_title::", music_title
        print "artist_name::", artist_name
        print "ratings::", ratings
        pass
        errors = []
        if music_title is None or music_title.strip() == '':
            print "Track's title is Required"
            err_msg = "Track's title is Required"
            errors.append(err_msg)

        if artist_name is None or artist_name.strip() == '':
            print "Artist Name is Required"
            err_msg = "Artist Name is Required"
            errors.append(err_msg)

        if ratings is None or ratings.strip() == '':
            print "Ratings is Required"
            err_msg = "Rating is Required"
            errors.append(err_msg)

        if len(genres) == 0:
            print "At least one genre is required"
            err_msg = "At least one genre is required"
            errors.append(err_msg)

        if len(request.FILES) > 1:
            print "More than one file not allowed"
            err_msg = "More than one file not allowed"
            errors.append(err_msg)




        if len(errors) == 0:
            print "@#In len(errors)==@@"
            music_title = music_title.lower()
            artist_name = artist_name.lower()
            ratings = float(ratings)
            print "music_title::", music_title
            print "artist_name::", artist_name
            print "ratings::", ratings
            # print "Genre_name::",genre_name
            try:
                track = MusicTrack.objects.get(artist_name=artist_name, music_title = music_title)
                print "Track Already Exists"
                message = "Track Already Exists"
                data = {"success": False, "message": message}
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
            except Exception, e:
                print "@@Excpetion@@", e
                try:
                    track = MusicTrack(user=user, music_title=music_title, artist_name=artist_name,
                                       ratings=ratings, music_track=music_track)
                    track.save()
                    print "Track saved without  genres"

                    try:
                        for genre in genres:
                            genre = Genre.objects.get(id=int(genre))
                            track.genre.add(genre)
                        track.save()
                        print "Track saved with  genres"
                        message = "Track saved with  genres"
                        data = {"success": True, "message": message}
                        data = json.dumps(data)
                        return HttpResponse(data, content_type="application/json")

                    except Exception, e:
                        print "Exception", e
                        print "Error in adding genres to track"
                        data = {"success": False, "message": "Error in adding genres to track"}
                        data = json.dumps(data)
                        return HttpResponse(data, content_type="application/json")

                except Exception,e:
                    print "$$$Exception$$", e
                    print "Track cannot be saved (without genres)"
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
    print "@@In Edit Genre@@"
    user = request.user
    print "user:::", user
    if user.is_authenticated:
        data = request.POST
        genre_id = data.get("genre_id")
        genre_name = data.get("genre_name")
        errors = []
        if genre_name is None or genre_name.strip() == '':
            print "Genre Name is Required"
            err_msg = "Genre Name is Required"
            errors.append(err_msg)

        if len(errors) == 0:
            genre_name = genre_name.strip().lower()
            try:
                genre = Genre.objects.get(genre_name=genre_name)
                print "Genre by this name already exists"
            except Exception, e:
                print "@@Excpetion@@", e
                genre = Genre.objects.get(id=int(genre_id))
                genre.genre_name = genre_name

                genre.save()
                print "@@genre renamed and saved@@"
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
    print "@@In add_genre@@"
    user = request.user
    print user
    if user.is_authenticated:
        data = request.POST
        print "Data::", data
        genre_name = data.get("genre_name")
        print "Genre_name::", genre_name
        errors = []
        if genre_name is None or genre_name.strip() == '':
            print "Genre Name is Required"
            err_msg = "Genre Name is Required"
            errors.append(err_msg)


        if len(errors) == 0:
            genre_name = genre_name.lower()
            print "Genre_name::",genre_name
            try:
                genre = Genre.objects.get(genre_name=genre_name)
                print "Genre Already Exists"
            except Exception, e:
                print "@@Excpetion@@", e
                try:
                    genre = Genre(genre_name=genre_name, user = user)
                    genre.save()
                except Exception,e:
                    print "$$$Ecpetion$$",e
                    return
                print "@@genre created and saved@@"
                message = "Genre created and saved."
                print message
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

    print "===In view_all_genre==="
    user = request.user
    genres = Genre.objects.all()
    print "==genres==", genres
    paginator = Paginator(genres, 5)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        genre_paginated = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        genre_paginated = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        genre_paginated = paginator.page(paginator.num_pages)
    # genres_serialized = GenreSerializer(genres, many=True)
    # genres_json = JSONRenderer().render(genres_serialized.data)
    # print "==genres_json==", genres_json
    return render_to_response("genre.html", {"genres": genre_paginated, "curr_user": user})


def view_all_music_tracks(request):

    print "===In view_all_music_tracks==="
    user = request.user
    print user
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
    # music_tracks_serialized = MusicTrackSerializer(music_tracks, many=True)
    # music_tracks_json = JSONRenderer().render(music_tracks_serialized.data)

    return render_to_response("track.html", {"tracks": music_tracks_paginated, "genres": genres, "curr_user": user})

@csrf_exempt
def register_user(request):

    print "==register_user=="
    # data = request.DATA
    data = request.POST
    print data
    email = str(data['email']).lower()
    first_name = data['user_name']
    last_name = data['user_name']
    password = data['password_su']
    try:
        user = User.objects.get(username = email)
        message = "User Already Registered"
        print message
    except Exception, e:
        print "#e#", e
        user = User(username=email, first_name=first_name, last_name=last_name, email=email )
        user.set_password(password)

        user.save()
        print "User Registered"
        message = "User Registered"

    user.backend = "django.contrib.auth.backends.ModelBackend"
    login(request, user)
    print "User logged in"
    data =json.dumps({"success": True, "message": message})
    return HttpResponse(data, content_type="application/json")

@csrf_exempt
def login_user(request):

    print "==login_user=="
    # data = request.DATA
    data = request.POST
    print data
    username = str(data['email_si']).lower()
    password = data['password_si']
    user = authenticate(username=username, password=password)
    if user is None:
        message = "Invalid Credentials"
        print message
        data =json.dumps({"success": False, "message": message})
        return HttpResponse(data, content_type="application/json")
    else:
        message = "User Looged in"
        print message
        data =json.dumps({"success": True, "message": message})
        login(request, user)
        return HttpResponse(data, content_type="application/json")


