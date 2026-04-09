from django.contrib import admin, messages
from .models import Patient  # Import your Patient model
from .models import Control
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
# Register the Patient model
#  with the admin site
""" admin.site.register(Patient) """

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    # This displays selected fields in the list view in the admin panel
    list_display = ('name', 'maternal_age', 'systolic_blood_pressure', 'diastolic_blood_pressure',
            'gestational_week', 'newborn_weight', 'eai1', 'nea1', 'eai2', 'nea2',
            'erythrocytes', 'hemoglobin', 'hematocrit', 'mcv', 'mch', 'mchc', 'rdw',
            'prothrombin_time_sec', 'prothrombin_time_percent', 'prothrombin_time_inr',
            'platelets', 'mpv', 'pct', 'pdw', 'creatinine', 'total_protein', 'albumin',
            'fibrinogen', 'crp', 'proteinuria', 'asat', 'alat', 'factor_v_leiden',
            'factor_ii_mutation', 'pai', 'mthfr')

    # Optionally, you can customize what fields are searchable in the admin interface
    search_fields = ('name', 'maternal_age')

    # Optionally, you can filter by specific fields in the admin panel
    list_filter = ('maternal_age', 'systolic_blood_pressure', 'diastolic_blood_pressure')



    @admin.register(Control)
    class PatientAdmin(admin.ModelAdmin):
    # This displays selected fields in the list view in the admin panel
     list_display = ('name', 'maternal_age', 'systolic_blood_pressure', 'diastolic_blood_pressure',
            'gestational_week', 'newborn_weight', 'eai1', 'nea1', 'eai2', 'nea2',
            'erythrocytes', 'hemoglobin', 'hematocrit', 'mcv', 'mch', 'mchc', 'rdw',
            'prothrombin_time_sec', 'prothrombin_time_percent', 'prothrombin_time_inr',
            'platelets', 'mpv', 'pct', 'pdw', 'creatinine', 'total_protein', 'albumin',
            'fibrinogen', 'crp', 'proteinuria', 'asat', 'alat', 'factor_v_leiden',
            'factor_ii_mutation', 'pai', 'mthfr')

    # Optionally, you can customize what fields are searchable in the admin interface
    search_fields = ('name', 'maternal_age')

    # Optionally, you can filter by specific fields in the admin panel
    list_filter = ('maternal_age', 'systolic_blood_pressure', 'diastolic_blood_pressure')






from .models import Abortion

@admin.register(Abortion)
class AbortionAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = (
        'no', 'code', 'year', 'number', 'age', 'gender',
        'factor_v_normal', 'factor_v_heterozygous', 'factor_v_homozygous',
        'factor_ii_normal', 'factor_ii_heterozygous', 'factor_ii_homozygous',
        'pai1_normal', 'pai1_heterozygous', 'pai1_homozygous',
        'mthfr_normal', 'mthfr_heterozygous', 'mthfr_homozygous'
    )
    
    # Add search functionality
    search_fields = ('no', 'code', 'year', 'gender')

    # Add filter options
    list_filter = ('year', 'gender', 'factor_v_normal', 'factor_ii_normal')

    # Add ordering functionality
    ordering = ('year', 'no')

    # Specify editable fields in the admin list view
    list_editable = ('code', 'year', 'number', 'age', 'gender')
   
    # Register the action
    actions = ['import_excel']



    def import_excel(self, request, queryset):
        """
        Admin action to upload and process an Excel file directly in the admin.
        """
        if 'apply' in request.POST:
            # Handle file upload
            excel_file = request.FILES.get('excel_file')
            if not excel_file:
                self.message_user(request, "No file selected!", level=messages.ERROR)
                return HttpResponseRedirect(request.get_full_path())

            try:
                # Read the uploaded Excel file
                df = pd.read_excel(excel_file)

                # Map and save data from Excel rows into the database
                for _, row in df.iterrows():
                    Abortion.objects.create(
                        no=row.get('No', ''),
                        code=row.get('Code', ''),
                        year=row.get('Year', None),
                        number=row.get('Number', None),
                        age=row.get('Age', None),
                        gender=row.get('Gender', ''),
                        factor_v_normal=row.get('Factor V Normal', False),
                        factor_v_heterozygous=row.get('Factor V Heterozygous', False),
                        factor_v_homozygous=row.get('Factor V Homozygous', False),
                        factor_ii_normal=row.get('Factor II Normal', False),
                        factor_ii_heterozygous=row.get('Factor II Heterozygous', False),
                        factor_ii_homozygous=row.get('Factor II Homozygous', False),
                        pai1_normal=row.get('PAI-1 Normal', False),
                        pai1_heterozygous=row.get('PAI-1 Heterozygous', False),
                        pai1_homozygous=row.get('PAI-1 Homozygous', False),
                        mthfr_normal=row.get('MTHFR Normal', False),
                        mthfr_heterozygous=row.get('MTHFR Heterozygous', False),
                        mthfr_homozygous=row.get('MTHFR Homozygous', False),
                    )
                self.message_user(request, "Data imported successfully!")
            except Exception as e:
                self.message_user(request, f"Error processing file: {e}", level=messages.ERROR)

            return HttpResponseRedirect(request.get_full_path())

        # Display a simple file upload form directly in the admin interface
        return HttpResponseRedirect(request.get_full_path() + "?upload_form")

    import_excel.short_description = "Import data from Excel"

    def changelist_view(self, request, extra_context=None):
        """
        Override the changelist view to add a file upload form directly in the admin page.
        """
        if request.GET.get('upload_form'):
            upload_form = format_html('''
                <form method="post" enctype="multipart/form-data">
                    <input type="file" name="excel_file" accept=".xls,.xlsx" required>
                    <button type="submit" name="apply" class="button">Upload and Import</button>
                </form>
            ''')
            self.message_user(request, "Upload your Excel file below:" + upload_form)
        return super().changelist_view(request, extra_context)