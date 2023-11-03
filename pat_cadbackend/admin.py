from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from .models import Officer, CurrentCall, Civilian, Citation, Arrest, Warrant, Vehicle

# Civilian Admin
class CivilianAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth',)
    search_fields = ('first_name', 'last_name',)
    ordering = ('last_name', 'first_name',)

# Citation Admin
class CitationAdmin(admin.ModelAdmin):
    list_display = ('description', 'date_issued',)
    search_fields = ('description',)
    ordering = ('-date_issued',)

# Arrest Admin
class ArrestAdmin(admin.ModelAdmin):
    list_display = ('description', 'date_arrested',)
    search_fields = ('description',)
    ordering = ('-date_arrested',)

# Warrant Admin
class WarrantAdmin(admin.ModelAdmin):
    list_display = ('description', 'date_issued',)
    search_fields = ('description',)
    ordering = ('-date_issued',)

# Vehicle Admin
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'license_plate',)
    search_fields = ('make', 'model', 'license_plate',)
    ordering = ('make', 'model',)

# Officer Admin
class OfficerAdmin(admin.ModelAdmin):
    list_display = ('badge_number', 'department', 'first_name', 'last_name',)
    search_fields = ('badge_number', 'department', 'first_name', 'last_name',)
    ordering = ('badge_number',)

# CurrentCall Admin
class CurrentCallAdmin(admin.ModelAdmin):
    list_display = ('description', 'time_of_call', 'priority',)
    list_filter = ('priority',)
    search_fields = ('description', 'time_of_call',)
    ordering = ('time_of_call',)

# Register your models here
admin.site.register(Officer, OfficerAdmin)
admin.site.register(CurrentCall, CurrentCallAdmin)
admin.site.register(Civilian, CivilianAdmin)
admin.site.register(Citation, CitationAdmin)
admin.site.register(Arrest, ArrestAdmin)
admin.site.register(Warrant, WarrantAdmin)
admin.site.register(Vehicle, VehicleAdmin)
