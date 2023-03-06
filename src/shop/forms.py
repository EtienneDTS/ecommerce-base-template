from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Review
        fields = ('rating', 'text',)