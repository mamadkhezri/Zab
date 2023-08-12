from typing import Any
from django import http
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Post, Comment, vote , Image, Audio, Video
from django.http import JsonResponse
from .forms import PostUpdateCreateForm , CommentCreateForm, CommentReplyForm
from django.utils.text import slugify
from django.template.defaultfilters import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class PostDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def get(self, request, post_id, post_slug):
        post_instance = get_object_or_404(Post, pk=post_id, slug=post_slug)
        comments = post_instance.post_comments.filter(is_reply=False)
        can_like = False
        if request.user.is_authenticated and post_instance.user_can_like(request.user):
            can_like = True

        can_unlike = False
        if request.user.is_authenticated and vote.objects.filter(author=request.user, post=post_instance).exists():
            can_unlike = True

        form = self.form_class()
        reply_form = self.form_class_reply()

        likes_count = vote.objects.filter(post=post_instance).count()

        return render(request, 'posts/detail_post.html', {
            'post': post_instance,
            'comments': comments,
            'form': form,
            'reply_form': reply_form,
            'can_like': can_like,
            'can_unlike': can_unlike,
            'likes_count': likes_count,
        })

    @method_decorator(login_required)
    def post(self, request, post_id, post_slug):
        post_instance = get_object_or_404(Post, pk=post_id, slug=post_slug)
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post_instance
            new_comment.save()
            messages.success(request, 'Your comment has been submitted successfully.', extra_tags='success')
            

            form = self.form_class()
        
        comments = post_instance.post_comments.filter(is_reply=False)
        reply_form = self.form_class_reply()

        return render(request, 'posts/detail_post.html', {
            'post': post_instance,
            'comments': comments,
            'form': form,
            'reply_form': reply_form,
        })


class PostDeleteView(LoginRequiredMixin, View):
    def get (self, request, post_id):
        post= get_object_or_404(Post , pk=post_id)
        if post.author.id == request.user.id:
            post.delete()
            messages.success(request, 'post delete ')
        else:
            messages.error(request, 'you can not post delete')
        return redirect('home:home')
    



class PostUpdateView(LoginRequiredMixin, View):

    def setup(self, request, *args: Any, **kwargs: Any):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, post_id):
        post = self.post_instance
        if post.author.id == request.user.id:
            form = PostUpdateCreateForm(instance=post)
            return render(request, 'posts/update.html', {'form': form, 'post': post})
        else:
            messages.error(request, 'You cannot update this post.', 'danger')
            return redirect('home:home')

    def post(self, request, post_id):
        post = self.post_instance
        if post.author.id == request.user.id:
            form = PostUpdateCreateForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post.title = form.cleaned_data['title']
                post.slug = slugify(post.title)
                post.save()
                messages.success(request, 'Post updated successfully.')
                return redirect('posts:post_detail', post_id=post.id, post_slug=post.slug)
            else:
                messages.error(request, 'Failed to update the post.', 'danger')
                return render(request, 'posts/update.html', {'form': form, 'post': post})
        else:
            messages.error(request, 'You cannot update this post.', 'danger')
            return redirect('home:home')
        


class PostcreateView(LoginRequiredMixin, View):
    form_class = PostUpdateCreateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'posts/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['title'][:30])
            new_post.author = request.user
            new_post.save()

            image_files = request.FILES.getlist('image')  # Retrieve a list of uploaded image files
            video_files = request.FILES.getlist('video')  # Retrieve a list of uploaded video files
            audio_files = request.FILES.getlist('audio')  # Retrieve a list of uploaded audio files

            try:
                for image_file in image_files:
                    Image.objects.create(post=new_post, image=image_file)
                for video_file in video_files:
                    Video.objects.create(post=new_post, video=video_file)
                for audio_file in audio_files:
                    Audio.objects.create(post=new_post, audio=audio_file)
            except Exception as e:
                print("Error during file creation:", e)

            messages.success(request, 'You created a new post', 'success')
            return redirect('posts:post_detail', new_post.id, new_post.slug)

        return render(request, 'posts/create.html', {'form': form})

class PostAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        post_instance = get_object_or_404(Post, id=post_id)
        comment_instance = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.post = post_instance
            reply.reply = comment_instance
            reply.is_reply = True
            reply.save()
        return redirect('posts:post_detail', pk=post_instance.pk, slug=post_instance.slug)
    
class LikePostView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = vote.objects.get_or_create(author=request.user, post=post)
        if not created:
            like.delete()
        return redirect('posts:post_detail', post.id, post.slug)
    
class UnlikePostView(LoginRequiredMixin, View):
    def unlike_post(self, request, post):
        try:
            existing_like = vote.objects.get(author=request.user, post=post)
            existing_like.delete()
        except vote.DoesNotExist:
            pass
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.method == "GET" and request.user.is_authenticated:
            self.unlike_post(request, post)
            return redirect('posts:post_detail', post_id=post_id, post_slug=post.slug)
        return redirect('posts:post_detail', post_id=post_id, post_slug=post.slug)



    



