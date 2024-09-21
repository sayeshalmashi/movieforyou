# Generated by Django 5.0.6 on 2024-09-21 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_remove_rating_movie_id_explicit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword_id', models.IntegerField(null=True, unique=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='keywords',
            field=models.ManyToManyField(blank=True, related_name='movies', to='blog.keyword'),
        ),
    ]
