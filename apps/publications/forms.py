from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file', 'is_public', 'topics']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.png,.jpg,.jpeg'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'topics': forms.SelectMultiple(attrs={'class': 'form-control'})
        }