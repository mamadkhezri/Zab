from django import forms
from .models import Post, Comment, Media
from multiupload.fields import MultiFileField
from django.forms import modelformset_factory





class PostUpdateCreateForm(forms.ModelForm):
	image = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5, required=False)

	class Meta:
		model = Post
		fields = ('image','title','content' )

class MediaForm(forms.ModelForm):
	class Meta:
		model = Media
		fields = ('post','image', 'file', 'media_type')
MediaFormSet = modelformset_factory(Media, form=MediaForm, extra=1, max_num=10)

		
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
	


class CommentReplyForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['comment']