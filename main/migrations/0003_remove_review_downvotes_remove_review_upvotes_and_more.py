# Generated by Django 5.1.2 on 2024-10-23 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_review_downvotes_remove_review_upvotes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='downvotes',
        ),
        migrations.RemoveField(
            model_name='review',
            name='upvotes',
        ),
        migrations.AddField(
            model_name='review',
            name='downvotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='review',
            name='upvotes',
            field=models.IntegerField(default=0),
        ),
    ]
