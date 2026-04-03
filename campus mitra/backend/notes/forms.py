from django import forms
from .models import Note


class NoteUploadForm(forms.ModelForm):
    class Meta:
        model  = Note
        fields = ['title', 'subject', 'file', 'description']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Note title'}),
            'subject':     forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'file':        forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.ppt,.pptx,.doc,.docx'}),
        }
