from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostSearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from posts.models import Post


class HomeView(View):
    form_class = PostSearchForm

    def get(self, request):
        posts = Post.objects.all() 
        form = self.form_class(request.GET)  
        if form.is_valid() and form.cleaned_data['search']:
            search_query = form.cleaned_data['search']
            posts = posts.filter(title__contains=search_query)

        return render(request, 'home/index.html', {'posts': posts, 'form': form})
		
        
