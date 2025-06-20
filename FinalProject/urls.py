"""
URL configuration for FinalProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)

from FinalProject import settings
from jobportal.views import (
    AdDetail, AdsListView, RegistrationView, ClientProfileView, pricing_list, \
    CreateAd, ContactListView, PaymentView, PaymentSuccessView, ResponseDetailView,
    ResponseDeleteView, AdvertisementUpdateView, \
    ClientAdvertisementDetailView, AdvertisementDeleteView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AdsListView.as_view(), name="home"),
    path('advertisement/detail/<int:pk>', AdDetail.as_view(), name='ad_detail'),

    path("login/", LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("password_change/", PasswordChangeView.as_view(
        template_name="registration/pwrd_change.html"), name="password_change"),
    path("password_change/done/", PasswordChangeDoneView.as_view(
        template_name="registration/pwrd_change_done.html"), name="password_change_done"),
    path("password_reset/", PasswordResetView.as_view(
        template_name="registration/pwrd_reset_form.html"), name="password_reset"),
    path("password_reset/done/", PasswordResetDoneView.as_view(
        template_name="registration/pwrd_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(
        template_name="registration/pwrd_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", PasswordResetCompleteView.as_view(
        template_name="registration/pwrd_reset_complete.html"), name="password_reset_complete"),
    path("registration/client/profile", ClientProfileView.as_view(template_name="client/index.html"),
         name="client_reg_profile"),
    path("accounts/profile/", ClientProfileView.as_view(template_name="client/index.html"),
         name="client_log_profile"),
    # redirects to currently logged  user
    path("accounts/profile/<int:pk>", ClientProfileView.as_view(template_name="client/index.html"),
         name="client_detail"),
    # redirects to any existing user with the given pk
    path("pricing/", pricing_list, name="pricing"),
    path("create_ad/", CreateAd.as_view(template_name="advertisement/create.html"), name="ad_creation"),
    path("contacts/", ContactListView.as_view(template_name="contacts/index.html"),
         name="contacts"),
    path("payment/<int:pk>", PaymentView.as_view(template_name="payment_mock/payment.html"), name='payment'),
    path("payment/success", PaymentSuccessView.as_view(template_name="payment_mock/payment_success.html"),
        name="payment_success"),
    path("contacts/", ContactListView.as_view(template_name="contacts/index.html"), name="contacts"),
    path('response/<int:pk>/', ResponseDetailView.as_view(), name='response_detail'),
    path('response/<int:pk>/delete/', ResponseDeleteView.as_view(), name='response_delete'),
    path('advertisement/<int:pk>/edit/', AdvertisementUpdateView.as_view(), name='advertisement_edit'),
    path("client/advertisement/<int:pk>/", ClientAdvertisementDetailView.as_view(),
         name="client_advertisement_detail"),
    path('advertisement/<int:pk>/delete/', AdvertisementDeleteView.as_view(), name='advertisement_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)