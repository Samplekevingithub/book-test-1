# Generated by Django 5.0.6 on 2024-06-05 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_book_rental'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_user',
            field=models.BooleanField(default=False, verbose_name='Is user'),
        ),
    ]
