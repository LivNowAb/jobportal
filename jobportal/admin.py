from django.contrib import admin
from jobportal.models import Client, Advertisement, Position, District, Region, BusinessType, Response, Contacts


# Register your models here.
admin.site.register(Client)
admin.site.register(Advertisement)
admin.site.register(Position)
admin.site.register(District)
admin.site.register(Region)
admin.site.register(BusinessType)
admin.site.register(Response)
admin.site.register(Contacts)