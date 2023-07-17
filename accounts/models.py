from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Relation(models.Model):
    from_user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    to_user= models.ForeignKey()

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(default=0)
    bio = models.TextField(null=True , blank=True)