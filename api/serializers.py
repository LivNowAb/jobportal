from rest_framework.serializers import ModelSerializer

from jobportal.models import Advertisement


class AdvertisementSerializer(ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['position', 'title', 'text_content', 'salary',
                  'client', 'published_date']

