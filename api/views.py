from django.shortcuts import render
from rest_framework import mixins, generics

from api.serializers import AdvertisementSerializer
from jobportal.models import Advertisement


class Advertisements(mixins.ListModelMixin, mixins.CreateModelMixin,
             generics.GenericAPIView):
    queryset = Advertisement.objects.filter(published=True)
    serializer_class = AdvertisementSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AdvertisementDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Advertisement.objects.filter(published=True)
    serializer_class = AdvertisementSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
