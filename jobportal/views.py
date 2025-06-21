from datetime import timedelta

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView, DeleteView

from jobportal.forms import RegistrationForm, ResponseForm, AdCreation, ClientCreation, PaymentForm
from jobportal.models import Advertisement, Client, Contacts, Response, Region, District, Position


# Create your views here.
def home(request):
    return render(request, "index.html")


def pricing_list(request):
    return render(request, "pricing.html")


class AdDetail(DetailView):
    model = Advertisement
    template_name = "advertisement/detail.html"
    context_object_name = 'ad_detail'

    def get_queryset(self):
        return super().get_queryset().select_related('client')  # select_related() offers better performance
        # super() calls parent class and overrides default method

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'submitted' in self.request.GET:
            context['form_submitted'] = True
        else:
            context['form_submitted'] = False
            context['form'] = ResponseForm()
        return context  # displays a blank form if submitted is False

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ResponseForm(request.POST, request.FILES)
        if form.is_valid():
            response = form.save(commit=False)
            response.advertisement = self.object  # links response to advertisement
            response.save()
            return redirect(f'{self.request.path}?submitted=True')
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)


class AdsListView(ListView):
    model = Advertisement
    template_name = "index.html"
    context_object_name = 'home'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('client__district__region_id', 'position') # filter

        cutoff_date = timezone.now() - timedelta(days=14) # expiring ads older than 14 days
        queryset = queryset.filter(published_date__gte=cutoff_date)

        queryset = queryset.filter(published=True) # displays only paid for ads

        region = self.request.GET.get('region') # filtering options
        district = self.request.GET.get('district')
        position = self.request.GET.get('position')

        if region:
            queryset = queryset.filter(client__district__region_id=region)
        if district:
            queryset = queryset.filter(client__district_id=district)
        if position:
            queryset = queryset.filter(position=position)
            # applies filters based on user input

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()
        context['positions'] = Position.objects.all() # populates filter dropdowns

        query = self.request.GET.copy() #pagination
        query.pop('page', None)
        context['query_string'] = query.urlencode()

        return context


class RegistrationView(View):
    def get(self, request):
        user_form = RegistrationForm()
        client_form = ClientCreation()
        return render(request, "registration/registration.html", {
            "user_form": user_form,
            "client_form": client_form
        })

    def post(self, request):
        user_form = RegistrationForm(request.POST)
        client_form = ClientCreation(request.POST, request.FILES)

        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()  # saves User to DB

            login(request, user)  # cancels previous session and logs in newly created user

            client = client_form.save(commit=False)
            client.user = user
            client.save()  # saves Client model to DB

            return redirect("client_log_profile")
        else:
            return render(request, "registration/registration.html", {
                "user_form": user_form,
                "client_form": client_form
            })


class ClientProfileView(TemplateView):
    model = Client
    template_name = "client/index.html"
    context_object_name = 'client_detail'

    class Meta:
        ordering = ['-published_date']

    def get_context_data(self, **kwargs):
        context = super(ClientProfileView, self).get_context_data(**kwargs)
        context['client_detail'] = Client.objects.get(user=self.request.user)
        return context  # fetches Client object that is linked to currently logged user


class ClientAdvertisementDetailView(DetailView):
    model = Advertisement
    template_name = 'advertisement/client_advertisement_detail.html'
    context_object_name = 'advertisement'

    def get_queryset(self):
        return Advertisement.objects.filter(client__user=self.request.user)


class ResponseDetailView(DetailView):
    model = Response
    template_name = 'response/detail.html'
    context_object_name = 'response'


class ResponseDeleteView(DeleteView):
    model = Response
    template_name = 'response/delete.html'
    success_url = reverse_lazy("client_log_profile")


class CreateAd(LoginRequiredMixin, CreateView):
    model = Advertisement
    template_name = "advertisement/create.html"
    form_class = AdCreation

    def form_valid(self, form):
        client = Client.objects.get(user=self.request.user)
        form.instance.created_by = self.request.user
        form.instance.client = client  # user and client model must match ad author
        form.instance.published = False  # saves as draft, payment must go through before publishing
        self.object = form.save()

        return redirect('payment', pk=self.object.id)


class AdvertisementUpdateView(UpdateView):
    model = Advertisement
    fields = ['title', 'text_content', 'position', 'salary']
    template_name = 'advertisement/edit.html'

    def get_success_url(self):
        return reverse('client_advertisement_detail', kwargs={'pk': self.object.pk})
        # self.object is the ad currently being edited


class AdvertisementDeleteView(DeleteView):
    model = Advertisement
    template_name = 'advertisement/delete.html'
    success_url = reverse_lazy("client_log_profile")


class PaymentView(LoginRequiredMixin, DetailView):
    model = Advertisement
    template_name = "payment_mock/payment.html"
    context_object_name = "payment"

    def get_queryset(self):
        return Advertisement.objects.filter(created_by=self.request.user)  # users can access only their own ads

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment_form'] = PaymentForm()
        return context


class PaymentSuccessView(LoginRequiredMixin, View):
    template_name = "payment_mock/payment_success.html"

    def post(self, request, *args, **kwargs):
        ad_id = self.request.GET.get('ad_id')
        ad = get_object_or_404(Advertisement, pk=ad_id, created_by=self.request.user)
        ad.publish()

        return render(request, self.template_name, {'ad': ad})


class ContactListView(ListView):
    model = Contacts
    context_object_name = 'contacts_list'
    template_name = "contacts/index.html"
