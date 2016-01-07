# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('police_logs_map', '0002_auto_20160103_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='PoliceLogReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_from', models.DateTimeField()),
                ('date_to', models.DateTimeField()),
                ('authority', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='policelog',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='police_logs_map.PoliceLogReport', null=True),
        ),
    ]
