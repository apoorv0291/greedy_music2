# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import greedy_music.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('genre_name', models.CharField(unique=True, max_length=50)),
                ('user', models.OneToOneField(related_name='user_genre', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['genre_name'],
                'verbose_name_plural': 'Genres',
            },
        ),
        migrations.CreateModel(
            name='MusicTrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('music_title', models.CharField(max_length=100)),
                ('music_track', models.FileField(upload_to=greedy_music.models.get_track_url)),
                ('artist_name', models.CharField(max_length=100)),
                ('ratings', models.DecimalField(max_digits=2, decimal_places=1)),
                ('genre', models.ManyToManyField(related_name='music_track', to='greedy_music.Genre')),
                ('user', models.OneToOneField(related_name='user_music_track', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['artist_name', 'music_track'],
                'verbose_name_plural': 'MusicTracks',
            },
        ),
        migrations.AlterUniqueTogether(
            name='musictrack',
            unique_together=set([('music_track', 'artist_name')]),
        ),
    ]
