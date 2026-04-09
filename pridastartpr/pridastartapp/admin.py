from django.contrib import admin
from . models import Patients, PatientProba, Score, Prida, Person, PridaMutations, PridaControli, PridaMutations2
from import_export.admin import ImportExportModelAdmin

# class ScoreAdmin(admin.ModelAdmin):
#     list_display = ['name', 'value']


admin.site.register(Patients)
admin.site.register(PatientProba)
# admin.site.register(Score, ScoreAdmin)
admin.site.register(Score)
admin.site.register(Prida, ImportExportModelAdmin)
admin.site.register(PridaMutations, ImportExportModelAdmin)
admin.site.register(PridaMutations2, ImportExportModelAdmin)

admin.site.register(PridaControli, ImportExportModelAdmin)


admin.site.register(Person)


# @admin.register(Person)
# class PersonAdmin(ImportExportModelAdmin):
#     list_display = ('name', 'email', 'location')
# Register your models here.
