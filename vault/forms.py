
from django import forms
from django.contrib.auth.models import User
from .models import Document, DocumentPermission


class DocumentUploadForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['title', 'file']


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
