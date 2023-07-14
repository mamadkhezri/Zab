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
    form_class = PostUpdateForm
    
    def setup(self, request, *args, **kwargs):
	    self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
            return super().setup(request, *args, **kwargs)

    
    def dispatch(self, request, *args, **kwargs):
		post = self.post_instance
		if not post.user.id == request.user.id:
			messages.error(request, 'you cant update this post', 'danger')
			return redirect('home:home')
		return super().dispatch(request, *args, **kwargs)
    

    def get(self, request, *args, **kwargs):
		post = self.post_instance        
		form = self.form_class(instance=post)
		return render(request, 'posts/update.html', {'form':form})
    

    def post(self, request, *args, **kwargs):
		post = self.post_instance
		form = self.form_class(request.POST, instance=post)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.slug = slugify(form.cleaned_data['body'][:30])
			new_post.save()
			messages.success(request, 'you updated this post', 'success')
			return redirect('home:post_detail', post.id, post.slug)
        


    



