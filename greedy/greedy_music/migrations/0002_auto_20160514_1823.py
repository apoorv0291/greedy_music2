# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('greedy_music', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='user',
            field=models.ForeignKey(related_name='user_genre', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='musictrack',
            name='user',
            field=models.ForeignKey(related_name='user_music_track', to=settings.AUTH_USER_MODEL),
        ),
    ]
