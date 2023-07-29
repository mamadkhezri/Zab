from django.db import models
from django.contrib.auth.models import User

class Relation(models.Model):
    from_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    to_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_author} follows {self.to_author}"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/', null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    family_name = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username
        

