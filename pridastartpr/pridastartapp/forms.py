from django import forms
from .models import Patients, PatientProba, Score, Prida, Person, PridaMutations, PridaMutations2
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class PreeclampsiaForm(forms.ModelForm):
    class Meta:
        model = Patients
        # fields = ['patient_id', 'name', 'years']
        fields = ['patient_id', 'name', 'years', 'probe_date', 'birth_date', 'arterial_pressure', 'gw', 'baby_weight',
                  'erythrocytes', 'hemoglobin']


class PatientProbaForm(forms.ModelForm):

    class Meta:
        model = PatientProba
        fields = ['patient_id', 'name', 'years']
        # fields = ['name', 'years']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['name', 'value']


class PridaForm(forms.ModelForm):
    class Meta:
        model = Prida
        fields = ['code', 'number', 'age', 'sex', 'fvl', 'prothr', 'pai', 'mthfr']


class PridaMutationsForm(forms.ModelForm):
    class Meta:
        model = PridaMutations
        fields = ['code', 'age', 'fvl_ng', 'fvl_hetero', 'fvl_homo', 'prothr_ng', 'prothr_hetero',
                  'prothr_homo', 'pai_ng', 'pai_hetero', 'pai_homo', 'mthfr_ng', 'mthfr_hetero', 'mthfr_homo',
                  'abort']

class PridaMutationsForm2(forms.ModelForm):
    class Meta:
        model = PridaMutations2
        # fields = ['code', 'age', 'fvl_ng', 'fvl_hetero', 'fvl_homo', 'prothr_ng', 'prothr_hetero',
        #           'prothr_homo', 'pai_ng', 'pai_hetero', 'pai_homo', 'mthfr_ng', 'mthfr_hetero', 'mthfr_homo',
        #           'abort']
        fields = ['code', 'age',
                  'fvl_hetero', 'fvl_homo',
                  'prothr_hetero', 'prothr_homo',
                  'pai_hetero', 'pai_homo',
                  'mthfr_hetero', 'mthfr_homo',
                  'abort']
class PridaControliForm(forms.ModelForm):
    class Meta:
        model = PridaMutations
        # fields = ['code', 'birth_year', 'age', 'fvl_ng', 'fvl_hetero', 'fvl_homo', 'prothr_ng', 'prothr_hetero', \
        #           'prothr_homo', 'pai_ng', 'pai_hetero', 'pai_homo', 'mthfr_ng', 'mthfr_hetero', 'mthfr_homo']
        #
        fields = ['code', 'age', 'fvl_ng', 'fvl_hetero', 'fvl_homo', 'prothr_ng', 'prothr_hetero',
                  'prothr_homo', 'pai_ng', 'pai_hetero', 'pai_homo', 'mthfr_ng', 'mthfr_hetero', 'mthfr_homo',
                  'abort']

class PridaControliForm2(forms.ModelForm):
    class Meta:
        model = PridaMutations
        fields = ['code', 'age', 'abort', 'fvl_hetero', 'fvl_homo', 'prothr_hetero',
                  'prothr_homo', 'pai_hetero', 'pai_homo', 'mthfr_hetero', 'mthfr_homo']

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'email', 'location']

# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Потребителско име",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
        })
    )
    password = forms.CharField(
        required=True,
        label="Парола",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
        })
    )


