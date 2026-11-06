
from pathlib import Path

from django import forms
from django.contrib.auth.models import User

from .models import Document


class DocumentUploadForm(forms.ModelForm):

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    ALLOWED_EXTENSIONS = {
        '.pdf',
        '.txt',
        '.csv',
    }

    class Meta:
        model = Document
        fields = ['title', 'file']

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')

        if not uploaded_file:
            raise forms.ValidationError('Please select a file.')

        extension = Path(uploaded_file.name).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise forms.ValidationError(
                'Only PDF, TXT and CSV files are allowed.'
            )

        if uploaded_file.size > self.MAX_FILE_SIZE:
            raise forms.ValidationError(
                'File size must not exceed 10 MB.'
            )

        # Basic PDF file signature check
        if extension == '.pdf':
            uploaded_file.seek(0)
            file_signature = uploaded_file.read(5)
            uploaded_file.seek(0)

            if file_signature != b'%PDF-':
                raise forms.ValidationError(
                    'Invalid PDF file.'
                )

        return uploaded_file


class DocumentShareForm(forms.Form):

    document = forms.ModelChoiceField(
        queryset=Document.objects.none()
    )

    user = forms.ModelChoiceField(
        queryset=User.objects.none()
    )

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner')
        super().__init__(*args, **kwargs)

        self.fields['document'].queryset = Document.objects.filter(
            owner=owner
        )

        self.fields['user'].queryset = User.objects.exclude(
            id=owner.id
        )
