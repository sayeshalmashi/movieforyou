# Generated by Django 5.0.6 on 2024-06-10 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_movie_login_require'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='image',
            field=models.ImageField(default='blog/default.jpg', upload_to='blog/'),
        ),
    ]
