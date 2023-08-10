from django import forms
from .models import Post, Comment
from multiupload.fields import MultiFileField


class PostUpdateCreateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('poster','title','content','file')

		
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
	


class CommentReplyForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['comment']