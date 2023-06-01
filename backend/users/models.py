from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = ('email', 'first_name', 'last_name')
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=254,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=150,
        validators=(UnicodeUsernameValidator(), )
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class UserFollowing(models.Model):

    user_id = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )
    following_user_id = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user_id', 'following_user_id', ),
                name='unique_followers'
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_prevent_self_follow',
                check=~models.Q(user_id=models.F('following_user_id')),
            ),
        )
        ordering = ('-created', )

    def __str__(self):
        return f'{self.user_id} follows {self.following_user_id}'
