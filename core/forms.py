from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from .models import User, Post, Comment


class ProfileCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        max_length=50,
        validators=[
            RegexValidator(
                r'^[a-zA-Z0-9_]+$',
                'Логин может содержать латинские буквы, цифры, и символ нижнего подчеркивания'
            )
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'description', 'avatar')


class PostCreationForm(forms.ModelForm):
    title_of_post = forms.CharField(
        label='Название поста',
        max_length=250,
    )

    class Meta:
        model = Post
        fields = ('title_of_post', 'text_of_post', 'image_of_post')


class CommentCreationForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text_of_comment', 'image_of_comment')
