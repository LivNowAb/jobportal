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
from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.urls import path
from jobportal.views import home, AdDetail, AdsListView, RegistrationView, ClientProfileView, pricing_list, \
    CreateAd, ClientProfileCreation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('advertisement/detail/<int:pk>', AdDetail.as_view(), name='ad_detail'),
    path('advertisement/ads_list/', AdsListView.as_view(), name='ads_list'),
    path("login/", LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path( "password_change/", PasswordChangeView.as_view(template_name="registration/password_change.html"),
          name="password_change"),
    path("registration/client/profile", ClientProfileView.as_view(template_name="client/index.html"),
         name="client_reg_profile"),
    path("accounts/profile/", ClientProfileView.as_view(template_name="client/index.html"),
         name="client_log_profile"),
    # redirects to logged user profile
    path("accounts/profile/<int:pk>", ClientProfileView.as_view(template_name="client/index.html"),
         name="client_detail"),
    # redirects to any user profile with the corresponding pk
    path("pricing/", pricing_list, name="pricing"),
    path("create_ad/", CreateAd.as_view(template_name="advertisement/create.html"), name="ad_creation"),
    path("create_client/", ClientProfileCreation.as_view(template_name="client/create.html"),
         name="client_creation"),
    path("create_client/client/index/", ClientProfileView.as_view(template_name="client/index.html"))
    #TODO: OPRAVIT
]
