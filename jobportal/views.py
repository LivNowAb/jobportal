from django.shortcuts import render
from django.views.generic import DetailView, ListView

from jobportal.models import Advertisement


# Create your views here.
def home(request):
    return render(request, "index.html")

def ad_list(request):
    return render(request, "advertisement/index.html")

def client_list(request):
    return render(request, "client/index.html")

class AdsListView(ListView):
    model = Advertisement
    template_name = "advertisement/ads_list.html"
    context_object_name = 'ads_list'
