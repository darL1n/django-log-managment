from django.contrib import admin
from .models import Operation, LogFile, TraceBack
from django.contrib.auth.models import Group

class LogFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'created_at']
    list_filter = ['type', 'created_at']

class OperationAdmin(admin.ModelAdmin):
    list_display = ['id', 'level', 'created_at']
    list_filter = ['level', 'created_at']

class TraceBackAdmin(admin.ModelAdmin):
    list_display = ['id', 'level', 'created_at', 'is_corrected']
    list_filter = ['level', 'created_at', 'is_corrected']

admin.site.unregister(Group)
admin.site.register(Operation, OperationAdmin)
admin.site.register(TraceBack, TraceBackAdmin)
admin.site.register(LogFile, LogFileAdmin)