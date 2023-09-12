from typing import Any
from django import http
from .models import User,Relation, Notification
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm, EditUserForm, UserPasswordResetForm, CustomPasswordResetConfirmForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from posts.models import Post
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from webpush import send_user_notification



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
            user_registration_info = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password1'],  # Use 'password1' field
            }

            # Create a new User instance using your custom user manager
            user = User.objects.create_user(
                email=user_registration_info['email'],
                username=user_registration_info['username'],
                full_name=user_registration_info['full_name'],
                phone_number=user_registration_info['phone_number'],
                password=user_registration_info['password']
            )

            # Redirect to user login or any other appropriate view
            return redirect('accounts:user_login')

        return render(request, self.template_name, {'form': form})
		    



class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    success_url = 'home:home'

    def setup(self, request, *args, **kwargs):
        self.next= request.GET.get('next', None)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                if self.next:
                    return redirect(self.next)
                return redirect(self.success_url)
            else:
                messages.error(request, 'Username or password is incorrect.')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home:home')


class UserProfileView(View):
    @method_decorator(login_required(login_url='/accounts/login/'))
    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, pk=user_id)
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
    

class EditUserView(LoginRequiredMixin, View):
    form_class = EditUserForm

    def get (self, request):
        form = self.form_class(instance=request.user.profile, initial={'email':request.user.email})
        return render(request, 'accounts/edit_profile.html', {'form':form})
    
    def post (self,request):
        form =self.form_class(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'edit profile successfully', extra_tags='success')
        return redirect('accounts:user_profile', request.user.id)


  
class UserPasswordResetView(auth_views.PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'accounts/input_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
	template_name = 'accounts/send_email_reset.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm  # Use the custom form
    template_name = 'accounts/input_password_form.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_action_url'] = reverse_lazy('accounts:password_reset_confirm', kwargs={'uidb64': self.kwargs['uidb64'], 'token': self.kwargs['token']})
        return context



    
class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
	template_name = 'accounts/password_change_message.html'


class GetNotificationsView(View):
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user, viewed=False).order_by('-timestamp')
        notifications_data = [{'message': n.message, 'id': n.id} for n in notifications]
        return JsonResponse({'notifications': notifications_data})

class MarkNotificationAsViewedView(View):
    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id)
        notification.viewed = True
        notification.save()
        return JsonResponse({'message': 'Notification marked as viewed'})







        

 
		   