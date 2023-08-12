from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Image (models.Model):
    image = models.ImageField(upload_to='blog/')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='image_files')

class Video(models.Model):
    video = models.FileField(upload_to='blog/',null=True, blank=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE , related_name='videos_files')

class Audio(models.Model):
    audio = models.FileField(upload_to='blog/', null=True, blank=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE , related_name='audios_files')

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    #tags = 
    #category = models.ManyToManyField(Category)
    file = models.ManyToManyField(Image, related_name='associated_posts', blank=True) 
    videos = models.ManyToManyField(Video, related_name='associated_posts')
    audios = models.ManyToManyField(Audio, related_name='associated_posts')
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
        return user.uvotes.filter(post=self).exists()
    

    

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
    

	


        



