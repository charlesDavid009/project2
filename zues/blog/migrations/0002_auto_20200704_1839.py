# Generated by Django 2.2.13 on 2020-07-04 17:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcomment',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='SubCommnets_likes', through='blog.SubCommentLikes', to=settings.AUTH_USER_MODEL),
        ),
    ]