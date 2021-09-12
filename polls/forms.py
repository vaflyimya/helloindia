from .models import Comment
from django.forms import ModelForm, fields, TextInput, widgets, Textarea

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_autor', 'comment_text']

        widgets = {
            "comment_autor": TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'ваше имя'
            }),
            "comment_text": Textarea(attrs = {
                'class': 'form-control',
                'placeholder': 'текст комма'
            })
        }