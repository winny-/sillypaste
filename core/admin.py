from django.contrib import admin
from .models import Paste

# Register your models here.
@admin.register(Paste)
class PasteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', )
