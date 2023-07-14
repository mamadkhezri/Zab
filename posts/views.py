from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Post
from .forms import PostUpdateForm
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        return render(request, 'posts/detail_post.html', {'post': post})
    


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
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.author.id == request.user.id:
            form = PostUpdateForm(instance=post)
            return render(request, 'posts/update.html', {'form': form, 'post': post})
        else:
            messages.error(request, 'You cannot update this post.', 'danger')
            return redirect('home:home')

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.author.id == request.user.id:
            form = PostUpdateForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post updated successfully.')
                return redirect('posts:post_detail', post_id=post.id, post_slug=post.slug)
            else:
                messages.error(request, 'Failed to update the post.', 'danger')
                return render(request, 'posts/update.html', {'form': form, 'post': post})
        else:
            messages.error(request, 'You cannot update this post.', 'danger')
            return redirect('home:home')


    



