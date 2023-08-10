# Generated by Django 4.2.3 on 2023-08-10 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_remove_post_media_post_file_post_poster_delete_media'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='poster',
        ),
        migrations.RemoveField(
            model_name='post',
            name='file',
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(blank=True, null=True, upload_to='media/blog/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos_files', to='posts.post')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='blog/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_files', to='posts.post')),
            ],
        ),
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio', models.FileField(blank=True, null=True, upload_to='media/blog/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audios_files', to='posts.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='audios',
            field=models.ManyToManyField(related_name='associated_posts', to='posts.audio'),
        ),
        migrations.AddField(
            model_name='post',
            name='videos',
            field=models.ManyToManyField(related_name='associated_posts', to='posts.video'),
        ),
        migrations.AddField(
            model_name='post',
            name='file',
            field=models.ManyToManyField(related_name='associated_posts', to='posts.image'),
        ),
    ]
