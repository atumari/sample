from django.contrib import admin
from .models import Author, Question

# Register your models here.
admin.site.register(Author)
admin.site.register(Question)