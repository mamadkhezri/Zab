from django import forms
from .models import Post

class PostUpdateForm(forms.ModelForm):
# همان فرمی است که در ماژول فزم ساختیم و اینجا ایمپوزت کردیم
	class Meta:
		model = Post
		fields = ('image','title','content', 'upload', )