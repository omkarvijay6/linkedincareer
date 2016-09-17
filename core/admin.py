from django.contrib import admin

# Register your models here.
from core.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass
