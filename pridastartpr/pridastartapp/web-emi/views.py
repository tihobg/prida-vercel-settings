from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import CustomRegistrationForm, LoginForm, PatientForm, ControlForm, AbortionForm
from .models import Patient, Control, Abortion

from .models import Abortion
from .forms import AbortionForm  # Assuming you have a corresponding form class
""" import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
import json
from django.conf import settings
import matplotlib.pyplot as plt
import seaborn as sns
import os """



# ADD/EDIT a new patient in Preeclampsia
@login_required
def add_patient(request, patient_id=None):
    if patient_id:
        # Editing an existing patient
        patient = get_object_or_404(Patient, pk=patient_id)
    else:
        # Adding a new patient
        patient = None

    if request.method == 'POST':
        # Submitting the form
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()  # Save the patient
            return redirect('site')  # Redirect to patient list after saving
        else:
            print(form.errors)  # Print any form validation errors for debugging
    else:
        # Displaying the form (for adding or editing)
        form = PatientForm(instance=patient)

    return render(request, 'add.html', {'form': form, 'patient': patient})

def site(request):
    patients = Patient.objects.all().order_by('-id')  # Fetch all patients
    paginator = Paginator(patients, 10)  # Show 10 patients per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'site.html', {'page_obj': page_obj})  



# ADD/EDIT a new patient in Pregnant Controls
@login_required
def addcontrols(request, control_id=None):
    if control_id:
        # Editing an existing control patient
        control = get_object_or_404(Control, pk=control_id)
    else:
        # Adding a new control patient
        control = None

    if request.method == 'POST':
        form = ControlForm(request.POST, instance=control)
        if form.is_valid():
            form.save()
            return redirect('controls')
    else:
        form = ControlForm(instance=control)

    return render(request, 'addcontrols.html', {'form': form, 'control': control})


@login_required
def controls(request):
    controls = Control.objects.all().order_by('-id')  # Fetch all controls
    paginator = Paginator(controls, 10)  # Show 10 controls per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'controls.html', {'page_obj': page_obj}) 


"""  """

# Registration Of USER 
def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # This should work now
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = CustomRegistrationForm()
    return render(request, 'register.html', {'form': form})

# Rename this view to avoid conflicts
def user_login(request):
    return render(request, 'login.html')

#LOGIN Part 
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('database')
                else:
                    messages.error(request, "Вашият акаунт е неактивен.")
            else:
                messages.error(request, "Грешно потребителско име или парола")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

# Logout Part 
def logout_view(request):
    if request.user.is_authenticated:  # Check if the user is logged in
        logout(request)
        return redirect('home')  # Redirect to the homepage or any other page after logout
    else:
        return redirect('login')
    

#correlation view


def correlation_view(request):
    if request.method == "POST":
        # Get the selected parameters from the POST request
        selected_params = [
            param for param in request.POST.keys()
            if request.POST.get(param) == 'on'
        ]

        # Fetch patient data for the selected parameters
        if selected_params:
            patient_data = Patient.objects.values(*selected_params)
            df = pd.DataFrame(patient_data)

            # Calculate the correlation matrix and generate the plot
            if len(selected_params) > 1:
                correlation_matrix = df.corr()

                # Create a heatmap plot
                plt.figure(figsize=(10, 8))
                sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", square=True)
                plt.title("Correlation Matrix for Selected Parameters")

                # Save the plot to a file
                plot_path = os.path.join(settings.MEDIA_ROOT, "correlation_plot.png")
                plt.savefig(plot_path)
                plt.close()

                # Set the plot URL for use in the template
                plot_url = settings.MEDIA_URL + "correlation_plot.png"
            else:
                plot_url = None  # No plot if less than two parameters selected
        else:
            plot_url = None  # No parameters selected

        # Render the results template
        return render(request, 'correlation_result.html', {
            'plot_url': plot_url,
            'selected_params': selected_params,
        })

    # If GET request, render the form page
    return render(request, 'correlation.html')





# ADD/EDIT a new record in Spontaneous Abortions
@login_required
def add_abortion(request, abortion_id=None):
    if abortion_id:
        # Editing an existing abortion record
        abortion = get_object_or_404(Abortion, pk=abortion_id)
    else:
        # Adding a new abortion record
        abortion = None

    if request.method == 'POST':
        # Submitting the form
        form = AbortionForm(request.POST, instance=abortion)
        if form.is_valid():
            form.save()  # Save the record
            return redirect('spontaneous_abortions')  # Redirect to abortion list after saving
        else:
            print(form.errors)  # Log form validation errors (consider replacing with a logger)
    else:
        # Displaying the form (for adding or editing)
        form = AbortionForm(instance=abortion)

    return render(request, 'add_abortion.html', {
        'form': form,
        'abortion': abortion,
        'is_editing': bool(abortion),  # Pass a flag to the template to differentiate between add/edit
    })


def spontaneous_abortions(request):
    abortions = Abortion.objects.all().order_by('-id')  # Fetch all abortion records
    paginator = Paginator(abortions, 10)  # Show 10 records per page

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'spontaneous_abortions.html', {
        'page_obj': page_obj,
    })


def abortions_correlation(request):
    # Logic for generating correlations
    correlations = {}  # Replace this with actual correlation data or calculations

    return render(request, 'abortions_correlation.html', {
        'correlations': correlations,
    })





    
    


# views


def home1(request):
    return render(request, 'home1.html')

def index(request):
    return render(request, 'web/index.html')

def home(request):
    return render(request, 'home.html')

def about_us(request):
    return render(request, 'about_us.html')

def services(request):
    return render(request, 'services.html')

def news(request):
    return render(request, 'news.html')

def biolic(request):
    return render(request, 'biolic.html')

def cellphysics(request):
    return render(request, "cellphysics.html")
def bmql(request):
    return render(request, "bmql.html")

def techpark(request):
    return render(request, "techpark.html")
def msystema(request):
    return render(request, "msystema.html")

def gallery(request):
    return render(request, 'gallery.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def database(request):
    return render(request, 'database.html')

def temporary(request):
    return render(request, 'temporary.html')






def correlation(request):
    return render(request, 'correlation.html')
    
def correlation_result(request):
    return render(request, 'correlation_result.html')




""" 
def controls(request):
      return render(request, 'controls.html')  """


""" @login_required
def add_edit_patient(request):
    return render(request, 'add_edit_patient.html') """
""" @login_required
def preeclampsia(request):
    return render(request, 'preeclampsia.html') """
""" 
def base(request):
    return render(request, 'base.html')
 """
""" @login_required
def pregnant_controls(request):
    return render(request, 'pregnant_controls.html') 
    def add_controla(request):
    return render(request, 'add_controla.html')"""

""" def add(request):
    return render(request, 'add.html')
 """