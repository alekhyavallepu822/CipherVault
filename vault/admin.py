
from django.contrib import admin
from .models import UserProfile, Document, DocumentPermission, AuditLog

admin.site.register(UserProfile)
admin.site.register(Document)


@admin.register(DocumentPermission)
class DocumentPermissionAdmin(admin.ModelAdmin):

    list_display = (
        'document',
        'user',
        'can_view',
        'granted_at'
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'document',
        'action',
        'timestamp'
    )

    readonly_fields = (
        'user',
        'document',
        'action',
        'timestamp'
    )
