# Generated by Django 5.0.6 on 2024-06-05 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_alter_rental_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_user',
            field=models.BooleanField(default=True, verbose_name='Is user'),
        ),
    ]