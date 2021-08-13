from django.contrib import admin
from .models import Paste, ExpiryLog

# Register your models here.
@admin.register(Paste)
class PasteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', )


@admin.register(ExpiryLog)
class ExpiryLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'completed', 'timestamp', 'paste_count', 'reclaimed_space', 'user_count')
