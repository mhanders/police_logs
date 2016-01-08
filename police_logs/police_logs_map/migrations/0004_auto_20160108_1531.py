# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('police_logs_map', '0003_auto_20160103_1734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policelog',
            name='report',
        ),
        migrations.DeleteModel(
            name='PoliceLogReport',
        ),
    ]
