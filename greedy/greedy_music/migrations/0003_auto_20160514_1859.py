# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('greedy_music', '0002_auto_20160514_1823'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='musictrack',
            unique_together=set([('music_title', 'artist_name')]),
        ),
    ]
