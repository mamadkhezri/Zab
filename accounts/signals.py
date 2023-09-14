from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, User, Notification, Relation
from django.core.handlers.wsgi import WSGIRequest
from django.test.client import RequestFactory
from posts.models import Post, Comment
from django.urls import reverse




@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
        instance.profile.save()



@receiver(post_save, sender=Post)
def notify_followers_new_post(sender, instance, created, **kwargs):
    if created:
        post_id = instance.pk
        post_slug = instance.slug
        url = reverse('posts:post_detail', kwargs={'post_id': post_id, 'post_slug': post_slug})

        for relation in instance.author.followers.all():
            Notification.objects.create(
                user=relation.from_author,  
                message=f'{instance.author.username} wrote a new post: <a href="{url}">{instance.title}</a>',
                link=f'/post/{instance.pk}/'
            )

@receiver(post_save, sender=Comment)
def notify_post_owner_new_comment(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.post.user,
            message=f'{instance.author.username} wrote a new post: {instance.content}',
            link=f'/post/{instance.post.pk}/'
        )