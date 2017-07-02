from django import forms
from .models import Store, Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('author', 'star', 'taste_score', 'environment_score', 'service_score', 'content')


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ('name', 'phone_number', 'address')
