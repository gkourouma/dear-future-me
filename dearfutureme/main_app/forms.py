from django import forms
from .models import Capsule
from .models import Memory


class CapsuleForm(forms.ModelForm):
    class Meta:
        model = Capsule
        fields = ['title', 'content', 'cover_image', 'open_date']
        widgets = {
            'open_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'title': 'Capsule Title',
            'content': 'Capsule Content',
            'cover_image': 'Upload Cover Image',
            'open_date': 'Select Open Date',
        }
        help_texts = {
            'title': 'Enter a title for your capsule.',
            'content': 'Write the content of your capsule here.',
            'cover_image': 'Optional: Upload an image for your capsule cover.',
            'open_date': 'Choose the date when this capsule will be opened.',
        }
        error_messages = {
            'title': {
                'required': 'This field is required.',
                'max_length': 'Title is too long. Max 255 characters.',
            },
            'open_date': {
                'invalid': 'Enter a valid date.',
            },
        }


class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ['title','content','date_taken', 'image', 'video', 'audio']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Memory Title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write about your memory here...'}),
            'date_taken': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Date Taken'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*', 'placeholder': 'Upload an Image'}),
            'video': forms.ClearableFileInput(attrs={'accept': 'video/*', 'placeholder': 'Upload a Video'}),
            'audio': forms.ClearableFileInput(attrs={'accept': 'audio/*', 'placeholder': 'Upload Audios'}),
        }
        labels = {
            'title': 'Memory Title',
            'content': 'Your Story',
            'date_taken': 'Date Taken',
            'image': 'Upload Images',
            'video': 'Upload Videos',
            'audio': 'Upload Audios',
        }
