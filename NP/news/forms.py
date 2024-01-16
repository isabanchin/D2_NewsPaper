from django.forms import ModelForm
from .models import Post
from django import forms

# Создаём модельную форму


class PostForm(ModelForm):
    # В класс мета, как обычно, надо написать модель, по которой будет строиться форма, и нужные нам поля. Мы уже делали что-то похожее с фильтрами
    class Meta:
        model = Post
        fields = ['author', 'tittle', 'text', 'type']
        widgets = {
            'tittle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tittle'
            }),
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter text'
            }),
            'type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'author': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
