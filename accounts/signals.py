from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, User

@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
        instance.profile.save()
