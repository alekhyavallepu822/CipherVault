
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Document, DocumentPermission, AuditLog
from .forms import DocumentUploadForm


class DocumentAccessTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            password='testpass123'
        )

        self.viewer = User.objects.create_user(
            username='viewer',
            password='testpass123'
        )

        self.other_user = User.objects.create_user(
            username='other',
            password='testpass123'
        )

        self.document = Document.objects.create(
            title='Test Document',
            owner=self.owner,
            file=SimpleUploadedFile(
                'test.txt',
                b'Test document content',
                content_type='text/plain'
            )
        )

    def test_owner_can_download_document(self):
        self.client.login(
            username='owner',
            password='testpass123'
        )

        response = self.client.get(
            reverse('download_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 200)
        response.close()

    def test_authorized_viewer_can_download_document(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.viewer,
            can_view=True
        )

        self.client.login(
            username='viewer',
            password='testpass123'
        )

        response = self.client.get(
            reverse('download_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 200)
        response.close()

    def test_unauthorized_user_cannot_download_document(self):
        self.client.login(
            username='other',
            password='testpass123'
        )

        response = self.client.get(
            reverse('download_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            AuditLog.objects.filter(
                user=self.other_user,
                document=self.document,
                action='ACCESS_DENIED'
            ).exists()
        )
        response.close()

    def test_revoked_viewer_cannot_download_document(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.viewer,
            can_view=False
        )

        self.client.login(
            username='viewer',
            password='testpass123'
        )

        response = self.client.get(
            reverse('download_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            AuditLog.objects.filter(
                user=self.viewer,
                document=self.document,
                action='ACCESS_DENIED'
            ).exists()
        )
        response.close()

    def test_invalid_file_extension(self):
        uploaded_file = SimpleUploadedFile(
            'test.exe',
            b'sample content'
        )

        form = DocumentUploadForm(
            data={'title': 'Test Document'},
            files={'file': uploaded_file}
        )

        self.assertFalse(form.is_valid())

    def test_invalid_pdf_signature(self):
        uploaded_file = SimpleUploadedFile(
            'fake.pdf',
            b'This is not a PDF file'
        )

        form = DocumentUploadForm(
            data={'title': 'Test PDF'},
            files={'file': uploaded_file}
        )

        self.assertFalse(form.is_valid())

    def test_valid_pdf_upload(self):
        uploaded_file = SimpleUploadedFile(
            'valid.pdf',
            b'%PDF-1.4 sample PDF content'
        )

        form = DocumentUploadForm(
            data={'title': 'Valid PDF'},
            files={'file': uploaded_file}
        )

        self.assertTrue(form.is_valid())
