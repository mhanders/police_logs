# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('police_logs_map', '0004_auto_20160108_1531'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='policelog',
            unique_together=set([('datetime_reported', 'datetime_occurred', 'address', 'detail')]),
        ),
    ]
