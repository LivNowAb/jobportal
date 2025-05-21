from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "index.html")

def ad_list(request):
    return render(request, "advertisment/index.html")

def client_list(request):
    return render(request, "client/index.html")