from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("text", "group")
        labels = {
            "text": ("Текст поста"),
            "group": ("Группа")
        }
        help_texts = {
            "text": ("Текст поста"),
            "group": ("Группа поста")
        }
        widgets = {
            "group": forms.Select(attrs={"class": "custom-select md-form"}),
        }
        error_messages = {
            "text": {
                'null': 'Простите, но вы похоже забыли написать текст'
            }
        }
