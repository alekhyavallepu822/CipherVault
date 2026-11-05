
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('OWNER', 'Document Owner'),
        ('VIEWER', 'Document Viewer'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='VIEWER'
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Document(models.Model):

    title = models.CharField(max_length=200)

    file = models.FileField(upload_to='documents/')

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class DocumentPermission(models.Model):

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='permissions'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='document_permissions'
    )

    can_view = models.BooleanField(default=True)

    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['document', 'user'],
                name='unique_document_user_permission'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.document.title}"


class AuditLog(models.Model):

    ACTION_CHOICES = [
        ('ACCESS_GRANTED', 'Access Granted'),
        ('ACCESS_DENIED', 'Access Denied'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"
