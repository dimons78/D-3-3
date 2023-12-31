from django.conf import settings
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    # Добавьте    статус    DRAFT — черновик.
    # Пока объявление в черновике, оно показывается только автору
    #  объявления, другим пользователям ононедоступно
    DRAFT = "DRAFT", "Черновик"



class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.DRAFT
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    objects = models.Manager()

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявления'



