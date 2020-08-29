from django.shortcuts import render, redirect, get_object_or_404, reverse
import json
from django.core import serializers
from django.conf import settings
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect, request
from .forms import ContactForm, CheckoutForm
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, CheckoutAddress, Payment
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


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'app/order-summary.html', context)

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
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
                phone = form.cleaned_data.get('phone')
                address = form.cleaned_data.get('address')
                city = form.cleaned_data.get('city')
                state = form.cleaned_data.get('state')
                zipcode = form.cleaned_data.get('zipcode')
                # TODO: add functionaly for these fields
                # same_billing_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                checkout_address = CheckoutAddress(
                    user=self.request.user,
                    phone=phone,
                    address=address,
                    city=city,
                    state=state,
                    zipcode=zipcode
                )
                checkout_address.save()
                order.checkout_address = checkout_address
                order.save()

                if payment_option == 'P':
                    return redirect('app:cash')
                elif payment_option == 'C':
                    order.ordered = True
                    order.save()
                    messages.success(self.request, "Thank u, Your order was successful", extra_tags='alert '
                                                                                                    'alert-success')
                    return redirect('app:success')
                else:
                    messages.warning(self.request, "Invalid payment option", extra_tags='alert alert-warning')
                    return redirect("app:checkout")
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
    payment = Payment.objects.filter(paid=False)
    resp = VerifyPaytmResponse(request)
    if resp['verified']:

        for p in payment:
            p.user = order.user
            p.paid = True
            p.save()

        order.ordered = True
        order.order = payment
        order.save()

        return HttpResponse('<html><center><h1 class="text-green">Transaction Successful</h1><br> '
                            '<h4>Keep Shopping with us.</h4></center></html>', status=200)
    else:
        # check what happened; details in resp['paytm']

        #data = {'details': resp['paytm']['ORDERID'], 'txn': resp['paytm']['TXNID'], 'status': resp['paytm']['STATUS']}
        #return HttpResponse(json.dumps(data), content_type='application/json', status=400)
        return HttpResponse('<html><center><h1 class="text-green">Transaction Failed</h1><br></center></html>', status=400)

def paytm(request):
    order = Order.objects.get(user=request.user, ordered=False)
    payment = Payment.objects.create(user=request.user, amount=order.get_total_price())
    payment.save()
    order_id = checksum.__id_generator__()
    bill_amount = order.total()
    data_dict = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
        'WEBSITE': settings.PAYTM_WEBSITE,
        'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
        'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,
        'MOBILE_NO': order.user.phone,
        'EMAIL': order.user.email,
        'CUST_ID': order.user.id,
        'ORDER_ID': order_id,
        'TXN_AMOUNT': bill_amount,
    }  # This data should ideally come from database
    data_dict['CHECKSUMHASH'] = checksum.generateSignature(data_dict, settings.PAYTM_MERCHANT_KEY)
    payment.checksum = data_dict['CHECKSUMHASH']
    payment.txn_id = order_id
    payment.save()
    context = {
        'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
        'company_name': settings.PAYTM_COMPANY_NAME,
        'data_dict': data_dict
    }
    return render(request, 'app/request.html', context)


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
            messages.success(request, 'Thank you! Your Account Was Successfully Created!',
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
                "Your website" + ' ',
                ['mekapotulaphani@gmail.com'],
                headers={'Reply-To': contact_email}
            )
            email.send()
            form.save()
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
            messages.info(request, "Added quantity Item")
            return redirect("app:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart")
            return redirect("app:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart")
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
            messages.info(request, "Item \"" + order_item.item.item_name + "\" remove from your cart")
            return redirect("app:order-summary")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("app:product", pk=pk)
    else:
        # add message doesnt have order
        messages.info(request, "You do not have an Order")
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
            messages.info(request, "Item quantity was updated")
            return redirect("app:order-summary")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("app:order-summary")
    else:
        # add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("app:order-summary")
