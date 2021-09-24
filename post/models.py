from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

STATUS_CHOICES = (
    ('open', 'Открытое'),
    ('closed', 'Закрытое'),
    ('draft', 'Черновик')
)


class Post(models.Model):
    user = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=255)
    image = models.ImageField('Картинка', upload_to='posts', blank=True)
    text = models.TextField('Текст')
    created_at = models.DateField("Дата создания", auto_now_add=True)
    updated_at = models.DateField("Дата редактирования", auto_now=True)
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',
                                verbose_name='Объявление')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    text = models.TextField('Текст')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)


    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.post} --> {self.user}'


class Like(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(unique=True, default=False)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'






