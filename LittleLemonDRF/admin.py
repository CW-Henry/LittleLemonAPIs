from django.contrib import admin
from .models import Book, Category, MenuItem, Rating

# Register your models here.
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Rating)