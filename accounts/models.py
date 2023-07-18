from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Relation(models.Model):
    from_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    to_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_author} follows {self.to_author}"

