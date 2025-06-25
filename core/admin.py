from django.contrib import admin

from django.contrib import admin
from .models import EncryptedFile

@admin.register(EncryptedFile)
class EncryptedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'version', 'uploaded_at', 'expires_at', 'has_been_downloaded')
    list_filter = ('uploaded_at', 'has_been_downloaded', 'version')
    search_fields = ('file',)

