# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # დარწმუნდით, რომ ელექტრონული ფოსტის ველი აქ არის და უნიკალურია!
    ელ_ფოსტა = models.EmailField(unique=True, null=False, blank=False, verbose_name="ელ. ფოსტა")

    # თქვენი დამატებითი ველები
    ტელეფონის_ნომერი = models.CharField(max_length=20, blank=True, null=True, verbose_name="ტელეფონის ნომერი")
    ლოკაციის_დეტალები = models.TextField(
        blank=True,
        null=True,
        help_text="დეტალური ინსტრუქციები წიგნის ასაღებად ან ზოგადი ლოკაცია.",
        verbose_name="ლოკაციის დეტალები"
    )

    # ვანაცვლებთ USERNAME_FIELD-ს ელექტრონული ფოსტით
    USERNAME_FIELD = 'ელ_ფოსტა'
    # ვშლით ელექტრონულ ფოსტას REQUIRED_FIELDS-დან, რადგან ის ახლა USERNAME_FIELD-ია
    REQUIRED_FIELDS = ['username'] # თუ username საჭიროა, წინააღმდეგ შემთხვევაში []

    class Meta:
        verbose_name = "მომხმარებელი"
        verbose_name_plural = "მომხმარებლები"

    def __str__(self):
        return self.ელ_ფოსტა # მომხმარებლები ახლა ელექტრონული ფოსტით გამოჩნდებიან