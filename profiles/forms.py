from allauth.account.forms import SignupForm
from django import forms
from ancillaries.models import Departments
from .models import *


class CustomSignupForm(SignupForm):
    """ Custom All auth Signup Form With Custom Fields """
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    department = forms.ModelChoiceField(queryset=Departments.objects.all(),
                                        required=True)
    user_type = forms.ModelChoiceField(queryset=UserTypes.objects.all(),
                                       required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        profile = UserProfile(
            user=user,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            department=self.cleaned_data['department'],
            user_type=self.cleaned_data['user_type'],
            phone_number=self.cleaned_data['phone_number'],
        )
        profile.save()
        return user

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone '
        'Number'


class BonusOrderForm(forms.ModelForm):
    """ Bonus Order Form """
    class Meta:
        model = UserBonusOrder
        fields = ['bonus']

    def __init__(self, *args, **kwargs):
        super(BonusOrderForm, self).__init__(*args, **kwargs)
        self.fields['bonus'].label = 'Bonus (Euros)'
