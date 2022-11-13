from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):

    def create_user(self, username, password):
        if not username:
            raise ValueError("User Most Have A Username")
        if not password:
            raise ValueError("User Most Have A Password")

        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.super_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    """
    If you need full control over User model,
    it is better to use AbstractBaseUser but if you are just adding things to
    the existing user, for example, you just want to add an extra field
    location field or any other profile data then use AbstractUser.
    """

    def user_directory_path(self, filename):
        return f'u{self.id}/admin/profile/{filename}'

    username = models.CharField(max_length=63, unique=True)
    password = models.CharField(max_length=127)
    super_admin = models.BooleanField(default=False)
    photo = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'

    @property
    def is_staff(self):
        """ Is the User a member of staff? """
        return self.super_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'User'
        verbose_name_plural = 'user'
        ordering = ['username']

    @property
    def get_photo(self):
        try:
            return self.photo.url
        except ValueError:
            return None


class Token(Token):
    user = models.ForeignKey(
        User,
        related_name='auth_token',
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )

    class Meta:
        verbose_name_plural = 'token'
        db_table = 'Token'


@receiver(post_save, sender=User)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)

