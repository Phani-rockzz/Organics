from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
app_name = 'app'

urlpatterns = [

    path('', views.home,name='home'),
    path('base_layout/', views.base_layout, name='base_layout'),
    path('signup/', views.register, name='signup'),
    path('signin/', auth_views.LoginView.as_view(template_name='app/login.html'), name='signin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('products/', views.products, name='products'),
    path('search/', views.search, name='search'),
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

