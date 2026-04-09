from django.urls import path
from . import views
from .views import register


urlpatterns = [
     
  
    path('', views.home, name='home'),
    path('about_us/', views.about_us, name='about_us'),
    path('services/', views.services, name='services'),
    path('news/', views.news, name='news'),
    path('biolic/', views.biolic, name='biolic'),
    path('cellphysics/', views.cellphysics, name='cellphysics'),
    path('techpark/', views.techpark, name='techpark'),
    path('msystema/', views.msystema, name='msystema'),
    path('bmql/', views.bmql, name='bmql'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('logout/', views.logout_view, name='logout'),
    
   
    
    path('database/', views.database, name='database'),
    path('temporary/', views.temporary, name='temporary'),
    path('news/', views.news, name='news'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
   


#Preeclampsia Information
    path('preeclampsia/', views.site, name='site'),  # Patient list view (site.html)
    path('add/', views.add_patient, name='add_patient'),  # Add patient (add.html)
    path('edit/<int:patient_id>/', views.add_patient, name='edit_patient'),  # Edit patient (add.html reused)

#Pregnant Control Information
    path('controls/', views.controls, name='controls'),  # List all controls
    path('addcontrols/', views.addcontrols, name='addcontrols'),  # Add a new control
    path('editcontrols/<int:control_id>/', views.addcontrols, name='edit_controls'),  # Edit an existing control


#accsses to preeclampsia patients
 path('correlation/', views.correlation, name='correlation'), 
 path('correlation_result/', views.correlation_result, name='correlation_result'), 



#Spontaneous abortions
path('spontaneous_abortions/', views.spontaneous_abortions, name='spontaneous_abortions'),
    path('spontaneous_abortions/add/', views.add_abortion, name='add_abortion'),
    path('spontaneous_abortions/edit/<int:abortion_id>/', views.add_abortion, name='edit_abortion'),
    path('spontaneous_abortions/correlation/', views.abortions_correlation, name='abortions_correlation'),

]




""" path('preeclampsia/', views.preeclampsia, name='preeclampsia'), """
"""    path('add_edit_patient/', views.add_edit_patient, name='add_edit_patient'),
    path('add_edit_patient/<int:id>/', views.add_edit_patient, name='edit_patient'),
      path('pregnant_controls/', views.pregnant_controls, name='pregnant_controls'),
   path('add_controla/', views.add_controla, name='add_controla'),  
    path('edit/<int:controla_id>/', views.add_controla, name='edit_controla'),
    path('spontaneous_abortions/', views.spontaneous_abortions, name='spontaneous_abortions'),
       path('home1/', views.home1, name='home1'),
     path('home1/', views.home1, name='home1'),
      """