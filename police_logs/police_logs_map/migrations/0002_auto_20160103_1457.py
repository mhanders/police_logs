# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('police_logs_map', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='policelog',
            old_name='datetime_repored',
            new_name='datetime_reported',
        ),
    ]
