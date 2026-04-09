from django import forms
from django.contrib.auth.models import User
from .models import Patient
from .models import Control
from .models import Abortion


"""REGIstration Form """
class CustomRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    repeat_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        if password != repeat_password:
            raise forms.ValidationError("Passwords do not match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



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




# Preeclampisa Edit Add Form 
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        

#Prenant Controla Add Form
class ControlForm(forms.ModelForm):
    class Meta:
        model = Control
        fields = '__all__'



#Form for abortion from django import forms

class AbortionForm(forms.ModelForm):
    class Meta:
        model = Abortion
        fields = '__all__'  # Include all fields from the Abortion model
        widgets = {
            'gender': forms.Select(choices=[('Male', 'Мъж'), ('Female', 'Жена')]),  # Dropdown for gender
            'some_field': forms.RadioSelect(choices=[  # Radio buttons for 0/1
                (0, '0'),
                (1, '1'),
            ]),

        }
        