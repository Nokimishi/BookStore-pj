from django import forms
from book_store3.models import UserProfile

class UserProfileForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = UserProfile
        fields = ['image', 'dob', 'address']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
