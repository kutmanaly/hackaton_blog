from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    # чтобы не дублировать код при создании юзера и админа
    def _create(self, email, password, name, **extra_fields):
        if not email:   # проверяет, есть ли email
            raise ValueError('Email не может быть пустым')
        email = self.normalize_email(email)  # нормальизует email
        user = self.model(email=email, name=name, **extra_fields)  # создается полюзователь
        user.set_password(password)  # устанавливает шифрованный код
        user.save()  # обновляет объект БД
        return user

    # создаёт обычного пользователя
    def create_user(self, email, password, name, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        # устанавливается значение по умолчанию
        extra_fields.setdefault('is_active', False)
        return self._create(email, password, name, **extra_fields)

    def create_superuser(self, email, password, name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create(email, password, name, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField('Электронная почта', primary_key=True)
    name = models.CharField('Имя', max_length=50)
    last_name = models.CharField("Фамилия", max_length=50, blank=True)
    is_active = models.BooleanField("Активный?", default=False)
    is_staff = models.BooleanField("Админ?", default=False)
    activation_code = models.CharField("Код активации", max_length=8, blank=True)

    # привязка менджера
    objects = UserManager()

    # указывает поле, которое будет использоваться как логин
    USERNAME_FIELD = 'email'
    # указываются объяжательные поля, кроме username и password
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    # какие пользователи могут иметь доступ к админ панели
    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff

    # создает код активации
    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(8)
        self.activation_code = code
        self.save()

    # отправляет письмо активации
    def send_activation_mail(self):
        from django.core.mail import send_mail
        message = f'Ваш код активации: {self.activation_code}'
        send_mail('Активация аккаунта',
                  message,
                  'hello@gmail.com',
                  [self.email])
