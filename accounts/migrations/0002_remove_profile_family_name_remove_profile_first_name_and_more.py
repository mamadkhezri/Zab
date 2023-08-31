# Generated by Django 4.2.3 on 2023-08-31 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='family_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AddField(
            model_name='profile',
            name='full_name',
            field=models.CharField(default='The author of Zab', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(default='the author of zab', max_length=70),
            preserve_default=False,
        ),
    ]
