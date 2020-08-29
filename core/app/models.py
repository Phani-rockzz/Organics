from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import User

from datetime import date
from decimal import Decimal
from email.mime.application import MIMEApplication
from django.conf import settings

from django.template.loader import render_to_string, get_template
from django.template import TemplateDoesNotExist, Context
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from io import StringIO
from django.conf import settings as app_settings


# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """creates and saves a new user"""
        if not email:
            raise ValueError('users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that supports email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'


# products
class Item(models.Model):
    item_name = models.CharField(max_length=255)

    category = models.CharField(max_length=255)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True, editable=True, default='images/blog-default.jpg')

    description = models.TextField()
    usage = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse("app:product", kwargs={
            "pk": self.pk

        })

    def get_add_to_cart_url(self):
        return reverse("app:add-to-cart", kwargs={
            "pk": self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("app:remove-from-cart", kwargs={
            "pk": self.pk
        })

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url





class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_discount_item_price()




    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_item_price()

        return self.get_total_item_price()




class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True, null=True)
    ordered_date = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey(
        'CheckoutAddress', on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.email

    def get_min_amount(self):
        return int(999)

    def shipping_price(self):
        return 40


    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def total(self):
        total = 0
        if self.get_total_price() < self.get_min_amount():
            total += self.get_total_price() + self.shipping_price()
        else:
            total += self.get_total_price()
        return total



# address
class CheckoutAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = PhoneNumberField(null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class Contact(models.Model):
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField(max_length=100)
    contact_phone = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.contact_name


class Payment(models.Model):
    txn_id = models.CharField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    checksum = models.CharField(max_length=255, null=True, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email



