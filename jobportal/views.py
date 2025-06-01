from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, FormView, TemplateView, CreateView

from jobportal.forms import RegistrationForm, ResponseForm, AdCreation, ClientCreation
from jobportal.models import Advertisement, Client


# Create your views here.
def home(request):
    return render(request, "index.html")

def ad_list(request):
    return render(request, "advertisement/index.html")

def client_list(request):
    return render(request, "client/index.html")

def pricing_list(request):
    return render(request, "pricing.html")


class AdDetail(DetailView):
    model = Advertisement
    template_name = "advertisement/detail.html"
    context_object_name = 'ad_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'submitted' in self.request.GET:
            context['form_submitted'] = True
        else:
            context['form_submitted'] = False
            context['form'] = ResponseForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ResponseForm(request.POST, request.FILES)
        if form.is_valid():
            response = form.save(commit=False)
            response.advertisement = self.object
            response.save()
            return redirect(f'{self.request.path}?submitted=True')
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)


class AdsListView(ListView):
    model = Advertisement
    template_name = "advertisement/ads_list.html"
    context_object_name = 'ads_list'


class RegistrationView(FormView):
    template_name = "registration/registration.html"
    form_class = RegistrationForm
    success_url = "client/profile"

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


class ClientProfileCreation(PermissionRequiredMixin, CreateView):
    template_name = "client/create.html"
    form_class = ClientCreation
    success_url = "client/index.html"
    permission_required = ""



# class ClientProfileView(DetailView):
#     model = Client
#     template_name = "client/index.html"
#     context_object_name = 'client_detail'


class ClientProfileView(TemplateView):
    model = Client
    template_name = "client/index.html"
    context_object_name = 'client_detail'

    def get_context_data(self, **kwargs):
        context = super(ClientProfileView, self).get_context_data(**kwargs)
        context['client_detail'] = Client.objects.get(user=self.request.user)
        return context
        # fetches Client object that is linked to currently logged user


#TODO: CreateAd OPRAVIT
class CreateAd(PermissionRequiredMixin, CreateView):
     template_name = "advertisement/create.html"
     form_class= AdCreation
     success_url = "ads_list"
     permission_required = ""

     def post(self, request, *args, **kwargs):
         form = AdCreation(request.POST, request.FILES)
         if form.is_valid():
             try:
                 client = Client.objects.get(user=request.user)
             except Client.DoesNotExist:
                 return self.render_to_response(
                     self.get_context_data(form=form, error="Váš přihlášený účet není spojený s žádným podnikem - nelze publikovat inzerát.")
                 )
             ad = form.save(commit=False)
             ad.client = client
             ad.save()
             return redirect(f'{self.request.path}?submitted=True')
         else:
             return self.form_invalid(form) #NEFUNGUJE