from django import forms
from .models import Post, Comment , Image, Video,Audio
from django.forms.widgets import ClearableFileInput

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class PostUpdateCreateForm(forms.ModelForm):
    image = forms.FileField(widget=MultipleFileInput(), required=False)
    video = forms.FileField(widget=MultipleFileInput(), required=False)
    audio = forms.FileField(widget=MultipleFileInput(), required=False)
    
    class Meta:
        model = Post
        fields = ('image', 'video', 'audio', 'title', 'content')

    def save(self, commit=True):
        post = super().save(commit=commit)

        image_files = self.cleaned_data.get('image')
        video_files = self.cleaned_data.get('video')
        audio_files = self.cleaned_data.get('audio')

        if image_files:
            for image in image_files:
                Image.objects.create(post=post, image=image)
        if video_files:
            for video in video_files:
                Video.objects.create(post=post, video=video)
        if audio_files:
            for audio in audio_files:
                Audio.objects.create(post=post, audio=audio)
        return post
		
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
	


class CommentReplyForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['comment']