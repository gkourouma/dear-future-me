from django import forms
from django.core.exceptions import ValidationError
from .models import Profile
from .models import Capsule
from .models import Memory
from .models import Comment


class CapsuleForm(forms.ModelForm):
    class Meta:
        model = Capsule
        fields = ['title', 'content', 'cover_image', 'is_locked', 'open_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a title for your album'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write about your album here...'}),
            'cover_image': forms.ClearableFileInput(attrs={'accept': 'image/*', 'placeholder': 'Upload an Image'}),
            'is_locked': forms.CheckboxInput(attrs={'placeholder': 'Lock Album'}),
            'open_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'title': 'Album Title',
            'content': 'Album Content',
            'cover_image': 'Upload Cover Image',
            'open_date': 'Open Date',
            'is_locked': 'Lock Album?',
        }
        help_texts = {
            'cover_image': 'Optional: Upload an image for your album cover.',
            'open_date': 'If locked, Choose the date when this album will be opened.',
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

    def clean(self):
        cleaned = super().clean()
        locked    = cleaned.get('is_locked')
        open_date = cleaned.get('open_date')

        if locked and not open_date:
            self.add_error('open_date',
                "You must specify an open date if you lock this capsule."
            )
        return cleaned


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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Tell us about yourself...'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
