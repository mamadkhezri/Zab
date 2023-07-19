from django import forms
from .models import Post, Comment

class PostUpdateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('image','title','content', 'upload', )



class PostCreateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('image','title','content', 'upload', )


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']