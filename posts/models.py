from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/')
    title = models.CharField(max_length=255)
    content = models.TextField()
    upload = models.FileField(upload_to='media/blog/')
    #tags = 
    #category = models.ManyToManyField(Category)
    counted_views = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    slug = models.SlugField()
    login_require = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
         ordering = ['-created_date', '-counted_views']

    def __str__(self):
        return f'{self.title} - {self.slug} - {self.created_date}'
    
    def get_absolute_url(self):
        print("PK:", self.pk)
        print("Slug:", self.slug)
        url = reverse('posts:post_detail', args=[str(self.pk), self.slug])
        print("Generated URL:", url)
        return url
    
    def user_can_like(self, user):
        user_like = user.uvotes.filter(post=self)
        if user_like.exists():
            return True
        return False
    


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_comments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    comment = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class vote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvotes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pvotes')

    def __str__(self):
        return f'{self.author} liked {self.post}'
    

	


        



