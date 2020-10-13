from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'app'

urlpatterns = [

    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('base_layout/', views.base_layout, name='base_layout'),
    path('signup/', views.register, name='signup'),
    path('signin/', auth_views.LoginView.as_view(template_name='app/login.html'), name='signin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('products/', views.ProductsView.as_view(), name='products'),
    path('product/<pk>/', views.ProductView.as_view(), name='product'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('profile/', views.user_profile, name='profile'),
    path('orders/', views.get_order, name='orders'),
    path('order-details/<pk>', views.get_order_details, name='details'),
    path('response/', views.response, name='response'),
    path('request/', views.paytm, name='request'),
    path('success/', views.success, name='success'),
    path('payu_success/', views.payu_success, name='payu_success'),
    path('failure/', views.payu_failure, name='failure'),
    path('payu_cash/', views.payu_cash, name='payu_cash'),
    path('payu_checkout/', views.payu_checkout, name='payu_checkout'),
    path('cash/', views.cash, name='cash'),
    path('add-to-cart/<pk>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<pk>/', views.remove_from_cart, name='remove-from-cart'),
    path('reduce-quantity-item/<pk>/', views.reduce_quantity_item, name='reduce-quantity-item'),
    path('search/', views.search.as_view(), name='search'),
    path('request-refund/', views.RequestRefundView.as_view(), name='request-refund'),
    path('dashboard/staff/home/', views.dashboard, name='dashboard'),
    path('dashboard/staff/order/<pk>', views.dashboard_order_details, name='dashboard_order_details'),
    path('dashboard/staff/failed_orders/', views.dashboard_failed, name='dashboard_failed'),
    path('dashboard/staff/failed_orders/<pk>', views.dashboard_failed_details, name='dashboard_failed_details'),
    path('dashboard/staff/contacts/', views.dashboard_contact, name='dashboard_contact'),
    path('dashboard/staff/contact_details/<pk>', views.dashboard_contact_details, name='dashboard_contact_details'),
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
            success_url=reverse_lazy('app:password_change_done')),
        name='change_password'),
    path('password_change_done/', views.password_change_done, name='password_change_done'),
    path('contact', views.contactview, name='contact')

]
