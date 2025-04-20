# Register your models here.
from django.contrib import admin
from .models import Question, Result  # 👈 Import your models

admin.site.register(Question)         # 👈 Register the Question model
admin.site.register(Result)           # 👈 Register the Result model
