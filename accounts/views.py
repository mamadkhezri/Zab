from typing import Any
from django import http
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from posts.models import Post
from .models import Relation


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(
                cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'you registered successfully', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def setup(self, request,  *args: Any, **kwargs: Any) -> None:
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'username or password is wrong', 'warning')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        # Use 'author' instead of 'user'
        posts = Post.objects.filter(author=user)
        relation= Relation.objects.filter(from_author=request.user, to_author=user )
        if relation.exists():
            is_following= True
        return render(request, 'accounts/profile.html', {'user': user, 'posts': posts, 'is_following':is_following})


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        to_user = get_object_or_404(User, id=user_id)
        from_user = request.user

        if to_user != from_user and not Relation.objects.filter(from_author=from_user, to_author=to_user).exists():
            Relation(from_author=from_user, to_author=to_user).save()
            messages.success(request, f'You are now following {to_user.username}.')
        else:
            messages.error(request, 'Unable to follow this user.')

        return redirect('accounts:user_profile', user_id=to_user.id)

class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        to_user = get_object_or_404(User, id=user_id)
        from_user = request.user

        try:
            relation = Relation.objects.get(from_author=from_user, to_author=to_user)
            relation.delete()
            messages.success(request, f'You have unfollowed {to_user.username}.')
        except Relation.DoesNotExist:
            messages.error(request, 'Unable to unfollow this user.')

        return redirect('accounts:user_profile', user_id=to_user.id)
        

 
		   