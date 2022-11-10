import django
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import User


class Organization(models.Model):
    class Name(models.TextChoices):
        personal = 'personal', _('Personal')
        work = 'work', _('Work')
        education = 'education', _('Education')

    name = models.CharField(
        choices=Name.choices,
        default=Name.personal,
        max_length=9,
    )


class ToDo(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255)
    priority = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    tick = models.BooleanField(default=False)
    date = models.DateTimeField(default=django.utils.timezone.now)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ('-date',)

