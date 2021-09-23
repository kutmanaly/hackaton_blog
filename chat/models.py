from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Room(models.Model):
    creator = models.ForeignKey(User, verbose_name='Админ', on_delete=models.CASCADE)
    invited = models.ManyToManyField(User, verbose_name='Участники', related_name='invited_user')
    date = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комната чата'
        verbose_name_plural = 'Комнаты чатов'


class Chat(models.Model):
    room = models.ForeignKey(Room, verbose_name='Команата чата', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', verbose_name='Пользователь', on_delete=models.CASCADE)
    text = models.TextField('Сообщение', max_length=500)
    date = models.DateTimeField('Дата отправки', auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение чата'
        verbose_name_plural = 'Сообщения чатов'

