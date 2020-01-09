from django.contrib import admin

from .models import Message, RegExp


class MessageAdmin(admin.ModelAdmin):
    list_display = ('with_file', 'pattern_found', 'pattern', 'text', 'file_link', 'created_at')


class RegExpAdmin(admin.ModelAdmin):
    list_display = ('pattern',)


admin.site.register(Message, MessageAdmin)
admin.site.register(RegExp, RegExpAdmin)