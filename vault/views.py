
import os

from django.http import FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import (
    UserProfile,
    Document,
    DocumentPermission,
    AuditLog,
)
from .forms import DocumentUploadForm, DocumentShareForm


def home(request):
    return render(request, 'vault/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'VIEWER'}
            )

            return render(request, 'vault/register.html', {
                'form': UserCreationForm(),
                'success': True
            })
    else:
        form = UserCreationForm()

    return render(request, 'vault/register.html', {
        'form': form
    })


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'vault/login.html', {
        'form': form
    })


def user_logout(request):
    if request.method == 'POST':
        logout(request)

    return redirect('home')


@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user
            document.save()

            return render(request, 'vault/upload.html', {
                'form': DocumentUploadForm(),
                'success': True
            })
    else:
        form = DocumentUploadForm()

    return render(request, 'vault/upload.html', {
        'form': form
    })


@login_required
def my_documents(request):
    documents = Document.objects.filter(
        owner=request.user
    )

    permissions = DocumentPermission.objects.filter(
        document__owner=request.user,
        can_view=True
    ).select_related('document', 'user')

    return render(request, 'vault/my_documents.html', {
        'documents': documents,
        'permissions': permissions
    })


@login_required
def shared_with_me(request):
    permissions = DocumentPermission.objects.filter(
        user=request.user,
        can_view=True
    ).select_related('document', 'document__owner')

    return render(request, 'vault/shared_with_me.html', {
        'permissions': permissions
    })


@login_required
def share_document(request):
    if request.method == 'POST':
        form = DocumentShareForm(
            request.POST,
            owner=request.user
        )

        if form.is_valid():
            document = form.cleaned_data['document']
            user = form.cleaned_data['user']

            DocumentPermission.objects.update_or_create(
                document=document,
                user=user,
                defaults={'can_view': True}
            )

            return render(request, 'vault/share.html', {
                'form': DocumentShareForm(owner=request.user),
                'success': True
            })
    else:
        form = DocumentShareForm(owner=request.user)

    return render(request, 'vault/share.html', {
        'form': form
    })


@login_required
def download_document(request, document_id):
    try:
        document = Document.objects.get(id=document_id)

    except Document.DoesNotExist:
        AuditLog.objects.create(
            user=request.user,
            document=None,
            action='ACCESS_DENIED'
        )
        raise Http404("Document not found")

    is_owner = document.owner_id == request.user.id

    has_permission = DocumentPermission.objects.filter(
        document=document,
        user=request.user,
        can_view=True
    ).exists()

    if not is_owner and not has_permission:
        AuditLog.objects.create(
            user=request.user,
            document=document,
            action='ACCESS_DENIED'
        )
        raise Http404("You are not authorized to access this document")

    try:
        file_handle = document.file.open('rb')

    except (FileNotFoundError, OSError):
        AuditLog.objects.create(
            user=request.user,
            document=document,
            action='ACCESS_DENIED'
        )
        raise Http404("Document file not found")

    AuditLog.objects.create(
        user=request.user,
        document=document,
        action='ACCESS_GRANTED'
    )

    return FileResponse(
        file_handle,
        as_attachment=True,
        filename=os.path.basename(document.file.name)
    )


@login_required
@require_POST
def revoke_permission(request, permission_id):
    permission = get_object_or_404(
        DocumentPermission,
        id=permission_id
    )

    if permission.document.owner_id != request.user.id:
        raise Http404("You are not authorized")

    permission.can_view = False
    permission.save(update_fields=['can_view'])

    return redirect('my_documents')
