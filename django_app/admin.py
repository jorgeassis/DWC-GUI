from django.contrib import admin

from .models import speciesRecords, biodiversityRecords


class speciesAdmin(admin.ModelAdmin):
    list_display = ("speciesName","acceptedSpeciesName")

class recordsAdmin(admin.ModelAdmin):
    list_display = ("speciesName","acceptedSpeciesName")

myModels = [speciesRecords, biodiversityRecords]  # iterable list
admin.site.register(myModels)
