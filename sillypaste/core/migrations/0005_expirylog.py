# Generated by Django 3.1.1 on 2020-09-05 12:49

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [('core', '0004_auto_20200904_1501')]

    operations = [
        migrations.CreateModel(
            name='ExpiryLog',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'expired_ids',
                    models.CharField(
                        blank=True,
                        max_length=1048576,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile('^\\d+(?:,\\d+)*\\Z'),
                                code='invalid',
                                message='Enter only digits separated by commas.',
                            )
                        ],
                    ),
                ),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('count', models.PositiveIntegerField(default=0)),
                ('reclaimed_space', models.PositiveIntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
            ],
        )
    ]
