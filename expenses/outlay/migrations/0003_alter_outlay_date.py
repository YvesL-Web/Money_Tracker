# Generated by Django 4.1.7 on 2023-03-10 12:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outlay', '0002_alter_category_options_alter_outlay_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outlay',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
