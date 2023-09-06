from django import forms
from django.core.exceptions import ValidationError
from .models import Profile
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm





class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'phone_number', 'full_name')

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
		fields = ('email', 'phone_number', 'full_name', 'profile_picture', 'bio', 'location', 'date_of_birth', 'gender', 'website', 'is_active', 'is_admin')


class UserRegistrationForm(forms.Form):
	full_name = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}))
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	phone_number =forms.CharField(label='phone number', widget=forms.NumberInput(attrs={'class':'form-control'}))
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
		fields = ('full_name', 'image', 'age', 'bio')

	def clean_age(self):
		age = self.cleaned_data.get('age')
		if age is not None and (age < 1 or age > 100):
			raise forms.ValidationError("Age must be between 1 and 100.")
		return age



class UserPasswordResetForm(PasswordResetForm):
	email = forms.EmailField(label='email address', widget=forms.TextInput(attrs={'class':'form-control'}))


class CustomPasswordResetConfirmForm(SetPasswordForm):
    """
    Custom form for password reset confirmation.
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text="Enter your new password.",
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text="Enter the same password as above, for verification.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'New Password'})
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'Confirm New Password'})

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        return cleaned_data
		

# class UserEnterNewPassword(SetPasswordForm):
	# password = forms.CharField(label='New password',  widget=forms.PasswordInput(attrs={'class':'form-control'}))
	# cpassword = forms.CharField(label='Confirm password',  widget=forms.PasswordInput(attrs={'class':'form-control'}))

	# def __init__(self, user, *args, **kwargs):
		# super(UserEnterNewPassword, self).__init__(user, *args, **kwargs)

# from django import forms
# from django.contrib.auth.forms import SetPasswordForm