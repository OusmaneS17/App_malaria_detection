# malaria_app/forms.py

from django import forms
from .models import MalariaImage

class MalariaImageForm(forms.ModelForm):
    class Meta:
        model = MalariaImage
        fields = ['paatient_name', 'noteMedical', 'image']
        labels = {
            'paatient_name': 'Nom complet du patient',
            'noteMedical': 'Notes médicales supplémentaires',
            'image': 'Image à analyser'
        }
        widgets = {
            'noteMedical': forms.Textarea(attrs={'rows': 3}),
        }