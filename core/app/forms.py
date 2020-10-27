from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Contact, CheckoutAddress, Order
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
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    phone = PhoneNumberField(widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))


    class Meta:
        model = User
        fields = ["email", "password1", "password2", "name", 'phone']
        help_texts = {
            'password1': None,
            'password2': None,
        }


PAYMENT = (
    ('P', 'Paytm/Debit/Credit card'),
    ('C', 'cod(Cash On Delivery)'),
    ('D', 'Debit/Credit card/UPI')
)


class OrderForm(forms.ModelForm):
    being_delivered = forms.RadioSelect()
    received = forms.RadioSelect()
    refund_requested = forms.RadioSelect()
    refund_granted = forms.RadioSelect()

    class Meta:
        model = Order
        fields = ['being_delivered', 'received', 'refund_requested', 'refund_granted']

class CheckoutForm(forms.ModelForm):
    name = forms.CharField(max_length=500, label="Name:", required=True,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter name..'}))
    phone = PhoneNumberField(label='Phone Number:', required=True,
                             widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone...'}))
    address = forms.CharField(max_length=500, label="Address", required=True,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter address..'}))
    city = forms.CharField(max_length=500, label="City", required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter city..'}))
    district = forms.CharField(max_length=500, label="District", required=True,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter district..'}))
    zipcode = forms.CharField(label="address", required=True,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'zip code'}))
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT)

    class Meta:
        model = CheckoutAddress
        fields = ['name', 'phone', 'address', 'city', 'district', 'state', 'zipcode']


class ContactForm(forms.ModelForm):
    contact_name = forms.CharField(max_length=500, required=True, label="Name:",
                                   widget=forms.TextInput(attrs={'placeholder': 'Enter name...'}))
    contact_email = forms.EmailField(max_length=500, required=True, label="Email:",
                                     widget=forms.TextInput(attrs={'placeholder': 'Enter email...'}))
    contact_phone = PhoneNumberField( required=True, label='Phone Number:', widget=forms.NumberInput(attrs={'placeholder': 'Enter phone...'}))
    content = forms.CharField(required=True, label='Message:', widget=forms.Textarea(
                        attrs={'placeholder': 'Enter your message here...'}), )
    class Meta:
        model = Contact
        fields =  ['contact_name', 'contact_email', 'contact_phone', 'content']


class RefundForm(forms.Form):
    order_id = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()
