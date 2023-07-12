from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from posts.models import Post


class HomeView(View):
    def get(self, request):
        Posts= Post.objects.all
        return render(request, 'home/index.html', {'posts':Posts})
		
        
