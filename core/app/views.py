from django.shortcuts import render, redirect, get_object_or_404, reverse
import json
from django.core import serializers
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .forms import ContactForm
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template


# Create your views here.

def home(request):
    return render(request, 'app/home.html')


def base_layout(request):
    return render(request, 'app/base.html')


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


def products(request):
    return render(request, 'app/products.html')


def search(request):
    return render(request, 'app/search.html')


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
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('app/contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['mekapotulaphani@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()


            return redirect('app:contact')

    return render(request, "app/contact.html", {'form': form_class})





