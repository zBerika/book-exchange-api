# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # Импортируем базовый UserAdmin
from .models import User # <- ОЧЕНЬ ВАЖНО: Импортируем User, а не CustomUser

@admin.register(User) # Регистрируем вашу модель User
class CustomUserAdmin(BaseUserAdmin): # Наследуемся от BaseUserAdmin
    # Добавляем ваши новые поля в админку, чтобы они отображались
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('ტელეფონის_ნომერი', 'ლოკაციის_დეტალები')}), # Используйте имена полей из models.py
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('ტელეფონის_ნომერი', 'ლოკაციის_დეტალები')}),
    )

    list_display = ('username', 'email', 'is_staff', 'ტელეფონის_ნომერი') # Чтобы эти поля отображались в списке пользователей
    search_fields = ('username', 'email', 'ტელეფონის_ნომერი') # Чтобы можно было искать по ним
    ordering = ('username',) # Сортировка по имени пользователя