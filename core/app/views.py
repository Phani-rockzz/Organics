from django.shortcuts import render, redirect, get_object_or_404, reverse
import json
from django.core import serializers
from django.conf import settings
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect, request
from .forms import ContactForm, CheckoutForm, RefundForm, OrderForm
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import get_template
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, CheckoutAddress, Payment, User, PaytmHistory, Contact, Refund
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity, TrigramDistance
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse  # new
from django.views.decorators.csrf import csrf_exempt  # new
from django.template.loader import render_to_string
from . import checksum
from django.core.mail import send_mail
from .utils import VerifyPaytmResponse
user = settings.AUTH_USER_MODEL


# Create your views here.
class Home(ListView):
    model = Item
    queryset = Item.objects.all()
    template_name = 'app/home.html'


class ProductsView(ListView):
    model = Item
    queryset = Item.objects.all()
    template_name = 'app/products.html'


class ProductView(DetailView):
    model = Item
    template_name = "app/product.html"

def about(request):
    return render(request, 'app/about.html')

@login_required
def user_profile(request):
    order = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'app/profile.html', {'data': order})

@login_required
def get_order(request):
    order = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'app/orders.html', {'data': order})

def password_change_done(request):
    return render(request, 'app/password_change_done.html')

@login_required
def get_order_details(request, pk):
    address = CheckoutAddress.objects.filter(user=request.user, pk=pk)
    payment = Payment.objects.filter(user=request.user, pk=pk)
    order = Order.objects.filter(user=request.user, pk=pk).prefetch_related('items').select_related('address').select_related('payment')

    return render(request, 'app/order_details.html', {'object': order, 'object1': address, 'object2': payment})

@login_required
def order_update(request, pk):

    if request.user.is_superuser:
        form = get_object_or_404(Order, pk=pk)
    else:
        form = get_object_or_404(Order, pk=pk, user=request.user)
    form = OrderForm(request.POST or None, instance=form)
    if form.is_valid():
        form.save()
        return redirect('app:dashboard')
    return render(request, 'app/dashboard_order_update.html', {'form': form})


@login_required
def order_delete(request, pk):

    if request.user.is_superuser:
        post = get_object_or_404(Order, pk=pk)
    else:
        post = get_object_or_404(Order, pk=pk, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('app:dashboard')
    return render(request, 'app/dashboard_order_delete.html', {'object': post})




class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'app/order-summary.html', context)

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order", extra_tags='alert alert-error')
            return redirect("/")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': form,
            'order': order
        }
        return render(self.request, 'app/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)


            if form.is_valid():
                name = form.cleaned_data.get('name')
                phone = form.cleaned_data.get('phone')
                address = form.cleaned_data.get('address')
                city = form.cleaned_data.get('city')
                district = form.cleaned_data.get('district')
                state = form.cleaned_data.get('state')
                zipcode = form.cleaned_data.get('zipcode')
                # TODO: add functionaly for these fields
                # same_billing_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                checkout_address = CheckoutAddress(
                    user=self.request.user,
                    name=name,
                    phone=phone,
                    address=address,
                    city=city,
                    district=district,
                    state=state,
                    zipcode=zipcode
                )
                checkout_address.save()
                order.address = checkout_address
                order.save()

                if payment_option == 'P':
                    return redirect('app:cash')
                elif payment_option == 'C':
                    order_id = checksum.__id_generator__()
                    payment = Payment.objects.create(user=self.request.user, amount=order.total())
                    payment.user = order.user
                    payment.txn_id = order_id
                    payment.offline = True
                    payment.paid = False
                    payment.save()
                    order.ordered = True
                    order.order_id = order_id
                    order.payment = payment
                    order.save()
                    subject = "Order Confirmation from Farmway Organics"
                    message = 'Dear {}, \n\nYou have successfully placed an order.\
                            Your order id is {}. We will deliver your happiness as soon as possible thank you for shopping with us'.format(order.user.name, order.order_id)

                    send_mail(
                        subject,
                        message,
                        'phanigoud123@gmail.com',
                        [order.user.email],
                        fail_silently=False,
                    )
                    messages.success(self.request, "Thank u, Your order was successful", extra_tags='alert '
                                                                                                    'alert-success')
                    return redirect('app:success')
                elif payment_option == 'D':
                    return redirect('app:payu_cash')
                else:
                    messages.warning(self.request, "Invalid payment option", extra_tags='alert alert-warning')
                    return redirect("app:checkout", {'order': order})
            else:

                print(form.errors)
                messages.error(self.request, 'Sorry, Something went wrong!', extra_tags='alert alert-error')
                return redirect("app:checkout")

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("app:order-summary")


@csrf_exempt
def response(request):
    order = Order.objects.filter(ordered=False).first()
    payment = Payment.objects.filter(paid=False, offline=True)

    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]
        verify = checksum.verifySignature(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            for p in payment:
                p.paid = True
                p.offline = False
                p.save()

            order.ordered = True
            order.mode = True
            order.payment = p

            order.save()
            subject = "Order Confirmation from Farmway Organics"
            message = 'Dear {}, \n\nYou have successfully placed an order.\
                                        Your order id is {}. We will deliver your happiness as soon as possible thank you for shopping with us'.format(
                order.user.name, order.order_id)

            send_mail(
                subject,
                message,
                'phanigoud123@gmail.com',
                [order.user.email],
                fail_silently=False,
            )
#            PaytmHistory.objects.create(user=order.user, **data_dict)
            return render(request, "app/response.html", {"paytm": data_dict})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)

@login_required
def paytm(request):
    order = Order.objects.get(user=request.user, ordered=False)

    order_id = checksum.__id_generator__()
    bill_amount = order.total()
    if bill_amount:
        data_dict = {
            'MID': settings.PAYTM_MERCHANT_ID,
            'ORDER_ID': order_id,
            'TXN_AMOUNT': bill_amount,
            'CUST_ID': order.user.id,
            'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
            'WEBSITE': settings.PAYTM_WEBSITE,
            'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
            'CALLBACK_URL':settings.PAYTM_CALLBACK_URL,

        }
        param_dict = data_dict
        param_dict['CHECKSUMHASH'] = checksum.generateSignature(data_dict, settings.PAYTM_MERCHANT_KEY)
        payment = Payment.objects.create(user=request.user, amount=order.total())
        payment.checksum = param_dict['CHECKSUMHASH']
        payment.txn_id = order_id
        payment.user = order.user
        payment.save()
        order.payment = payment
        order.order_id = order_id
        order.save()
        context = {
            'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
            'company_name': settings.PAYTM_COMPANY_NAME,
            'paytmdict': param_dict,
        }
        return render(request, "app/request.html", context)
    return HttpResponse("Bill Amount Could not find. ?bill_amount")


from paywix.payu import Payu

payu_config = settings.PAYU_CONFIG
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')

# Create Payu Object for making transaction
# The given arguments are mandatory
payu = Payu(merchant_key, merchant_salt, surl, furl, mode)


# Payu checkout page
@csrf_exempt
@login_required
def payu_checkout(request):

    address = CheckoutAddress.objects.filter(user=request.user)
    order = Order.objects.get(user=request.user, ordered=False)
    order_id = checksum.__id_generator__()
    bill_amount = order.total()


    # The dictionary data  should be contains following details
    data = {'amount': bill_amount,
            'firstname': order.user.name,
            'email': order.user.email,
            'phone': order.user.phone, 'productinfo': 'organic fertilizer',
            'lastname': 'user', 'address1': order.address.phone,
            'address2': order.address.address, 'city': order.address.city,
            'state': order.address.state, 'country': 'india',
            'zipcode': order.address.zipcode, 'udf1': '',
            'udf2': '', 'udf3': '', 'udf4': '', 'udf5': ''
    }

    # No Transactio ID's, Create new with paywix, it's not mandatory
    # Create your own
    # Create transaction Id with payu and verify with table it's not existed
    payment = Payment.objects.create(user=request.user, amount=order.total())

    payment.txn_id = order_id
    payment.user = order.user
    payment.save()
    order.payment = payment
    order.order_id = order_id
    order.save()
    txnid = order_id
    data.update({"txnid": txnid})
    payu_data = payu.transaction(**data)
    return render(request, 'app/payu_checkout.html', {"posted": payu_data})


@csrf_exempt
def payu_success(request):
    order = Order.objects.filter(ordered=False).first()
    payment = Payment.objects.filter(paid=False)

    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    if response['return_data']['status'] == 'success':
        for p in payment:

            p.paid = True
            p.offline = False
            p.save()
        order.payment = p
        order.ordered = True
        order.mode = True
        order.save()
        subject = "Order Confirmation from Farmway Organics"
        message = 'Dear {}, \n\nYou have successfully placed an order.\
                                    Your order id is {}. We will deliver your happiness as soon as possible thank you for shopping with us'.format(
            order.user.name, order.order_id)

        send_mail(
            subject,
            message,
            'phanigoud123@gmail.com',
            [order.user.email],
            fail_silently=False,
        )

    return render(request, 'app/payu_success.html', {'response': response})

@csrf_exempt
def payu_failure(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    return render(request, 'app/failure.html', {'response': response})

@login_required
def payu_cash(request):
    order = Order.objects.get(user=request.user, ordered=False)
    context = {'order': order}

    return render(request, 'app/payu_cash.html', context)


@login_required
def cash(request):
    order = Order.objects.get(user=request.user, ordered=False)
    context = {'order': order}

    return render(request, 'app/cashfree.html', context)


def base_layout(request):
    return render(request, 'app/base.html')


def success(request):
    return render(request, 'app/success.html')


def register(request):
    registered = False
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            form.save()

            registered = True
            messages.success(request, 'Thank you! Your Account Was Successfully Created.',
                             extra_tags='alert alert-success')
            return redirect('app:signup')
        else:
            print(form.errors)
            messages.warning(request, 'Sorry, Something went wrong!', extra_tags='alert alert-warning')

    else:
        form = RegisterForm()

    return render(request, 'app/signup.html',
                  {'form': form, 'registered': registered})


class search(ListView):
    model = Item
    template_name = 'app/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            object_list = Item.objects.annotate(search=SearchVector('item_name', weight='A') + SearchVector(
                'category', weight='B'), ).filter(search=SearchQuery(query)).distinct('item_name', 'category')
            return object_list
        else:
            response = HttpResponse('Sorry! no data found.')
            return response


class DashboardSearch(ListView):
    model = Order
    template_name = 'app/dashboard_search.html'

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            object_list = Order.objects.annotate(search=SearchVector('order_id', weight='A') + SearchVector(
                'user', weight='B'), ).filter(search=SearchQuery(query)).distinct('order_id', 'user')
            return object_list
        else:
            response = HttpResponse('Sorry! no data found.')
            return response


from django.core.mail import send_mail


def contactview(request):
    form_class = ContactForm
    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
                , '')
            contact_email = request.POST.get(
                'contact_email'
                , '')
            contact_phone = request.POST.get(
                'contact_phone'
                , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('app/contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'contact_phone': contact_phone,
                'form_content': form_content,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Farmway Organics" + ' ',
                ['mekapotulaphani@gmail.com'],
                headers={'Reply-To': contact_email}
            )
            email.send()
            form.save()
            messages.success(request, 'Thank you! Your request Was Successfully Created.',
                             extra_tags='alert alert-success')
            return redirect('app:contact')
    return render(request, "app/contact.html", {'form': form_class})


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added quantity Item", extra_tags='alert alert-info')
            return redirect("app:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart", extra_tags='alert alert-info')
            return redirect("app:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart", extra_tags='alert alert-info')
        return redirect("app:order-summary")


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            messages.info(request, "Item \"" + order_item.item.item_name + "\" remove from your cart",
                          extra_tags='alert alert-info')
            return redirect("app:order-summary")
        else:
            messages.info(request, "This Item not in your cart", extra_tags='alert alert-info')
            return redirect("app:product", pk=pk)
    else:
        # add message doesnt have order
        messages.warning(request, "You do not have an Order", extra_tags='alert alert-info')
        return redirect("app:product", pk=pk)


@login_required
def reduce_quantity_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "Item quantity was updated", extra_tags='alert alert-info')
            return redirect("app:order-summary")
        else:
            messages.info(request, "This Item not in your cart", extra_tags='alert alert-info')
            return redirect("app:order-summary")
    else:
        # add message doesnt have order
        messages.info(request, "You do not have an Order", extra_tags='alert alert-info')
        return redirect("app:order-summary")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "app/request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            order_id = form.cleaned_data.get('order_id')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(order_id=order_id)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("app:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("app:request-refund")


@login_required
def dashboard(request):
    order = Order.objects.all().order_by('-ordered_date')
    return render(request, 'app/dashboard.html', {'order': order})


@login_required
def dashboard_order_details(request, pk):
    order = Order.objects.filter(pk=pk).order_by('-ordered_date')
    return render(request, 'app/dashboard_order_details.html', {'object': order})


@login_required
def dashboard_failed(request):
    order = Order.objects.all().order_by('-ordered_date')
    return render(request, 'app/dashboard_failed.html', {"object": order})


@login_required
def dashboard_failed_details(request, pk):
    order = Order.objects.filter(pk=pk).order_by('-ordered_date')
    return render(request, 'app/dashboard_order_details.html', {'object': order})

@login_required
def dashboard_contact(request):
    contact = Contact.objects.all()
    return render(request, 'app/dashboard_contacts.html', {'contact': contact})

@login_required
def dashboard_contact_details(request, pk):
    contact = Contact.objects.filter(pk=pk)
    return render(request, 'app/dashboard_contact_details.html', {'contact': contact})