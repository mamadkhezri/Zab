from django import forms
from .models import Post

class PostUpdateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('image','title','content', 'upload', )



class PostCreateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('image','title','content', 'upload', )