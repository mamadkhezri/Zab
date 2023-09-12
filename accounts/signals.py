from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, User, Notification, Relation
from django.core.handlers.wsgi import WSGIRequest
from django.test.client import RequestFactory
from .views import CreateNotificationView
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
def create_post_notification(sender, instance, created, **kwargs):
    if created:
        request = RequestFactory().get(reverse('create-notification', kwargs={'pk': instance.pk}))
        response = CreateNotificationView.as_view()(request, instance=instance)

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        request = RequestFactory().get(reverse('create-notification', kwargs={'pk': instance.pk}))
        response = CreateNotificationView.as_view()(request, instance=instance)

@receiver(post_save, sender=Relation)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        # Check if both users are following each other
        if Relation.objects.filter(from_author=instance.to_author, to_author=instance.from_author).exists():
            request = RequestFactory().get(reverse('create-notification', kwargs={'pk': instance.pk}))
            response = CreateNotificationView.as_view()(request, instance=instance)