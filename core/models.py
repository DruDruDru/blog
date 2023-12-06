from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse


class User(AbstractUser):
    username = models.CharField(primary_key=True, verbose_name='Имя пользователя', max_length=50,
                                unique=True, blank=False)
    email = models.EmailField(verbose_name='Почта', max_length=100,
                              unique=True, blank=False)
    description = models.TextField(verbose_name='Описание', max_length=1000,
                                   blank=True, null=True)
    avatar = models.ImageField(verbose_name='Аватар', blank=True,
                               null=True, upload_to='images/avatars')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.pk)])


class Comment(models.Model):
    objects = None
    text_of_comment = models.TextField(verbose_name='Сообщение', max_length=2500,
                                       blank=False, null=False)
    image_of_comment = models.ImageField(verbose_name='Изображение', blank=True,
                                         null=True, upload_to='images/comment')
    post = models.ForeignKey(verbose_name='Пост', to='Post',
                             on_delete=models.CASCADE, null=False,
                             blank=False, default='', auto_created='Post')
    upload_by = models.ForeignKey(verbose_name='Автор', null=False, blank=False,
                                  to='User', on_delete=models.CASCADE,
                                  auto_created='User', default='', )

    class Meta:
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text_of_comment


class Post(models.Model):
    objects = None
    title_of_post = models.CharField(verbose_name='Заголовок', max_length=250,
                                     blank=False, null=False)
    text_of_post = models.TextField(verbose_name='Описание', max_length=2500,
                                    blank=False, null=False)
    image_of_post = models.ImageField(verbose_name='Изображение', blank=True,
                                      null=True, upload_to='images/post')
    created_by = models.ForeignKey(verbose_name='Автор', null=True, blank=False,
                                   to='User', on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title_of_post

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])
