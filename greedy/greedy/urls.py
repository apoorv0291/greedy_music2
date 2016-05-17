from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from greedy import  settings
from greedy.views import *
admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^greedymusic/', include('greedy_music.urls')),
    url(r'^$', include('greedy_music.urls'))

    # url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    #     'document_root': settings.MEDIA_ROOT}),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)