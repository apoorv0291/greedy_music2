from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from greedy import settings
from greedy_music.views import *
admin.autodiscover()


urlpatterns = [
    url(r'^search/?$', search_tracks), #search query
    #tracks url
    url(r'^track/?$', view_all_music_tracks),
    url(r'^track/(?P<track_id>\d+)/?$', track_details),
    #genre url
    url(r'^genre/?$', view_all_genre),
    url(r'^genre/(?P<genre_id>\d+)/?$', genre_details),
    #user urls
    url(r'^register/?$', register_user),
    url(r'^login/?$', login_user),
    url(r'^logout/?$', logout_user),
    url(r'^(?s).*$',view_all_music_tracks), #fallback url
    url(r'^$', view_all_music_tracks),#fallback url
    # url(r'^addGenre/?$', add_genre),
    # url(r'^addTrack/?$', add_track),
    # url(r'^editGenre/?$', edit_genre),
    # url(r'^editTrack/?$', edit_track),


    # url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    #     'document_root': settings.MEDIA_ROOT}),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)