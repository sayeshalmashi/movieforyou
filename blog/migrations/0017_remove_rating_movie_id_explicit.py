# Generated by Django 5.0.6 on 2024-09-17 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_rating_movie_id_explicit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='movie_id_explicit',
        ),
    ]
