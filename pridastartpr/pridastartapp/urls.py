from django.urls import path, include
from . import views
from . import viewsemi

urlpatterns = [

    path('', viewsemi.home, name='home'),
    path('about_us_emi/', viewsemi.about_us_emi, name='about_us_emi'),
    path('services_emi/', viewsemi.services_emi, name='services_emi'),
    path('database_emi/', viewsemi.database_emi, name='database_emi'),
    path('news_emi/', viewsemi.news_emi, name='news_emi'),
    path('contact_us_emi/', viewsemi.contact_us_emi, name='contact_us_emi'),
    path('temporary_emi/', viewsemi.temporary_emi, name='temporary_emi'),
    path('bmql_emi/', viewsemi.bmql_emi, name='bmql_emi'),
    path('cellphysics_emi/', viewsemi.cellphysics_emi, name='cellphysics_emi'),
    path('techpark_emi/', viewsemi.techpark_emi, name='techpark_emi'),
    path('msystema_emi/', viewsemi.msystema_emi, name='msystema_emi'),
    path('biolic_emi/', viewsemi.biolic_emi, name='biolic_emi'),
    path('contact_us_emi/', viewsemi.contact_us_emi, name='contact_us_emi'),

    # path('', views.home, name='home'),
    path('preeclampsia1/', viewsemi.preeclampsia, name='preeclampsia1'),
    # path('base/', views.base, name='base'),
    # # path('home/', views.home, name='home'),
    # path('about_us/', views.about_us, name='about_us'),
    # path('services/', views.services, name='services'),
    # path('news/', views.news, name='news'),
    # path('gallery/', views.gallery, name='gallery'),
    # path('contact_us/', views.contact_us, name='contact_us'),
    path('logout/', viewsemi.logout_view, name='logout'),
    path('logout1/', viewsemi.logout1, name='logout1'),

    path('login/', viewsemi.login_view, name='login'),
    path('login1/', viewsemi.login1, name='login1'),

    path('test1/', viewsemi.test1, name='test'),

    path('add_edit_patient', viewsemi.add_edit_patient, name='add_edit_patient'),

    #
    # path('login/', views.blog_view, name='blog'),
    # path('generate/', views.generate_objects, name='generate'),
    #
    # path('database/', views.database, name='database'),
    path('users/register/', viewsemi.register, name='register'),
    # path('users/login/', views.login_view, name='login'),
    # path('users/correlation', views.correlation, name='correlation'),
    # path('proba/', views.proba, name='proba'),
    path('controli/', viewsemi.controli, name='controli'),
    # # path('proba1/', views.simple_upload, name='proba1'),
    path('proba1/', viewsemi.proba1, name='proba1'),
    path('calc_patients_more_mut_p/', viewsemi.calc_patients_more_mut_p, name='calc_patients_more_mut_p'),
    path('calc_patients_more_mut_controli/', viewsemi.calc_patients_more_mut_controli, name='calc_patients_more_mut_controli'),
    # # path('preeclampsia1/', views.preeclampsia, name='preeclampsia'),
    path('correlation/', viewsemi.correlation, name='correlation'),
    # path('schema-viewer/', include('schema_viewer.urls')),
    path('conclusions/', viewsemi.conclusions, name='conclusions')


    # path('proba2/', views.proba1, name='proba2') no

    # path('users/correlation/', views.correlation, name='correlation'), no

]