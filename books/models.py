from django.db import models
from django.conf import settings # მომხმარებლის მორგებული მოდელისთვის

class Author(models.Model):
    სახელი = models.CharField(max_length=255, unique=True, verbose_name="ავტორის სახელი")
    აღწერა = models.TextField(blank=True, null=True, verbose_name="აღწერა")

    class Meta:
        verbose_name = "ავტორი"
        verbose_name_plural = "ავტორები"

    def __str__(self):
        return self.სახელი

class Genre(models.Model):
    სახელი = models.CharField(max_length=100, unique=True, verbose_name="ჟანრის სახელი")

    class Meta:
        verbose_name = "ჟანრი"
        verbose_name_plural = "ჟანრები"

    def __str__(self):
        return self.სახელი

class Condition(models.Model):
    სახელი = models.CharField(max_length=50, unique=True, verbose_name="მდგომარეობის სახელი")
    აღწერა = models.TextField(blank=True, null=True, verbose_name="აღწერა")

    class Meta:
        verbose_name = "მდგომარეობა"
        verbose_name_plural = "მდგომარეობები"

    def __str__(self):
        return self.სახელი

class Book(models.Model):
    მფლობელი = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='შეთავაზებული_წიგნები', verbose_name="მფლობელი")
    სათაური = models.CharField(max_length=255, verbose_name="სათაური") # Georgian: title
    ავტორი = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='წიგნები', verbose_name="ავტორი")
    ჟანრი = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='წიგნები', verbose_name="ჟანრი")
    მდგომარეობა = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True, related_name='წიგნები', verbose_name="მდგომარეობა")
    აღწერა = models.TextField(blank=True, null=True, verbose_name="აღწერა") # Georgian: description
    სურათი = models.ImageField(upload_to='წიგნის_პოსტერები/', blank=True, null=True, verbose_name="სურათი")
    ხელმისაწვდომია = models.BooleanField(default=True, verbose_name="ხელმისაწვდომია")
    მიღების_ლოკაციის_დეტალები = models.TextField(
        blank=True,
        null=True,
        help_text="კონკრეტული დეტალები ამ წიგნის ასაღებად.",
        verbose_name="მიღების ლოკაციის დეტალები"
    )
    შექმნის_თარიღი = models.DateTimeField(auto_now_add=True, verbose_name="შექმნის თარიღი")
    განახლების_თარიღი = models.DateTimeField(auto_now=True, verbose_name="განახლების თარიღი")

    class Meta:
        verbose_name = "წიგნი"
        verbose_name_plural = "წიგნები"
        ordering = ['-შექმნის_თარიღი']

    def __str__(self):
        return f"{self.სათაური} ავტორი: {self.ავტორი.სახელი if self.ავტორი else 'უცნობი'}"

class BookRequest(models.Model):
    წიგნი = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='მოთხოვნები', verbose_name="წიგნი")
    დაინტერესებული_მომხმარებელი = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='მოთხოვნილი_წიგნები', verbose_name="დაინტერესებული მომხმარებელი")
    სტატუსი = models.CharField(
        max_length=20,
        choices=[('მოლოდინში', 'მოლოდინში'), ('მიღებულია', 'მიღებულია'), ('უარყოფილია', 'უარყოფილია')],
        default='მოლოდინში',
        verbose_name="სტატუსი"
    )
    შეტყობინება = models.TextField(blank=True, null=True, verbose_name="შეტყობინება")
    შექმნის_თარიღი = models.DateTimeField(auto_now_add=True, verbose_name="შექმნის თარიღი")
    განახლების_თარიღი = models.DateTimeField(auto_now=True, verbose_name="განახლების თარიღი")

    class Meta:
        unique_together = ('წიგნი', 'დაინტერესებული_მომხმარებელი') # მომხმარებელს შეუძლია წიგნის მოთხოვნა მხოლოდ ერთხელ
        verbose_name = "წიგნის მოთხოვნა"
        verbose_name_plural = "წიგნის მოთხოვნები"

    def __str__(self):
        return f"მოთხოვნა '{self.წიგნი.სათაური}'-ზე {self.დაინტერესებული_მომხმარებელი.username}-ის მიერ ({self.სტატუსი})"