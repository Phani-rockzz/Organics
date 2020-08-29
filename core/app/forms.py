from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Contact, CheckoutAddress
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
User = get_user_model()

from bootstrap_modal_forms.forms import BSModalModelForm
from django.contrib.auth import password_validation
from phonenumber_field.formfields import PhoneNumberField

class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    password1 = forms.CharField(label=_("Password"), strip=False,
    widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),

    )
    password2 = forms.CharField(
    label=_("Password confirmation"),
    widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
    strip=False,

    )


    class Meta:
        model = User
        fields = ["email", "password1", "password2", "name", 'phone']
        help_texts = {
            'password1': None,
            'password2': None,
        }


PAYMENT = (
    ('P', 'Paytm/Debit/Credit Card'),
    ('C', 'cod')
)


class CheckoutForm(forms.ModelForm):
    phone = PhoneNumberField(label='phone', required=True,
                             widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone...'}))
    address = forms.CharField(max_length=500, label="address", required=True,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter address..'}))
    city = forms.CharField(max_length=500, label="city", required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter city..'}))
    state = forms.CharField(max_length=500, label="state", required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter state..'}))
    zipcode = forms.CharField(label="address", required=True,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'zip code'}))
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT)

    class Meta:
        model = CheckoutAddress
        fields = ['phone', 'address', 'city', 'state', 'zipcode']


class ContactForm(forms.ModelForm):
    contact_name = forms.CharField(max_length=500, label="Name", required=True,
                                   widget=forms.TextInput(attrs={'placeholder': 'Enter name...'}))
    contact_email = forms.EmailField(max_length=500, label="Email", required=True,
                                     widget=forms.TextInput(attrs={'placeholder': 'Enter email...'}))
    contact_phone = PhoneNumberField(label='phone', required=True, widget=forms.NumberInput(attrs={'placeholder': 'Enter phone...'}))
    content = forms.CharField(label='message', widget=forms.Textarea(
                        attrs={'placeholder': 'Enter your message here...'}), required=True)
    class Meta:
        model = Contact
        fields =  ['contact_name', 'contact_email', 'contact_phone', 'content']



