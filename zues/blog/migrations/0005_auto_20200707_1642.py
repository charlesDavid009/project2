# Generated by Django 2.2 on 2020-07-07 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200704_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.Blog'),
        ),
    ]