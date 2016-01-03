# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PoliceLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_repored', models.DateTimeField()),
                ('datetime_occurred', models.DateTimeField()),
                ('incident_type', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=300)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('detail', models.TextField()),
                ('authority', models.CharField(max_length=20)),
            ],
        ),
    ]
