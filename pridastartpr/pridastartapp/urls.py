from django.urls import path, include
from . import views
from . import viewsemi

urlpatterns = [

    path('', viewsemi.home, name='home'),
    path('home_eng', viewsemi.home_eng, name='home_eng'),

    path('about_us_emi/', viewsemi.about_us_emi, name='about_us_emi'),
    path('services_emi/', viewsemi.services_emi, name='services_emi'),
    path('services_eng/', viewsemi.services_eng, name='services_eng'),

    path('database_emi/', viewsemi.database_emi, name='database_emi'),
    path('mutations_eng/', viewsemi.mutations_eng, name='mutations_eng'),
    path('pregnant_controls_mut_analysis_eng/', viewsemi.pregnant_controls_mut_analysis_eng,
         name='pregnant_controls_mut_analysis_eng'),
    path('pregnant_mut_analysis_eng/', viewsemi.pregnant_mut_analysis_eng, name='pregnant_mut_analysis_eng'),
    path('controli_mut_analysis_eng/', viewsemi.controli_mut_analysis_eng, name='controli_mut_analysis_eng'),
    path('mut_analysis_eng/', viewsemi.mut_analysis_eng, name='mut_analysis_eng'),

    path('news_emi/', viewsemi.news_emi, name='news_emi'),
    path('contact_us_emi/', viewsemi.contact_us_emi, name='contact_us_emi'),
    path('spontaneous_aborts/', viewsemi.spontaneous_aborts, name='spontaneous_aborts'),

    # path('preeclampsia/', viewsemi.preeclampsia, name='preeclampsia'),
    path('preeclampsia_eng/', viewsemi.preeclampsia_eng, name='preeclampsia_eng'),
    path('preeclampsia_eng_new/', viewsemi.preeclampsia_eng_new, name='preeclampsia_eng_new'),
    path('preeclampsia_controli_eng/', viewsemi.preeclampsia_controli_eng, name='preeclampsia_controli_eng'),

    path('select_pathology_eng/', viewsemi.select_pathology_eng, name='select_pathology_eng'),

    path('temporary_eng/', viewsemi.temporary_eng, name='temporary_eng'),

    path('bmql_emi/', viewsemi.bmql_emi, name='bmql_emi'),
    path('cellphysics_emi/', viewsemi.cellphysics_emi, name='cellphysics_emi'),
    path('prida_publication_bg/', viewsemi.prida_publication_bg, name='prida_publication_bg'),
    path('prida_publication_eng/', viewsemi.prida_publication_eng, name='prida_publication_eng'),

    path('prida_publication2_bg/', viewsemi.prida_publication2_bg, name='prida_publication2_bg'),
    path('prida_publication2_eng/', viewsemi.prida_publication2_eng, name='prida_publication2_eng'),

    path('prida_publication3_bg/', viewsemi.prida_publication3_bg, name='prida_publication3_bg'),
    path('prida_publication3_eng/', viewsemi.prida_publication3_eng, name='prida_publication3_eng'),

    path('prida_publication4_bg/', viewsemi.prida_publication4_bg, name='prida_publication4_bg'),
    path('prida_publication4_eng/', viewsemi.prida_publication4_eng, name='prida_publication4_eng'),

    path('prida_publication5_bg/', viewsemi.prida_publication5_bg, name='prida_publication5_bg'),
    path('prida_publication5_eng/', viewsemi.prida_publication5_eng, name='prida_publication5_eng'),

    path('prida_publication6_bg/', viewsemi.prida_publication6_bg, name='prida_publication6_bg'),
    path('prida_publication6_eng/', viewsemi.prida_publication6_eng, name='prida_publication6_eng'),

    path('techpark_emi/', viewsemi.techpark_emi, name='techpark_emi'),
    path('msystema_emi/', viewsemi.msystema_emi, name='msystema_emi'),
    path('biolic_emi/', viewsemi.biolic_emi, name='biolic_emi'),
    path('biolic_eng/', viewsemi.biolic_eng, name='biolic_eng'),

    path('contact_us_emi/', viewsemi.contact_us_emi, name='contact_us_emi'),
    path('new_patient/', viewsemi.new_patient, name='new_patient'),

    # path('', views.home, name='home'),
    path('preeclampsia/', viewsemi.preeclampsia, name='preeclampsia'),
    # path('base/', views.base, name='base'),
    # # path('home/', views.home, name='home'),
    path('about_us_eng/', viewsemi.about_us_eng, name='about_us_eng'),
    # path('services/', views.services, name='services'),
    path('news_eng/', viewsemi.news_eng, name='news_eng'),
    # path('gallery/', views.gallery, name='gallery'),
    path('contact_us_eng/', viewsemi.contact_us_eng, name='contact_us_eng'),
    path('logout/', viewsemi.logout_view, name='logout'),
    path('logout1/', viewsemi.logout1, name='logout1'),
    path('logout_eng/', viewsemi.logout_view_eng, name='logout_eng'),

    path('login/', viewsemi.login_view, name='login'),
    path('login1/', viewsemi.login1, name='login1'),
    path('login_eng/', viewsemi.login_eng, name='login_eng'),

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
    path('controli_eng/', viewsemi.controli_eng, name='controli_eng'),

    # # path('proba1/', views.simple_upload, name='proba1'),
    path('proba1/', viewsemi.proba1, name='proba1'),
    path('proba1_eng/', viewsemi.proba1_eng, name='proba1_eng'),

    path('calc_patients_more_mut_p/', viewsemi.calc_patients_more_mut_p, name='calc_patients_more_mut_p'),
    path('calc_patients_more_mut_controli/', viewsemi.calc_patients_more_mut_controli, name='calc_patients_more_mut_controli'),
    # # path('preeclampsia1/', views.preeclampsia, name='preeclampsia'),
    path('correlation/', viewsemi.correlation, name='correlation'),
    # path('schema-viewer/', include('schema_viewer.urls')),
    path('conclusions/', viewsemi.conclusions, name='conclusions')


    # path('proba2/', views.proba1, name='proba2') no

    # path('users/correlation/', views.correlation, name='correlation'), no

]