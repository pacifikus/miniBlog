from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Blogger(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    bio = models.TextField(max_length=500, blank=True, default='Нет информации', verbose_name='Общая информация')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    class Meta:
        verbose_name = 'Автор блога'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('blogger', args=[str(self.id)])


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        Blogger.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user(sender, instance, created, **kwargs):
    instance.blogger.save()


class Blog(models.Model):
    blog_name = models.CharField(max_length=250, verbose_name='Название')
    last_upd_date = models.DateTimeField(auto_now=True)
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE, verbose_name='Автор')
    description = models.CharField(max_length=500, verbose_name='Описание', blank=True)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return self.blog_name

    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.id)])


class BlogMessage(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    create_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name='Описание')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='Блог')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['create_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('message_detail', args=[str(self.blog.id), str(self.id)])

    def get_short_text(self):
        return self.text[:300] + '...' if len(self.text) > 300 else self.text


class Comment(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name='Текст')
    blog_message = models.ForeignKey(BlogMessage, on_delete=models.CASCADE, verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-create_date']

    def __str__(self):
        return f'{self.author_name} - {self.create_date}'

    def get_short_text(self):
        return self.text[:150] + '...' if len(self.text) > 150 else self.text

    get_short_text.verbose_name = 'Текст'
