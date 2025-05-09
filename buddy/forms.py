from django import forms
from .models import Note, Event, Tag

class NoteForm(forms.ModelForm):
    event_text = forms.CharField(required=False, label='Event', widget=forms.TextInput(attrs={'placeholder': 'Enter or choose an event'}))
    tags_text = forms.CharField(required=False, label='Tags', widget=forms.TextInput(attrs={'placeholder': 'Comma-separated tags'}))

    class Meta:
        model = Note
        fields = ['title', 'event', 'transcript_text', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'transcript_text': forms.Textarea(attrs={'rows': 5}),
        }