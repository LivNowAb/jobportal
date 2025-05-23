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

class AdDetail(ListView):
    model = Advertisement
    template_name = "advertisement/detail.html"
    context_object_name = 'ad_detail'