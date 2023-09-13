from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from .managers import UserManager



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female"), ("other", "Other")], blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    friends = models.ManyToManyField('self', symmetrical=True)
    blocked_users = models.ManyToManyField('self')
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'username', 'full_name']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin



class Relation(models.Model):
    from_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    to_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_author} follows {self.to_author}"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/', null=True, blank=True, default='static/img/defult.jpg')
    full_name = models.CharField(max_length=100, default='The author of Zab')
    age = models.PositiveSmallIntegerField(null=True, blank=True, validators=[
        MinValueValidator(1, message='Age must be at least 1.'),
        MaxValueValidator(100, message='Age cannot exceed 100.'),
    ])
    bio = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    link = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    viewed  = models.BooleanField(default=False)

    def __str__(self):
        return self.message
        

