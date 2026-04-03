from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display  = ('title', 'subject', 'uploaded_by', 'uploaded_at', 'is_active')
    list_filter   = ('subject', 'is_active')
    search_fields = ('title', 'uploaded_by__first_name')
    list_editable = ('is_active',)
