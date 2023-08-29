from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField



class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'phone_number', 'first_name', 'last_name')

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
			raise ValidationError('passwords dont match')
		return cd['password2']

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField(help_text="you can change password using <a href=\"../password/\">this form</a>.")

	class Meta:
		model = User
		fields = ('email', 'phone_number', 'first_name', 'last_name', 'profile_picture', 'bio', 'location', 'date_of_birth', 'gender', 'website', 'is_active', 'is_admin')


class UserRegistrationForm(forms.Form):
	first_name = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}))
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

 
	def clean_email(self):
		email = self.cleaned_data['email']
		user = User.objects.filter(email=email).exists()
		if user:
			raise ValidationError('this email already exists')
		return email

	def clean(self):
		cd = super().clean()
		p1 = cd.get('password1')
		p2 = cd.get('password2')

		if p1 and p2 and p1 != p2:
			raise ValidationError('password must match')
		

class UserLoginForm(forms.Form):
	username = forms.CharField(label='Email or username' ,widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control'}))


class EditUserForm(forms.ModelForm):
	email = forms.EmailField()
	
	class Meta:
		model = Profile
		fields = ('first_name', 'family_name', 'image', 'age', 'bio')

	def clean_age(self):
		age = self.cleaned_data.get('age')
		if age is not None and (age < 1 or age > 100):
			raise forms.ValidationError("Age must be between 1 and 100.")
		return age








