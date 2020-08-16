from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'app'

urlpatterns = [

    path('', views.home, name='home'),
    path('base_layout/', views.base_layout, name='base_layout'),
    path('signup/', views.register, name='signup'),
    path('signin/', auth_views.LoginView.as_view(template_name='app/login.html'), name='signin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('products/', views.ProductsView.as_view(), name='products'),
    path('product/<pk>/', views.ProductView.as_view(), name='product'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('response/', views.response, name='response'),
    path('request/', views.paytm, name='request'),
    path('success/', views.success, name='success'),
    path('cash/', views.cash, name='cash'),
    path('add-to-cart/<pk>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<pk>/', views.remove_from_cart, name='remove-from-cart'),
    path('reduce-quantity-item/<pk>/', views.reduce_quantity_item, name='reduce-quantity-item'),
    path('search/', views.search.as_view(), name='search'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='app/password_reset_form.html',
             subject_template_name='app/password_reset_subject.txt',
             email_template_name='app/password_reset_email.html',
             success_url=reverse_lazy('app:password_reset_done')
         ),
         name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'
                                                                          ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('app:password_reset_complete')),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='app/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='app/password_change.html',
            success_url='app/password_change_done.html'
        ),
        name='change_password'
    ),
    path('contact', views.contactview, name='contact')

]
