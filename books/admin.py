# books/admin.py
from django.contrib import admin

from .models import Book, Author, Genre, Condition, BookRequest

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Condition)
admin.site.register(BookRequest)