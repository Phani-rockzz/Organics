from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models
from django.utils.translation import gettext as _
from .models import Item, Order, OrderItem, CheckoutAddress, Contact, Payment, PaytmHistory, Refund
from django.urls import path

# Register your models here.
def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'address',
                    'payment',

                    ]
    list_display_links = [
        'user',
        'address',
        'payment',


    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__email',
        'order_no'
    ]
    actions = [make_refund_accepted]


class PaytmHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'MID', 'TXNAMOUNT', 'STATUS')


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'phone']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'phone')}),
        (_('Permissions'),
         {'fields': ('is_active', 'is_staff', 'is_superuser')}
         ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'phone')
        }),
    )

admin.site.register(models.User, UserAdmin)
admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(CheckoutAddress)
admin.site.register(Contact)
admin.site.register(Payment)
admin.site.register(PaytmHistory, PaytmHistoryAdmin)
admin.site.register(Refund)