# Generated by Django 3.2.7 on 2021-09-23 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.comment'),
        ),
    ]