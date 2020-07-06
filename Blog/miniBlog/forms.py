from django.forms import ModelForm
from .models import Comment


class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
