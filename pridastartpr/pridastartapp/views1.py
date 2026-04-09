from django.shortcuts import render, redirect
from . models import Patients, PatientProba, Score, Prida, Person, PridaMutations
from . forms import PreeclampsiaForm, RegisterForm, PatientProbaForm, ScoreForm, PridaForm, PridaMutationsForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from typing import Tuple
import sqlite3
from tablib import Dataset
from . resources import PersonResource
from django.contrib import messages

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import base64
import io
import os
import urllib

import csv
from bs4 import BeautifulSoup




def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/preeclampsia1')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', { 'form' : form})


def home1(request):
    return render(request, 'home1.html')


def database(request):
    return render(request, 'database.html')


def index(request):
    return render(request, 'web/index.html')


def home(request):
    return render(request, 'home.html')


def base(request):
    return render(request, 'base.html')


def services(request):
    return render(request, 'services.html')


def news(request):
    return render(request, 'news.html')


def gallery(request):
    return render(request, 'gallery.html')


def contact_us(request):
    return render(request, 'contact_us.html')


def logout_view(request):
    # handle logout logic here
    return render(request, 'home.html')


def about_us(request):
    return render(request, 'about_us.html')


def add_edit_patient(request):
    return render(request, 'add_edit_patient.html')


# def login(request):
#     return render(request, 'login.html')


def correlation(request):
    # if request.method == 'POST':
    #     form = AuthenticationForm(data=request.POST)
    #     if form.is_valid():
    #         login(request, form.get_user())
    #         return redirect('/')
    # else:
    #     form = AuthenticationForm()
    return render(request, 'users/correlation.html')


def register(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = RegisterForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('/about_us')
    else:
        # form = UserCreationForm()
        form = RegisterForm()
        # form = NameForm()
    return render(request, 'users/register.html', {'form': form})


def preeclampsia(request):

    # with open('login.html', 'r', encoding='utf-8') as file:
    #     html_cont = file.read()
    # all_tags = html_cont.find()
    # for tag in all_tags:
    #     print(tag.get_text())
    form_pre = PreeclampsiaForm()
    patients = Patients.objects.all()
    s = request.POST.getlist('ss')

    # Visualization of Correlation
    matplotlib.use('agg')
    # # plt.style.use('ggplot')
    nx = np.arange(10, 20)
    ny = np.array([2, 1, 4, 5, 8, 12, 18, 25, 96, 48])
    xyz = np.array([[10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                    [2, 1, 4, 5, 8, 12, 18, 25, 96, 48],
                    [5, 3, 2, 1, 0, -2, -8, -11, -15, -16]])

    corr_matrix = np.corrcoef(xyz).round(decimals=2)
    # # print(corr_matrix)
    #
    fig, ax = plt.subplots()
    im = ax.imshow(corr_matrix)
    im.set_clim(-1, 1)
    ax.grid(False)
    ax.xaxis.set(ticks=(0, 1, 2), ticklabels=('x', 'y', 'z'))
    ax.yaxis.set(ticks=(0, 1, 2), ticklabels=('x', 'y', 'z'))
    ax.set_ylim(2.5, -0.5)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, corr_matrix[i, j], ha='center', va='center',
                    color='r')
    cbar = ax.figure.colorbar(im, ax=ax, format='% .2f')

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    #
    # # ax.plot(nx, ny, linewidth=0, marker='s', label='Data Points')
    # # plt.savefig("mygraph.png")
    # # plt.show()
    # form = ScoreForm()
    form_pre = PreeclampsiaForm()
    form_pre1 = PatientProbaForm()

    if request.method == "POST":
        if 'save' in request.POST:
            pk = request.POST.get('save')
            if not pk:
                form_pre = PreeclampsiaForm(request.POST)
            else:
                patient = Patients.objects.get(patient_id=pk)
                form_pre = PreeclampsiaForm(request.POST, instance=patient)
            form_pre.save()
            form_pre = PreeclampsiaForm()

        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            patient = Patients.objects.get(patient_id=pk)
            patient.delete()
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            patient = Patients.objects.get(patient_id=pk)
            form_pre = PreeclampsiaForm(instance=patient)
            print('Hello')
    context1 = {
        'patients': patients,
        'key': s,
        'key6': url,
        'key7': form_pre1['name'],
        'key8': form_pre,

    }

    return render(request, 'preeclampsia1.html', context1)


def blog_view(request):
    # soup = BeautifulSoup('/Users/tihomir/PycharmProjects/projectproba/pridastartpr/pridastartapp/templates/login.html', 'html.parser')
    # print(soup.find('title'))
    with open('/Users/tihomir/PycharmProjects/projectproba/pridastartpr/pridastartapp/templates/login.html') as f:
        soup = BeautifulSoup(f, 'html.parser')
    print(soup.find('textarea'))
    # print(soup)

    posts = PatientProba.objects.all()
    with open('/Users/tihomir/PycharmProjects/projectproba/pridastartpr/pridastartapp/proba.csv', 'r') as f:
        reader = csv.reader(f)
        a = []
        i = 0
        # print(reader)
        for line in reader:
            i = i + 1
            a = line
            print(a[1])
            # p = PatientProba(name=f"{a[1]}")
            # p.save()
            # break
        print(a[0], a[1], a[2])
        print(i)
        # os.startfile(r'/Users/tihomir/PycharmProjects/projectproba/pridastartpr/pridastartapp/proba.csv')
        # file = open('/Users/tihomir/PycharmProjects/projectproba/pridastartpr/pridastartapp/proba.csv')

        # print(path)

        # p = PatientProba(name=f"{a[1]}")
        # p.save()


        # for c in a:
        #     c.replace('\ufeff', '')
        # data = [print([c.replace('\ufeff', '') for c in row]) for row in reader]
        # print(data)
        # for line in reader:
        #     print(line)

    # if request.method == 'POST':
    #     value = request.POST.get('my_input')
    #     print(value)

        context2 = {
            'posts': posts,
            'key9': i,
            'key10': soup.find('textarea'),
            # 'key11': value,

        }

    # return render(request, 'login.html', {'posts':posts})
    return render(request, 'login.html', context2)


def proba(request):
    context4 = {}
    prida = Prida.objects.all()
    # forma = ScoreForm()
    # forma1 = ScoreForm()
    prida_form = PridaForm()
    # print("Yes")
    # print(forma['value'])
    list_birth_year = Prida.objects.values_list('birth_year')
    list_age = Prida.objects.values_list('age')
    list_fvl = Prida.objects.values_list('fvl')
    list_prothr = Prida.objects.values_list('prothr')
    list_pai = Prida.objects.values_list('pai')
    list_mthfr = Prida.objects.values_list('mthfr')
    prida_list_data = request.POST.getlist('prida_list_data')



    print(prida[1])
    print(list_age[1][0])
    count_fvl = 0
    count_all_fvl_data = 0
    # count_fvl_0 = 0
    for fvl_data in list_fvl:
        count_all_fvl_data = count_all_fvl_data + 1
        if fvl_data[0] == '1.0':
            count_fvl = count_fvl + 1
    print(count_fvl)
    count_fvl_0 = count_all_fvl_data - count_fvl
    fvl_1_percent = count_fvl * 100 / count_all_fvl_data

    count_prothr = 0
    count_all_prothr_data = 0
    # count_prothr_0 = 0
    for prothr_data in list_prothr:
        count_all_prothr_data = count_all_prothr_data + 1
        if prothr_data[0] == '1.0':
            count_prothr = count_prothr + 1
    print(count_prothr)
    count_prothr_0 = count_all_prothr_data - count_prothr
    prothr_1_percent = count_prothr * 100 / count_all_prothr_data

    count_mthfr = 0
    count_all_mthfr_data = 0
    for mthfr_data in list_mthfr:
        count_all_mthfr_data = count_all_mthfr_data + 1
        if mthfr_data[0] == '1.0':
            count_mthfr = count_mthfr + 1
    print(count_mthfr)
    count_mthfr_0 = count_all_mthfr_data - count_mthfr
    mthfr_1_percent = count_mthfr * 100 / count_all_mthfr_data

    count_pai = 0
    count_all_pai_data = 0
    for pai_data in list_pai:
        count_all_pai_data = count_all_pai_data + 1
        if pai_data[0] == '1.0':
            count_pai = count_pai + 1
    print(count_pai)
    count_pai_0 = count_all_pai_data - count_pai
    pai_1_percent = count_pai * 100 / count_all_pai_data



        # if float(age[1][0]) == 0:
        #     print(float(age[1][0]))
        #     print("OK")
        # else:
        #     print("NO")

    # conn = sqlite3.connect('Score.db')
    # cursor = conn.cursor()

    # cursor.execute('''
    # CREATE TABLE IF NOT EXISTS products (
    #     ID TEXT PRIMARY KEY,
    #     name TEXT,
    #     price INTEGER
    #     )''')
    # products = [
    #     ('mimo', 11),
    #     ('mamo', 22)
    # ]
    #
    # cursor.executemany('INSERT INTO Score (name, value) VALUES (?, ?)', products)
    # #
    # conn.commit()
    # conn.close()




    # context3['prida'] = prida
    # # context3['forma'] = forma
    # # context3['forma1'] = forma1
    # context3['prida_form'] = prida_form
    # context3['list_birth_year'] = list_birth_year
    # context3['list_age'] = list_age
    # context3['list_fvl'] = list_fvl

    if request.method == "POST":
        if 'save' in request.POST:
            # forma = ScoreForm(request.POST)
            # forma.save()
            prida_form = PridaForm(request.POST)
            prida_form.save()
            # forma1 = ScoreForm(request.POST)
            # forma1.save()
            # scores = Score.objects.all()
            # print(scores[8])
    # a = 0

    if prida_list_data:
        print(prida_list_data[0])

    # print(prida_list_data)
    # a = prida_list_data[0]
    # context3 = {
    #     'prida': prida,
    #     'prida_form': prida_form,
    #     'prida_list_data': prida_list_data[0],
    #     'list_age': list_age,
    #     'list_fvl': list_fvl,
    #     'list_prothr': list_prothr,
    #     'list_pai': list_pai,
    #     'list_mthfr': list_mthfr,
    #     'count_fvl': count_fvl,
    #
    #
    # }
        context4['prida_list_data'] = prida_list_data[0]
        print(context4['prida_list_data'])

    context4['count_fvl'] = count_fvl
    context4['count_fvl_0'] = count_fvl_0
    context4['fvl_1_percent'] = fvl_1_percent

    context4['count_prothr'] = count_prothr
    context4['count_prothr_0'] = count_prothr_0
    context4['prothr_1_percent'] = prothr_1_percent

    context4['count_mthfr'] = count_mthfr
    context4['count_mthfr_0'] = count_mthfr_0
    context4['mthfr_1_percent'] = mthfr_1_percent

    context4['count_pai'] = count_pai
    context4['count_pai_0'] = count_pai_0
    context4['pai_1_percent'] = pai_1_percent

    context4['prida_list'] = prida_list_data
    context4['prida'] = prida
    context4['prida_form'] = prida_form
    # context3['fvl_1_percent'] = fvl_1_percent

    return render(request, 'proba.html', context4)


def proba1(request):
    context3 = {}
    prida_mutations = PridaMutations.objects.all()
    # forma = ScoreForm()
    # forma1 = ScoreForm()
    prida_mutations_form = PridaMutationsForm()
    # print(forma['value'])
    # list_birth_year = PridaMutations.objects.values_list('birth_year')
    list_age = PridaMutations.objects.values_list('age')

    list_fvl_ng = PridaMutations.objects.values_list('fvl_ng')
    list_fvl_hetero = PridaMutations.objects.values_list('fvl_hetero')
    list_fvl_homo = PridaMutations.objects.values_list('fvl_homo')

    list_prothr_ng = PridaMutations.objects.values_list('prothr_ng')
    list_prothr_hetero = PridaMutations.objects.values_list('prothr_hetero')
    list_prothr_homo = PridaMutations.objects.values_list('prothr_homo')

    list_pai_ng = PridaMutations.objects.values_list('pai_ng')
    list_pai_hetero = PridaMutations.objects.values_list('pai_hetero')
    list_pai_homo = PridaMutations.objects.values_list('pai_homo')

    list_mthfr_ng = PridaMutations.objects.values_list('mthfr_ng')
    list_mthfr_hetero = PridaMutations.objects.values_list('mthfr_hetero')
    list_mthfr_homo = PridaMutations.objects.values_list('mthfr_homo')

    list_abort = PridaMutations.objects.values_list('abort')


    prida_list_data = request.POST.getlist('prida_list_data')
    prida_age_list = request.POST.getlist('age')
    prida_abort_list = request.POST.getlist('abort')
    print(prida_list_data, 'OK')
    print(prida_age_list, 'OK')
    print(prida_abort_list, 'OK')
    end_line = request.POST.get('end_line')
    start_line = request.POST.get('start_line')

    age = ''
    for data in prida_age_list:
        if data == 'age1' or data == 'age2' or data == 'age3':
            age = data
    print(age, 'AGE')
    abort = ''
    for data in prida_abort_list:
        if data == 'abort_1' or data == 'abort_2' or data == 'abort_3':
            abort = data
    print(abort, 'ABORT')




    p = end_line
    print(start_line, end_line)
    # print(type(p))
    # end_line = int(end_line)
    # p = int(end_line)
    # print(end_line)
    # p1 = '123'
    # print(type(p1))
    # print(int(p1))
    # print(type(int(p1)))

    # print(type(list_fvl_ng))
    # mydata = PridaMutations.objects.values_list('fvl_ng')[5:10]
    # # mydata = PridaMutations.objects.filter('fvl_ng' == 0).values()
    # print(mydata)




    # count_fvl = 0
    # count_all_fvl_data = 0
    # # count_fvl_0 = 0
    # for fvl_data in list_fvl:
    #     count_all_fvl_data = count_all_fvl_data + 1
    #     if fvl_data[0] == '1.0':
    #         count_fvl = count_fvl + 1
    # print(count_fvl)
    # count_fvl_0 = count_all_fvl_data - count_fvl
    # fvl_1_percent = count_fvl * 100 / count_all_fvl_data

    # count_prothr = 0
    # count_all_prothr_data = 0
    # for prothr_data in list_prothr:
    #     count_all_prothr_data = count_all_prothr_data + 1
    #     if prothr_data[0] == '1.0':
    #         count_prothr = count_prothr + 1
    # print(count_prothr)
    # count_prothr_0 = count_all_prothr_data - count_prothr
    # prothr_1_percent = count_prothr * 100 / count_all_prothr_data

    # count_mthfr = 0
    # count_all_mthfr_data = 0
    # for mthfr_data in list_mthfr:
    #     count_all_mthfr_data = count_all_mthfr_data + 1
    #     if mthfr_data[0] == '1.0':
    #         count_mthfr = count_mthfr + 1
    # print(count_mthfr)
    # count_mthfr_0 = count_all_mthfr_data - count_mthfr
    # mthfr_1_percent = count_mthfr * 100 / count_all_mthfr_data

    # count_pai = 0
    # count_all_pai_data = 0
    # for pai_data in list_pai:
    #     count_all_pai_data = count_all_pai_data + 1
    #     if pai_data[0] == '1.0':
    #         count_pai = count_pai + 1
    # print(count_pai)
    # count_pai_0 = count_all_pai_data - count_pai
    # pai_1_percent = count_pai * 100 / count_all_pai_data

    if request.method == 'POST':
        if 'calculate_mutations_aborts' in request.POST:
            print('Calculate Mutations Aborts 1')
            print('1111 Calculate')
            context3['end_line'] = int(end_line)
            context3['start_line'] = int(start_line)
            context3['clients_list'] = int(end_line) - int(start_line)
            clients_list = context3['clients_list']
            sublist = slice(int(start_line), int(end_line))

            sublist_age = list_age[sublist]
            print(sublist_age)
            sublist_abort = list_abort[sublist]
            print(sublist_abort)

            index_array_age1 = create_age_array(sublist_age)[0]
            index_array_age2 = create_age_array(sublist_age)[1]
            index_array_age3 = create_age_array(sublist_age)[2]

            create_array_age_and_age_interval_access_html(prida_age_list,
                                                          index_array_age1,
                                                          index_array_age2,
                                                          index_array_age3)



            count_abort1 = 0
            count_abort2 = 0
            count_abort3 = 0

            index_array_abort1 = []
            index_array_abort2 = []
            index_array_abort3 = []



            count_index_array_abort = 0

            context3['index_array_age'] = create_array_age_and_age_interval_access_html(prida_age_list,
                                                                                        index_array_age1,
                                                                                        index_array_age2,
                                                                                        index_array_age3)['index_array_age']

            context3['age_interval_aborts'] = create_array_age_and_age_interval_access_html(prida_age_list,
                                                                                        index_array_age1,
                                                                                        index_array_age2,
                                                                                        index_array_age3)['age_interval']
            index_array_age_data = context3['index_array_age']

            # create_abort_index_array(index_array_age_data, sublist_abort)

            index_array_abort1 = create_abort_index_array(index_array_age_data, sublist_abort)[0]
            index_array_abort2 = create_abort_index_array(index_array_age_data, sublist_abort)[1]
            index_array_abort3 = create_abort_index_array(index_array_age_data, sublist_abort)[2]

            # create_dict_index_array_aborts_and_abort_variant_html(prida_abort_list,
            #                                                       index_array_abort1,
            #                                                       index_array_abort2,
            #                                                       index_array_abort3)


            ################################################################
            ## Създаване на поредица от пациенти с 1, 2 или повече аборти ##
            ################################################################
            # for abort in index_array_age_data:
            #     if sublist_abort[abort][0] == '1.0':
            #         count_abort1 = count_abort1 + 1
            #         index_array_abort1.append(abort)
            #     elif sublist_abort[abort][0] == '2.0':
            #         count_abort2 = count_abort2 + 1
            #         index_array_abort2.append(abort)
            #     elif sublist_abort[abort][0] != '?' or sublist_abort[abort][0] != '2.0' or sublist_abort[abort][
            #         0] != '1.0':
            #         count_abort3 = count_abort3 + 1
            #         index_array_abort3.append(abort)
            #
            #     count_index_array_abort = count_index_array_abort + 1
            #
            # print(index_array_abort1, 'OK')
            # print(index_array_abort2, 'OK')
            # print(index_array_abort3, 'OK')

            #########################################################################
            ## Създаване на групи от пациенти с 1, 2 и повече аборти и поредица от ##
            #########################################################################
            # for abort in prida_abort_list:
            #     if abort == 'abort_1':
            #         context3['index_array_abort'] = index_array_abort1
            #         context3['abort_variant'] = abort
            #     elif abort == 'abort_2':
            #         context3['index_array_abort'] = index_array_abort2
            #         context3['abort_variant'] = abort
            #     elif abort == 'abort_3':
            #         context3['index_array_abort'] = index_array_abort3
            #         context3['abort_variant'] = abort
            #
            # context3['number_abort_patients'] = len(context3['index_array_abort'])
            #
            # print(context3['index_array_abort'], 'OK', context3['number_abort_patients'])

            sublist_fvl_ng = list_fvl_ng[sublist]
            sublist_fvl_hetero = list_fvl_hetero[sublist]
            sublist_fvl_homo = list_fvl_homo[sublist]

            sublist_prothr_ng = list_prothr_ng[sublist]
            sublist_prothr_hetero = list_prothr_hetero[sublist]
            sublist_prothr_homo = list_prothr_homo[sublist]

            sublist_pai_ng = list_pai_ng[sublist]
            sublist_pai_hetero = list_pai_hetero[sublist]
            sublist_pai_homo = list_pai_homo[sublist]

            sublist_mthfr_ng = list_mthfr_ng[sublist]
            sublist_mthfr_hetero = list_mthfr_hetero[sublist]
            sublist_mthfr_homo = list_mthfr_homo[sublist]

            count_fvl_ng = 0
            count_fvl_hetero = 0
            count_fvl_homo = 0

            count_prothr_ng = 0
            count_prothr_hetero = 0
            count_prothr_homo = 0

            count_pai_ng = 0
            count_pai_hetero = 0
            count_pai_homo = 0

            count_mthfr_ng = 0
            count_mthfr_hetero = 0
            count_mthfr_homo = 0
            # print(prida_list_data)

            count_fvl_ng_mutations = 0
            count_fvl_ng_mutations_abort1 = 0
            count_fvl_ng_mutations_abort2 = 0
            count_fvl_ng_mutations_abort3 = 0

            count_fvl_hetero_mutations = 0
            count_fvl_hetero_mutations_abort1 = 0
            count_fvl_hetero_mutations_abort2 = 0
            count_fvl_hetero_mutations_abort3 = 0

            count_fvl_homo_mutations = 0
            count_fvl_homo_mutations_abort1 = 0
            count_fvl_homo_mutations_abort2 = 0
            count_fvl_homo_mutations_abort3 = 0

            count_prothr_ng_mutations = 0
            count_prothr_ng_mutations_abort1 = 0
            count_prothr_ng_mutations_abort2 = 0
            count_prothr_ng_mutations_abort3 = 0

            count_prothr_hetero_mutations = 0
            count_prothr_hetero_mutations_abort1 = 0
            count_prothr_hetero_mutations_abort2 = 0
            count_prothr_hetero_mutations_abort3 = 0

            count_prothr_homo_mutations = 0
            count_prothr_homo_mutations_abort1 = 0
            count_prothr_homo_mutations_abort2 = 0
            count_prothr_homo_mutations_abort3 = 0

            count_pai_ng_mutations = 0
            count_pai_ng_mutations_abort1 = 0
            count_pai_ng_mutations_abort2 = 0
            count_pai_ng_mutations_abort3 = 0

            count_pai_hetero_mutations = 0
            count_pai_hetero_mutations_abort1 = 0
            count_pai_hetero_mutations_abort2 = 0
            count_pai_hetero_mutations_abort3 = 0

            count_pai_homo_mutations = 0
            count_pai_homo_mutations_abort1 = 0
            count_pai_homo_mutations_abort2 = 0
            count_pai_homo_mutations_abort3 = 0

            count_mthfr_ng_mutations = 0
            count_mthfr_ng_mutations_abort1 = 0
            count_mthfr_ng_mutations_abort2 = 0
            count_mthfr_ng_mutations_abort3 = 0

            count_mthfr_hetero_mutations = 0
            count_mthfr_hetero_mutations_abort1 = 0
            count_mthfr_hetero_mutations_abort2 = 0
            count_mthfr_hetero_mutations_abort3 = 0

            count_mthfr_homo_mutations = 0
            count_mthfr_homo_mutations_abort1 = 0
            count_mthfr_homo_mutations_abort2 = 0
            count_mthfr_homo_mutations_abort3 = 0

            res_func1 = func1(
                prida_list_data,
                index_array_age_data,
                sublist_fvl_ng,
                sublist_fvl_hetero,
                sublist_fvl_homo,
                sublist_prothr_ng,
                sublist_prothr_hetero,
                sublist_prothr_homo,
                sublist_pai_ng,
                sublist_pai_hetero,
                sublist_pai_homo,
                sublist_mthfr_ng,
                sublist_mthfr_hetero,
                sublist_mthfr_homo,
                sublist_abort,
                clients_list)

            context3['count_mutations_abort1'] = res_func1[0]
            context3['percent_mutations_abort1'] = res_func1[1]
            context3['count_mutations_abort2'] = res_func1[2]
            context3['percent_mutations_abort2'] = res_func1[3]
            context3['count_mutations_abort3'] = res_func1[4]
            context3['percent_mutations_abort3'] = res_func1[5]

            print(context3['count_mutations_abort1'],
                  context3['percent_mutations_abort1'],
                  context3['count_mutations_abort2'],
                  context3['percent_mutations_abort2'],
                  context3['count_mutations_abort3'],
                  context3['percent_mutations_abort3'])

            # print(context3['age_interval'], 'New')
            # print(context3['index_array_age'], 'New', sublist_age)
            # print(prida_list_data[0], 'Prida List Data')
            # print(sublist_fvl_ng, 'Prida list data')
            # print(sublist_fvl_hetero, 'Prida list data')
            # print(sublist_fvl_homo, 'Prida list data')
            #
            # print(sublist_fvl_ng, 'Prida list data')
            # print(sublist_fvl_hetero, 'Prida list data')
            # print(sublist_fvl_homo, 'Prida list data')
            #
            # print(sublist_fvl_ng, 'Prida list data')
            # print(sublist_fvl_hetero, 'Prida list data')
            # print(sublist_fvl_homo, 'Prida list data')
            #
            # print(sublist_fvl_ng, 'Prida list data')
            # print(sublist_fvl_ng, 'Prida list data')
            # print(sublist_fvl_ng, 'Prida list data')
            #
            # print(sublist_fvl_ng, 'Prida list data')
            # print(sublist_fvl_ng, 'Prida list data')
            # print(sublist_fvl_ng, 'Prida list data')

            # sublist_factor = sublist_fvl_ng[factor_index][0]
            for factor_type in prida_list_data:
                if factor_type == 'fvl_ng':
                    pass
                    # context3['factor_type'] = 'fvl_ng'
                    # for factor_index in context3['index_array_age']:
                    #     print(sublist_fvl_ng[factor_index][0])
                    #     if sublist_fvl_ng[factor_index][0] == '1.0':
                    #         count_fvl_ng_mutations = count_fvl_ng_mutations + 1
                    #         if sublist_abort[factor_index][0] == '1.0':
                    #             count_fvl_ng_mutations_abort1 = count_fvl_ng_mutations_abort1 + 1
                    #         elif sublist_abort[factor_index][0] == '2.0':
                    #             count_fvl_ng_mutations_abort2 = count_fvl_ng_mutations_abort2 + 1
                    #         else:
                    #             count_fvl_ng_mutations_abort3 = count_fvl_ng_mutations_abort3 + 1
                    # context3['count_mutations_abort1'] = count_fvl_ng_mutations_abort1
                    # context3['percent_mutations_abort1'] = round(count_fvl_ng_mutations_abort1 * 100 /
                    #                                              clients_list, 2)
                    # context3['count_mutations_abort2'] = count_fvl_ng_mutations_abort2
                    # context3['percent_mutations_abort2'] = round(count_fvl_ng_mutations_abort2 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort3'] = count_fvl_ng_mutations_abort3
                    # context3['percent_mutations_abort3'] = round(count_fvl_ng_mutations_abort3 * 100 /
                    #                                              context3['clients_list'], 2)
                elif factor_type == 'fvl_hetero':
                    pass
                    # context3['factor_type'] = 'fvl_hetero'
                    # for factor_index in context3['index_array_age']:
                    #     print(sublist_fvl_hetero[factor_index][0])
                    #     if sublist_fvl_hetero[factor_index][0] == '1.0':
                    #         count_fvl_hetero_mutations = count_fvl_hetero_mutations + 1
                    #         if sublist_abort[factor_index][0] == '1.0':
                    #             count_fvl_hetero_mutations_abort1 = count_fvl_hetero_mutations_abort1 + 1
                    #         elif sublist_abort[factor_index][0] == '2.0':
                    #             count_fvl_hetero_mutations_abort2 = count_fvl_hetero_mutations_abort2 + 1
                    #         else:
                    #             count_fvl_hetero_mutations_abort3 = count_fvl_hetero_mutations_abort3 + 1
                    # context3['count_mutations_abort1'] = count_fvl_hetero_mutations_abort1
                    # context3['percent_mutations_abort1'] = round(count_fvl_hetero_mutations_abort1 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort2'] = count_fvl_hetero_mutations_abort2
                    # context3['percent_mutations_abort2'] = round(count_fvl_hetero_mutations_abort2 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort3'] = count_fvl_hetero_mutations_abort3
                    # context3['percent_mutations_abort3'] = round(count_fvl_hetero_mutations_abort3 * 100 /
                    #                                              context3['clients_list'], 2)

                elif factor_type == 'fvl_homo':
                    pass
                    # context3['factor_type'] = 'fvl_homo'
                    # for factor_index in context3['index_array_age']:
                    #     print(sublist_fvl_homo[factor_index][0])
                    #     if sublist_fvl_homo[factor_index][0] == '1.0':
                    #         count_fvl_homo_mutations = count_fvl_homo_mutations + 1
                    #         if sublist_abort[factor_index][0] == '1.0':
                    #             count_fvl_homo_mutations_abort1 = count_fvl_homo_mutations_abort1 + 1
                    #         elif sublist_abort[factor_index][0] == '2.0':
                    #             count_fvl_homo_mutations_abort2 = count_fvl_homo_mutations_abort2 + 1
                    #         else:
                    #             count_fvl_homo_mutations_abort3 = count_fvl_homo_mutations_abort3 + 1

                    # context3['count_mutations_abort1'] = count_fvl_homo_mutations_abort1
                    # context3['percent_mutations_abort1'] = round(count_fvl_homo_mutations_abort1 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort2'] = count_fvl_homo_mutations_abort2
                    # context3['percent_mutations_abort2'] = round(count_fvl_homo_mutations_abort2 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort3'] = count_fvl_homo_mutations_abort3
                    # context3['percent_mutations_abort3'] = round(count_fvl_homo_mutations_abort3 * 100 /
                    #                                              context3['clients_list'], 2)

                elif factor_type == 'prothr_ng':
                    pass
                    # context3['factor_type'] = 'prothr_ng'
                    # for factor_index in context3['index_array_age']:
                    #     print(sublist_prothr_ng[factor_index][0])
                    #     if sublist_prothr_ng[factor_index][0] == '1.0':
                    #         count_prothr_ng_mutations = count_prothr_ng_mutations + 1
                    #         if sublist_abort[factor_index][0] == '1.0':
                    #             count_prothr_ng_mutations_abort1 = count_prothr_ng_mutations_abort1 + 1
                    #         elif sublist_abort[factor_index][0] == '2.0':
                    #             count_prothr_ng_mutations_abort2 = count_prothr_ng_mutations_abort2 + 1
                    #         else:
                    #             count_prothr_ng_mutations_abort3 = count_prothr_ng_mutations_abort3 + 1

                    # context3['count_mutations_abort1'] = count_prothr_ng_mutations_abort1
                    # context3['percent_mutations_abort1'] = round(count_prothr_ng_mutations_abort1 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort2'] = count_prothr_ng_mutations_abort2
                    # context3['percent_mutations_abort2'] = round(count_prothr_ng_mutations_abort2 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort3'] = count_prothr_ng_mutations_abort3
                    # context3['percent_mutations_abort3'] = round(count_prothr_ng_mutations_abort3 * 100 /
                    #                                              context3['clients_list'], 2)

                elif factor_type == 'prothr_hetero':
                    pass
                    # context3['factor_type'] = 'prothr_hetero'
                    # for factor_index in context3['index_array_age']:
                    #     print(sublist_prothr_hetero[factor_index][0])
                    #     if sublist_prothr_hetero[factor_index][0] == '1.0':
                    #         count_prothr_hetero_mutations = count_prothr_hetero_mutations + 1
                    #         if sublist_abort[factor_index][0] == '1.0':
                    #             count_prothr_hetero_mutations_abort1 = count_prothr_hetero_mutations_abort1 + 1
                    #         elif sublist_abort[factor_index][0] == '2.0':
                    #             count_prothr_hetero_mutations_abort2 = count_prothr_hetero_mutations_abort2 + 1
                    #         else:
                    #             count_prothr_hetero_mutations_abort3 = count_prothr_hetero_mutations_abort3 + 1
                    # context3['count_mutations_abort1'] = count_prothr_hetero_mutations_abort1
                    # context3['percent_mutations_abort1'] = round(count_prothr_hetero_mutations_abort1 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort2'] = count_prothr_hetero_mutations_abort2
                    # context3['percent_mutations_abort2'] = round(count_prothr_hetero_mutations_abort2 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort3'] = count_prothr_hetero_mutations_abort3
                    # context3['percent_mutations_abort3'] = round(count_prothr_hetero_mutations_abort3 * 100 /
                    #                                              context3['clients_list'], 2)

                elif factor_type == 'prothr_homo':
                    pass
                    # context3['factor_type'] = 'prothr_homo'
                    # for factor_index in context3['index_array_age']:
                    #     print(sublist_prothr_homo[factor_index][0])
                    #     if sublist_prothr_homo[factor_index][0] == '1.0':
                    #         count_prothr_homo_mutations = count_prothr_homo_mutations + 1
                    #         if sublist_abort[factor_index][0] == '1.0':
                    #             count_prothr_homo_mutations_abort1 = count_prothr_homo_mutations_abort1 + 1
                    #         elif sublist_abort[factor_index][0] == '2.0':
                    #             count_prothr_homo_mutations_abort2 = count_prothr_homo_mutations_abort2 + 1
                    #         else:
                    #             count_prothr_homo_mutations_abort3 = count_prothr_homo_mutations_abort3 + 1

                    # context3['count_mutations_abort1'] = count_prothr_homo_mutations_abort1
                    # context3['percent_mutations_abort1'] = round(count_prothr_homo_mutations_abort1 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort2'] = count_prothr_homo_mutations_abort2
                    # context3['percent_mutations_abort2'] = round(count_prothr_homo_mutations_abort2 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort3'] = count_prothr_homo_mutations_abort3
                    # context3['percent_mutations_abort3'] = round(count_prothr_homo_mutations_abort3 * 100 /
                    #                                              context3['clients_list'], 2)

                elif factor_type == 'pai_ng':
                    pass
                    # context3['factor_type'] = 'pai_ng'
                    # for factor_index in context3['index_array_age']:
                    #     print(sublist_pai_ng[factor_index][0])
                    #     if sublist_pai_ng[factor_index][0] == '1.0':
                    #         count_pai_ng_mutations = count_pai_ng_mutations + 1
                    #         if sublist_abort[factor_index][0] == '1.0':
                    #             count_pai_ng_mutations_abort1 = count_pai_ng_mutations_abort1 + 1
                    #         elif sublist_abort[factor_index][0] == '2.0':
                    #             count_pai_ng_mutations_abort2 = count_pai_ng_mutations_abort2 + 1
                    #         else:
                    #             count_pai_ng_mutations_abort3 = count_pai_ng_mutations_abort3 + 1

                    # context3['count_mutations_abort1'] = count_pai_ng_mutations_abort1
                    # context3['percent_mutations_abort1'] = round(count_pai_ng_mutations_abort1 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort2'] = count_pai_ng_mutations_abort2
                    # context3['percent_mutations_abort2'] = round(count_pai_ng_mutations_abort2 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort3'] = count_pai_ng_mutations_abort3
                    # context3['percent_mutations_abort3'] = round(count_pai_ng_mutations_abort3 * 100 /
                    #                                              context3['clients_list'], 2)

                elif factor_type == 'pai_hetero':
                    pass
                    # context3['factor_type'] = 'pai_hetero'
                    # for factor_index in context3['index_array_age']:
                    #     print(sublist_pai_hetero[factor_index][0])
                    #     if sublist_pai_hetero[factor_index][0] == '1.0':
                    #         count_pai_hetero_mutations = count_pai_hetero_mutations + 1
                    #         if sublist_abort[factor_index][0] == '1.0':
                    #             count_pai_hetero_mutations_abort1 = count_pai_hetero_mutations_abort1 + 1
                    #         elif sublist_abort[factor_index][0] == '2.0':
                    #             count_pai_hetero_mutations_abort2 = count_pai_hetero_mutations_abort2 + 1
                    #         else:
                    #             count_pai_hetero_mutations_abort3 = count_pai_hetero_mutations_abort3 + 1

                    # context3['count_mutations_abort1'] = count_pai_hetero_mutations_abort1
                    # context3['percent_mutations_abort1'] = round(count_pai_hetero_mutations_abort1 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort2'] = count_pai_hetero_mutations_abort2
                    # context3['percent_mutations_abort2'] = round(count_pai_hetero_mutations_abort2 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort3'] = count_pai_hetero_mutations_abort3
                    # context3['percent_mutations_abort3'] = round(count_pai_hetero_mutations_abort3 * 100 /
                    #                                              context3['clients_list'], 2)

                elif factor_type == 'pai_homo':
                    pass
                    # context3['factor_type'] = 'pai_homo'
                    # for factor_index in context3['index_array_age']:
                    #     print(sublist_pai_homo[factor_index][0])
                    #     if sublist_pai_homo[factor_index][0] == '1.0':
                    #         count_pai_homo_mutations = count_pai_homo_mutations + 1
                    #         if sublist_abort[factor_index][0] == '1.0':
                    #             count_pai_homo_mutations_abort1 = count_pai_homo_mutations_abort1 + 1
                    #         elif sublist_abort[factor_index][0] == '2.0':
                    #             count_pai_homo_mutations_abort2 = count_pai_homo_mutations_abort2 + 1
                    #         else:
                    #             count_pai_homo_mutations_abort3 = count_pai_homo_mutations_abort3 + 1

                    # context3['count_mutations_abort1'] = count_pai_homo_mutations_abort1
                    # context3['percent_mutations_abort1'] = round(count_pai_homo_mutations_abort1 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort2'] = count_pai_homo_mutations_abort2
                    # context3['percent_mutations_abort2'] = round(count_pai_homo_mutations_abort2 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort3'] = count_pai_homo_mutations_abort3
                    # context3['percent_mutations_abort3'] = round(count_pai_homo_mutations_abort3 * 100 /
                    #                                              context3['clients_list'], 2)

                elif factor_type == 'mthfr_ng':
                    pass
                    # context3['factor_type'] = 'mthfr_ng'
                    # for factor_index in context3['index_array_age']:
                    #     print(sublist_mthfr_ng[factor_index][0])
                    #     if sublist_mthfr_ng[factor_index][0] == '1.0':
                    #         count_mthfr_ng_mutations = count_mthfr_ng_mutations + 1
                    #         if sublist_abort[factor_index][0] == '1.0':
                    #             count_mthfr_ng_mutations_abort1 = count_mthfr_ng_mutations_abort1 + 1
                    #         elif sublist_abort[factor_index][0] == '2.0':
                    #             count_mthfr_ng_mutations_abort2 = count_mthfr_ng_mutations_abort2 + 1
                    #         else:
                    #             count_mthfr_ng_mutations_abort3 = count_mthfr_ng_mutations_abort3 + 1

                    # context3['count_mutations_abort1'] = count_mthfr_ng_mutations_abort1
                    # context3['percent_mutations_abort1'] = round(count_mthfr_ng_mutations_abort1 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort2'] = count_mthfr_ng_mutations_abort2
                    # context3['percent_mutations_abort2'] = round(count_mthfr_ng_mutations_abort2 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort3'] = count_mthfr_ng_mutations_abort3
                    # context3['percent_mutations_abort3'] = round(count_mthfr_ng_mutations_abort3 * 100 /
                    #                                              context3['clients_list'], 2)

                elif factor_type == 'mthfr_hetero':
                    pass
                    # context3['factor_type'] = 'mthfr_hetero'
                    # for factor_index in context3['index_array_age']:
                    #     print(sublist_mthfr_hetero[factor_index][0])
                    #     if sublist_mthfr_hetero[factor_index][0] == '1.0':
                    #         count_mthfr_hetero_mutations = count_mthfr_hetero_mutations + 1
                    #         if sublist_abort[factor_index][0] == '1.0':
                    #             count_mthfr_hetero_mutations_abort1 = count_mthfr_hetero_mutations_abort1 + 1
                    #         elif sublist_abort[factor_index][0] == '2.0':
                    #             count_mthfr_hetero_mutations_abort2 = count_mthfr_hetero_mutations_abort2 + 1
                    #         else:
                    #             count_mthfr_hetero_mutations_abort3 = count_mthfr_hetero_mutations_abort3 + 1

                    # context3['count_mutations_abort1'] = count_mthfr_hetero_mutations_abort1
                    # context3['percent_mutations_abort1'] = round(count_mthfr_hetero_mutations_abort1 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort2'] = count_mthfr_hetero_mutations_abort2
                    # context3['percent_mutations_abort2'] = round(count_mthfr_hetero_mutations_abort2 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort3'] = count_mthfr_hetero_mutations_abort3
                    # context3['percent_mutations_abort3'] = round(count_mthfr_hetero_mutations_abort3 * 100 /
                    #                                              context3['clients_list'], 2)

                elif factor_type == 'mthfr_homo':
                    pass
                    # context3['factor_type'] = 'mthfr_homo'
                    # for factor_index in context3['index_array_age']:
                    #     print(sublist_mthfr_homo[factor_index][0])
                    #     if sublist_mthfr_homo[factor_index][0] == '1.0':
                    #         count_mthfr_homo_mutations = count_mthfr_homo_mutations + 1
                    #         if sublist_abort[factor_index][0] == '1.0':
                    #             count_mthfr_homo_mutations_abort1 = count_mthfr_homo_mutations_abort1 + 1
                    #         elif sublist_abort[factor_index][0] == '2.0':
                    #             count_mthfr_homo_mutations_abort2 = count_mthfr_homo_mutations_abort2 + 1
                    #         else:
                    #             count_mthfr_homo_mutations_abort3 = count_mthfr_homo_mutations_abort3 + 1

                    # context3['count_mutations_abort1'] = count_mthfr_homo_mutations_abort1
                    # context3['percent_mutations_abort1'] = round(count_mthfr_homo_mutations_abort1 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort2'] = count_mthfr_homo_mutations_abort2
                    # context3['percent_mutations_abort2'] = round(count_mthfr_homo_mutations_abort2 * 100 /
                    #                                              context3['clients_list'], 2)
                    # context3['count_mutations_abort3'] = count_mthfr_homo_mutations_abort3
                    # context3['percent_mutations_abort3'] = round(count_mthfr_homo_mutations_abort3 * 100 /
                    #                                              context3['clients_list'], 2)
                else:
                    pass
    if request.method == 'POST':
        if 'btn_patients_more_mutations' in request.POST:
            print('More Mutations!!!')
            print('List FVL Hetero', list_fvl_hetero)
        else:
            print('More 111')

    if request.method == 'POST':
        if 'submit' in request.POST:
            context3['end_line'] = int(end_line)
            context3['start_line'] = int(start_line)
            context3['clients_list'] = int(end_line) - int(start_line)
            clients_list = context3['clients_list']

            sublist = slice(int(start_line), int(end_line))
            print('OK')
            print(prida_list_data)

            sublist_age = list_age[sublist]
            print(sublist_age)
            sublist_abort = list_abort[sublist]
            print(sublist_abort)

            count_age1 = 0
            count_age2 = 0
            count_age3 = 0

            index_array_age1 = []
            index_array_age2 = []
            index_array_age3 = []

            count_index_array_age = 0

            for age in sublist_age:
                if 20 <= age[0] <= 30:
                    count_age1 = count_age1 + 1
                    index_array_age1.append(count_index_array_age)
                elif 31 <= age[0] <= 40:
                    count_age2 = count_age2 + 1
                    index_array_age2.append(count_index_array_age)
                elif 41 <= age[0] <= 50:
                    count_age3 = count_age3 + 1
                    index_array_age3.append(count_index_array_age)
                count_index_array_age = count_index_array_age + 1

            print(index_array_age1, 'OK Age1')
            print(index_array_age2, 'OK Age2')
            print(index_array_age3, 'OK Age3')

            for age in prida_age_list:
                if age == 'age1':
                    context3['index_array_age'] = index_array_age1
                    context3['age_interval'] = age
                elif age == 'age2':
                    context3['index_array_age'] = index_array_age2
                    context3['age_interval'] = age
                elif age == 'age3':
                    context3['index_array_age'] = index_array_age3
                    context3['age_interval'] = age

            # print(context3['index_array_age'], 'OK')

            count_abort1 = 0
            count_abort2 = 0
            count_abort3 = 0

            index_array_abort1 = []
            index_array_abort2 = []
            index_array_abort3 = []

            count_index_array_abort = 0

            for abort in context3['index_array_age']:
                if sublist_abort[abort][0] == '1.0':
                    count_abort1 = count_abort1 + 1
                    index_array_abort1.append(abort)
                elif sublist_abort[abort][0] == '2.0':
                    count_abort2 = count_abort2 + 1
                    index_array_abort2.append(abort)
                elif sublist_abort[abort][0] != '?' or sublist_abort[abort][0] != '2.0' or sublist_abort[abort][0] != '1.0':
                    count_abort3 = count_abort3 + 1
                    index_array_abort3.append(abort)

                count_index_array_abort = count_index_array_abort + 1

            print(index_array_abort1, 'OK')
            print(index_array_abort2, 'OK')
            print(index_array_abort3, 'OK')

            for abort in prida_abort_list:
                if abort == 'abort_1':
                    context3['index_array_abort'] = index_array_abort1
                    context3['abort_variant'] = abort
                elif abort == 'abort_2':
                    context3['index_array_abort'] = index_array_abort2
                    context3['abort_variant'] = abort
                elif abort == 'abort_3':
                    context3['index_array_abort'] = index_array_abort3
                    context3['abort_variant'] = abort

            context3['number_abort_patients'] = len(context3['index_array_abort'])

            print(context3['index_array_abort'], 'OK', context3['number_abort_patients'])

            sublist_fvl_ng = list_fvl_ng[sublist]
            sublist_fvl_hetero = list_fvl_hetero[sublist]
            sublist_fvl_homo = list_fvl_homo[sublist]

            sublist_prothr_ng = list_prothr_ng[sublist]
            sublist_prothr_hetero = list_prothr_hetero[sublist]
            sublist_prothr_homo = list_prothr_homo[sublist]

            sublist_pai_ng = list_pai_ng[sublist]
            sublist_pai_hetero = list_pai_hetero[sublist]
            sublist_pai_homo = list_pai_homo[sublist]

            sublist_mthfr_ng = list_mthfr_ng[sublist]
            sublist_mthfr_hetero = list_mthfr_hetero[sublist]
            sublist_mthfr_homo = list_mthfr_homo[sublist]

            count_fvl_ng = 0
            count_fvl_hetero = 0
            count_fvl_homo = 0

            count_prothr_ng = 0
            count_prothr_hetero = 0
            count_prothr_homo = 0

            count_pai_ng = 0
            count_pai_hetero = 0
            count_pai_homo = 0

            count_mthfr_ng = 0
            count_mthfr_hetero = 0
            count_mthfr_homo = 0
            print(prida_list_data)
            for f in prida_list_data:
                print(f, 'OK2')
                if f == 'fvl_ng':
                    for fvl_ng in context3['index_array_abort']:
                        if sublist_fvl_ng[fvl_ng][0] == '1.0':
                            count_fvl_ng = count_fvl_ng + 1
                    print(count_fvl_ng, 'fvl_ng')
                    if count_fvl_ng > 0:
                        mutations_age1_abort1_fvl_ng_percent = count_fvl_ng / len(context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_fvl_ng_percent'] = mutations_age1_abort1_fvl_ng_percent
                    else:
                        context3['mutations_age1_abort1_fvl_ng_percent'] = 0
                elif f == 'fvl_hetero':
                    for fvl_hetero in context3['index_array_abort']:
                        if sublist_fvl_hetero[fvl_hetero][0] == '1.0':
                            count_fvl_hetero = count_fvl_hetero + 1
                    print(count_fvl_hetero, 'fvl_hetero')
                    if count_fvl_hetero > 0:
                        mutations_age1_abort1_fvl_hetero_percent = count_fvl_hetero / len(context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_fvl_hetero_percent'] = mutations_age1_abort1_fvl_hetero_percent
                    else:
                        context3['mutations_age1_abort1_fvl_hetero_percent'] = 0
                elif f == 'fvl_homo':
                    for fvl_homo in context3['index_array_abort']:
                        if sublist_fvl_homo[fvl_homo][0] == '1.0':
                            count_fvl_homo = count_fvl_homo + 1
                    print(count_fvl_homo, 'fvl_homo')
                    if count_fvl_homo > 0:
                        mutations_age1_abort1_fvl_homo_percent = count_fvl_homo / len(context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_fvl_homo_percent'] = mutations_age1_abort1_fvl_homo_percent
                    else:
                        context3['mutations_age1_abort1_fvl_homo_percent'] = 0
                elif f == 'prothr_ng':
                    for prothr_ng in context3['index_array_abort']:
                        if sublist_prothr_ng[prothr_ng][0] == '1.0':
                            count_prothr_ng = count_prothr_ng + 1
                    print(count_prothr_ng, 'prothr_ng')
                    if count_prothr_ng > 0:
                        mutations_age1_abort1_prothr_ng_percent = count_prothr_ng / len(context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_prothr_ng_percent'] = mutations_age1_abort1_prothr_ng_percent
                    else:
                        context3['mutations_age1_abort1_prothr_ng_percent'] = 0
                elif f == 'prothr_hetero':
                    for prothr_hetero in context3['index_array_abort']:
                        if sublist_prothr_hetero[prothr_hetero][0] == '1.0':
                            count_prothr_hetero = count_prothr_hetero + 1
                    print(count_prothr_hetero, 'prothr_hetero')
                    if count_prothr_hetero > 0:
                        mutations_age1_abort1_prothr_hetero_percent = count_prothr_hetero / len(context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_prothr_hetero_percent'] = mutations_age1_abort1_prothr_hetero_percent
                    else:
                        context3['mutations_age1_abort1_prothr_hetero_percent'] = 0
                elif f == 'prothr_homo':
                    for prothr_homo in context3['index_array_abort']:
                        if sublist_prothr_homo[prothr_homo][0] == '1.0':
                            count_prothr_homo = count_prothr_homo + 1
                    print(count_prothr_homo, 'prothr_homo')
                    if count_prothr_homo > 0:
                        mutations_age1_abort1_prothr_homo_percent = count_prothr_homo / len(context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_prothr_homo_percent'] = mutations_age1_abort1_prothr_homo_percent
                    else:
                        context3['mutations_age1_abort1_prothr_homo_percent'] = 0
                elif f == 'pai_ng':
                    for pai_ng in context3['index_array_abort']:
                        if sublist_pai_ng[pai_ng][0] == '1.0':
                            count_pai_ng = count_pai_ng + 1
                    print(count_pai_ng, 'pai_ng')
                    if count_pai_ng > 0:
                        mutations_age1_abort1_pai_ng_percent = count_pai_ng / len(context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_pai_ng_percent'] = mutations_age1_abort1_pai_ng_percent
                    else:
                        context3['mutations_age1_abort1_pai_ng_percent'] = 0

                elif f == 'pai_hetero':
                    for pai_hetero in context3['index_array_abort']:
                        if sublist_pai_hetero[pai_hetero][0] == '1.0':
                            count_pai_hetero = count_pai_hetero + 1
                    print(count_pai_hetero, 'pai_hetero')
                    if count_pai_hetero > 0:
                        mutations_age1_abort1_pai_hetero_percent = count_pai_hetero / len(context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_pai_hetero_percent'] = mutations_age1_abort1_pai_hetero_percent
                    else:
                        context3['mutations_age1_abort1_pai_hetero_percent'] = 0
                elif f == 'pai_homo':
                    for pai_homo in context3['index_array_abort']:
                        if sublist_pai_homo[pai_homo][0] == '1.0':
                            count_pai_homo = count_pai_homo + 1
                    print(count_pai_homo, 'pai_homo')
                    if count_pai_homo > 0:
                        mutations_age1_abort1_pai_homo_percent = count_pai_homo / len(context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_pai_homo_percent'] = mutations_age1_abort1_pai_homo_percent
                    else:
                        context3['mutations_age1_abort1_pai_homo_percent'] = 0
                elif f == 'mthfr_ng':
                    for mthfr_ng in context3['index_array_abort']:
                        if sublist_mthfr_ng[mthfr_ng][0] == '1.0':
                            count_mthfr_ng = count_mthfr_ng + 1
                    print(count_mthfr_ng, 'mthfr_ng')
                    if count_mthfr_ng > 0:
                        mutations_age1_abort1_mthfr_ng_percent = count_mthfr_ng / len(context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_mthfr_ng_percent'] = mutations_age1_abort1_mthfr_ng_percent
                    else:
                        context3['mutations_age1_abort1_mthfr_ng_percent'] = 0
                elif f == 'mthfr_hetero':
                    for mthfr_hetero in context3['index_array_abort']:
                        if sublist_mthfr_hetero[mthfr_hetero][0] == '1.0':
                            count_mthfr_hetero = count_mthfr_hetero + 1
                    print(count_mthfr_hetero, 'mthfr_hetero')
                    if count_mthfr_hetero > 0:
                        mutations_age1_abort1_mthfr_hetero_percent = count_mthfr_hetero / len(context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_mthfr_hetero_percent'] = mutations_age1_abort1_mthfr_hetero_percent
                    else:
                        context3['mutations_age1_abort1_mthfr_hetero_percent'] = 0
                elif f == 'mthfr_homo':
                    for mthfr_homo in context3['index_array_abort']:
                        if sublist_mthfr_homo[mthfr_homo][0] == '1.0':
                            count_mthfr_homo = count_mthfr_homo + 1
                    print(count_mthfr_homo, 'mthfr_homo')
                    if count_mthfr_homo > 0:
                        mutations_age1_abort1_mthfr_homo_percent = count_mthfr_homo / len(context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_mthfr_homo_percent'] = mutations_age1_abort1_mthfr_homo_percent
                    else:
                        context3['mutations_age1_abort1_mthfr_homo_percent'] = 0

            context3['mutations_fvl_ng'] = count_fvl_ng
            context3['mutations_fvl_hetero'] = count_fvl_hetero
            context3['mutations_fvl_homo'] = count_fvl_homo
            context3['mutations_prothr_ng'] = count_prothr_ng
            context3['mutations_prothr_hetero'] = count_prothr_hetero
            context3['mutations_prothr_homo'] = count_prothr_homo
            context3['mutations_pai_ng'] = count_pai_ng
            context3['mutations_pai_hetero'] = count_pai_hetero
            context3['mutations_pai_homo'] = count_pai_homo
            context3['mutations_mthfr_ng'] = count_mthfr_ng
            context3['mutations_mthfr_hetero'] = count_mthfr_hetero
            context3['mutations_mthfr_homo'] = count_mthfr_homo

            count_fvl_ng_mutations = 0
            count_fvl_ng_mutations_abort1 = 0
            count_fvl_ng_mutations_abort2 = 0
            count_fvl_ng_mutations_abort3 = 0

            count_fvl_hetero_mutations = 0
            count_fvl_hetero_mutations_abort1 = 0
            count_fvl_hetero_mutations_abort2 = 0
            count_fvl_hetero_mutations_abort3 = 0

            count_fvl_homo_mutations = 0
            count_fvl_homo_mutations_abort1 = 0
            count_fvl_homo_mutations_abort2 = 0
            count_fvl_homo_mutations_abort3 = 0

            count_prothr_ng_mutations = 0
            count_prothr_ng_mutations_abort1 = 0
            count_prothr_ng_mutations_abort2 = 0
            count_prothr_ng_mutations_abort3 = 0

            count_prothr_hetero_mutations = 0
            count_prothr_hetero_mutations_abort1 = 0
            count_prothr_hetero_mutations_abort2 = 0
            count_prothr_hetero_mutations_abort3 = 0

            count_prothr_homo_mutations = 0
            count_prothr_homo_mutations_abort1 = 0
            count_prothr_homo_mutations_abort2 = 0
            count_prothr_homo_mutations_abort3 = 0

            count_pai_ng_mutations = 0
            count_pai_ng_mutations_abort1 = 0
            count_pai_ng_mutations_abort2 = 0
            count_pai_ng_mutations_abort3 = 0

            count_pai_hetero_mutations = 0
            count_pai_hetero_mutations_abort1 = 0
            count_pai_hetero_mutations_abort2 = 0
            count_pai_hetero_mutations_abort3 = 0

            count_pai_homo_mutations = 0
            count_pai_homo_mutations_abort1 = 0
            count_pai_homo_mutations_abort2 = 0
            count_pai_homo_mutations_abort3 = 0

            count_mthfr_ng_mutations = 0
            count_mthfr_ng_mutations_abort1 = 0
            count_mthfr_ng_mutations_abort2 = 0
            count_mthfr_ng_mutations_abort3 = 0

            count_mthfr_hetero_mutations = 0
            count_mthfr_hetero_mutations_abort1 = 0
            count_mthfr_hetero_mutations_abort2 = 0
            count_mthfr_hetero_mutations_abort3 = 0

            count_mthfr_homo_mutations = 0
            count_mthfr_homo_mutations_abort1 = 0
            count_mthfr_homo_mutations_abort2 = 0
            count_mthfr_homo_mutations_abort3 = 0

            print(context3['age_interval'], 'New')
            print(context3['index_array_age'], 'New', sublist_age)
            print(prida_list_data, 'Prida List Data')
            # for factor_type in prida_list_data:
            #     if factor_type == 'fvl_ng':
            #         for factor_index in context3['index_array_age']:
            #             print(sublist_fvl_ng[factor_index][0])
            #             if sublist_fvl_ng[factor_index][0] == '1.0':
            #                 count_fvl_ng_mutations = count_fvl_ng_mutations + 1
            #                 if sublist_abort[factor_index][0] == '1.0':
            #                     count_fvl_ng_mutations_abort1 = count_fvl_ng_mutations_abort1 + 1
            #                 elif sublist_abort[factor_index][0] == '2.0':
            #                     count_fvl_ng_mutations_abort2 = count_fvl_ng_mutations_abort2 + 1
            #                 else:
            #                     count_fvl_ng_mutations_abort3 = count_fvl_ng_mutations_abort3 + 1
            #     elif factor_type == 'fvl_hetero':
            #         for factor_index in context3['index_array_age']:
            #             print(sublist_fvl_hetero[factor_index][0])
            #             if sublist_fvl_hetero[factor_index][0] == '1.0':
            #                 count_fvl_hetero_mutations = count_fvl_hetero_mutations + 1
            #                 if sublist_abort[factor_index][0] == '1.0':
            #                     count_fvl_hetero_mutations_abort1 = count_fvl_hetero_mutations_abort1 + 1
            #                 elif sublist_abort[factor_index][0] == '2.0':
            #                     count_fvl_hetero_mutations_abort2 = count_fvl_hetero_mutations_abort2 + 1
            #                 else:
            #                     count_fvl_hetero_mutations_abort3 = count_fvl_hetero_mutations_abort3 + 1
            #     elif factor_type == 'fvl_homo':
            #         for factor_index in context3['index_array_age']:
            #             print(sublist_fvl_homo[factor_index][0])
            #             if sublist_fvl_homo[factor_index][0] == '1.0':
            #                 count_fvl_homo_mutations = count_fvl_homo_mutations + 1
            #                 if sublist_abort[factor_index][0] == '1.0':
            #                     count_fvl_homo_mutations_abort1 = count_fvl_homo_mutations_abort1 + 1
            #                 elif sublist_abort[factor_index][0] == '2.0':
            #                     count_fvl_homo_mutations_abort2 = count_fvl_homo_mutations_abort2 + 1
            #                 else:
            #                     count_fvl_homo_mutations_abort3 = count_fvl_homo_mutations_abort3 + 1
            #     elif factor_type == 'prothr_ng':
            #         for factor_index in context3['index_array_age']:
            #             print(sublist_prothr_ng[factor_index][0])
            #             if sublist_prothr_ng[factor_index][0] == '1.0':
            #                 count_prothr_ng_mutations = count_prothr_ng_mutations + 1
            #                 if sublist_abort[factor_index][0] == '1.0':
            #                     count_prothr_ng_mutations_abort1 = count_prothr_ng_mutations_abort1 + 1
            #                 elif sublist_abort[factor_index][0] == '2.0':
            #                     count_prothr_ng_mutations_abort2 = count_prothr_ng_mutations_abort2 + 1
            #                 else:
            #                     count_prothr_ng_mutations_abort3 = count_prothr_ng_mutations_abort3 + 1
            #     elif factor_type == 'prothr_hetero':
            #         for factor_index in context3['index_array_age']:
            #             print(sublist_prothr_hetero[factor_index][0])
            #             if sublist_prothr_hetero[factor_index][0] == '1.0':
            #                 count_prothr_hetero_mutations = count_prothr_hetero_mutations + 1
            #                 if sublist_abort[factor_index][0] == '1.0':
            #                     count_prothr_hetero_mutations_abort1 = count_prothr_hetero_mutations_abort1 + 1
            #                 elif sublist_abort[factor_index][0] == '2.0':
            #                     count_prothr_hetero_mutations_abort2 = count_prothr_hetero_mutations_abort2 + 1
            #                 else:
            #                     count_prothr_hetero_mutations_abort3 = count_prothr_hetero_mutations_abort3 + 1
            #     elif factor_type == 'prothr_homo':
            #         for factor_index in context3['index_array_age']:
            #             print(sublist_prothr_homo[factor_index][0])
            #             if sublist_prothr_homo[factor_index][0] == '1.0':
            #                 count_prothr_homo_mutations = count_prothr_homo_mutations + 1
            #                 if sublist_abort[factor_index][0] == '1.0':
            #                     count_prothr_homo_mutations_abort1 = count_prothr_homo_mutations_abort1 + 1
            #                 elif sublist_abort[factor_index][0] == '2.0':
            #                     count_prothr_homo_mutations_abort2 = count_prothr_homo_mutations_abort2 + 1
            #                 else:
            #                     count_prothr_homo_mutations_abort3 = count_prothr_homo_mutations_abort3 + 1
            #     elif factor_type == 'pai_ng':
            #         for factor_index in context3['index_array_age']:
            #             print(sublist_pai_ng[factor_index][0])
            #             if sublist_pai_ng[factor_index][0] == '1.0':
            #                 count_pai_ng_mutations = count_pai_ng_mutations + 1
            #                 if sublist_abort[factor_index][0] == '1.0':
            #                     count_pai_ng_mutations_abort1 = count_pai_ng_mutations_abort1 + 1
            #                 elif sublist_abort[factor_index][0] == '2.0':
            #                     count_pai_ng_mutations_abort2 = count_pai_ng_mutations_abort2 + 1
            #                 else:
            #                     count_pai_ng_mutations_abort3 = count_pai_ng_mutations_abort3 + 1
            #     elif factor_type == 'pai_hetero':
            #         for factor_index in context3['index_array_age']:
            #             print(sublist_pai_hetero[factor_index][0])
            #             if sublist_pai_hetero[factor_index][0] == '1.0':
            #                 count_pai_hetero_mutations = count_pai_hetero_mutations + 1
            #                 if sublist_abort[factor_index][0] == '1.0':
            #                     count_pai_hetero_mutations_abort1 = count_pai_hetero_mutations_abort1 + 1
            #                 elif sublist_abort[factor_index][0] == '2.0':
            #                     count_pai_hetero_mutations_abort2 = count_pai_hetero_mutations_abort2 + 1
            #                 else:
            #                     count_pai_hetero_mutations_abort3 = count_pai_hetero_mutations_abort3 + 1
            #     elif factor_type == 'pai_homo':
            #         for factor_index in context3['index_array_age']:
            #             print(sublist_pai_homo[factor_index][0])
            #             if sublist_pai_homo[factor_index][0] == '1.0':
            #                 count_pai_homo_mutations = count_pai_homo_mutations + 1
            #                 if sublist_abort[factor_index][0] == '1.0':
            #                     count_pai_homo_mutations_abort1 = count_pai_homo_mutations_abort1 + 1
            #                 elif sublist_abort[factor_index][0] == '2.0':
            #                     count_pai_homo_mutations_abort2 = count_pai_homo_mutations_abort2 + 1
            #                 else:
            #                     count_pai_homo_mutations_abort3 = count_pai_homo_mutations_abort3 + 1
            #     elif factor_type == 'mthfr_ng':
            #         for factor_index in context3['index_array_age']:
            #             print(sublist_mthfr_ng[factor_index][0])
            #             if sublist_mthfr_ng[factor_index][0] == '1.0':
            #                 count_mthfr_ng_mutations = count_mthfr_ng_mutations + 1
            #                 if sublist_abort[factor_index][0] == '1.0':
            #                     count_mthfr_ng_mutations_abort1 = count_mthfr_ng_mutations_abort1 + 1
            #                 elif sublist_abort[factor_index][0] == '2.0':
            #                     count_mthfr_ng_mutations_abort2 = count_mthfr_ng_mutations_abort2 + 1
            #                 else:
            #                     count_mthfr_ng_mutations_abort3 = count_mthfr_ng_mutations_abort3 + 1



                #         elif sublist_fvl_hetero[factor_index][0] == '1.0':
                #             count_fvl_hetero_mutations = count_fvl_hetero_mutations + 1
                #             if sublist_abort[factor_index][0] == '1.0':
                #                 count_fvl_hetero_mutations_abort1 = count_fvl_hetero_mutations_abort1 + 1
                #             elif sublist_abort[factor_index][0] == '2.0':
                #                 count_fvl_hetero_mutations_abort2 = count_fvl_hetero_mutations_abort2 + 1
                #             else:
                #                 count_fvl_hetero_mutations_abort3 = count_fvl_hetero_mutations_abort3 + 1
                # # else:
                #     count_fvl_ng_mutations = count_fvl_ng_mutations + 1
                #     if sublist_abort[fvl_ng][0] == '1.0':
                #         count_fvl_ng_mutations_abort1 = count_fvl_ng_mutations_abort1 + 1
                #     elif sublist_abort[fvl_ng][0] == '2.0':
                #         count_fvl_ng_mutations_abort2 = count_fvl_ng_mutations_abort2 + 1
                #     else:
                #         count_fvl_ng_mutations_abort3 = count_fvl_ng_mutations_abort3 + 1

            # print(count_fvl_ng_mutations, 'New')
            # print(count_fvl_ng_mutations_abort1, 'Abort1 FVL Ng')
            # print(count_fvl_ng_mutations_abort2, 'Abort2 FVL Ng')
            # print(count_fvl_ng_mutations_abort3, 'Abort3 FVL Ng')
            #
            # print(count_fvl_hetero_mutations_abort1, 'Abort1 FVL Hetero')
            # print(count_fvl_hetero_mutations_abort2, 'Abort2 FVL Hetero')
            # print(count_fvl_hetero_mutations_abort3, 'Abort3 FVL Hetero')
            #
            # print(context3['mutations_fvl_hetero'])





            print(sublist_fvl_hetero)
            context3['sublist_abort'] = sublist_abort

            ####################################################
            ############## Start Count Age #####################
            ####################################################
            print('Tihomir')
            for i in range(0, len(prida_list_data)):
                if prida_list_data[i] == 'age1':
                    count_age1 = 0
                    list_num_array_data = []
                    index_sublist_age1 = 0
                    for age1 in sublist_age:
                        if 20 <= age1[0] <= 30:
                            count_age1 = count_age1 + 1
                            list_num_array_data.append(index_sublist_age1)
                        index_sublist_age1 = index_sublist_age1 + 1
                    context3['num_array_data_age1'] = list_num_array_data
                    print(context3['num_array_data_age1'])

                elif prida_list_data[i] == 'age2':
                    list_num_array_data = []
                    index_sublist_age2 = 0
                    count_age2 = 0
                    for age2 in sublist_age:
                        if 31 <= age2[0] <= 40:
                            count_age2 = count_age2 + 1
                            list_num_array_data.append(index_sublist_age2)
                        index_sublist_age2 = index_sublist_age2 + 1
                    # print(count_age2, list_num_array_data)
                    context3['num_array_data_age2'] = list_num_array_data
                    print(context3['num_array_data_age2'])

                elif prida_list_data[i] == 'age3':
                    list_num_array_data = []
                    index_sublist_age3 = 0
                    count_age3 = 0
                    for age3 in sublist_age:
                        if 41 <= age3[0] <= 50:
                            count_age3 = count_age3 + 1
                            list_num_array_data.append(index_sublist_age3)
                        index_sublist_age3 = index_sublist_age3 + 1
                    # print(count_age3, list_num_array_data)
                    context3['num_array_data_age3'] = list_num_array_data
                    print(context3['num_array_data_age3'])


            print('End Tihomir')
            ####################################################
            ############## End Count Age #######################
            ####################################################
            index_data_array_age1_abort1 = []
            index_data_array_age1_abort2 = []
            index_data_array_age1_abort3 = []

            num_array_abort2 = []
            num_array_abort3 = []
            num_patients_abort1 = 0
            num_patients_abort2 = 0
            num_patients_abort_more = 0
            # for index_array_age1 in context3['num_array_data_age1']:
            #     if sublist_abort[index_array_age1][0] == '1.0':
            #         num_patients_abort1 = num_patients_abort1 + 1
            #         index_data_array_age1_abort1.append(index_array_age1)
            #         print(index_data_array_age1_abort1, 'Bravo 1')
            #         context3['num_patients_abort1'] = num_patients_abort1
            #         context3['index_data_array_age1_abort1'] = index_data_array_age1_abort1
            #         context3['num_patients_abort1'] = num_patients_abort1
            #     elif sublist_abort[index_array_age1][0] == '2.0':
            #         num_patients_abort2 = num_patients_abort2 + 1
            #         num_array_abort2.append(index_array_age1)
            #         print(num_array_abort2, 'Bravo 2')
            #         context3['num_patients_abort2'] = num_patients_abort2
            #         context3['index_data_array_age1_abort2'] = index_data_array_age1_abort2
            #
            #     elif sublist_abort[index_array_age1][0] > '2.0':
            #         num_patients_abort_more = num_patients_abort_more + 1
            #         num_array_abort3.append(index_array_age1)
            #         print(num_array_abort3, 'Bravo 3')
            #         context3['num_patients_abort_more'] = num_patients_abort_more
            #         context3['index_data_array_age1_abort3'] = index_data_array_age1_abort3


            count_fvl_ng_age1_abort1 = 0
            count_fvl_hetero_age1_abort1 = 0
            count_fvl_homo_age1_abort1 = 0

            count_prothr_ng_age1_abort1 = 0
            count_prothr_hetero_age1_abort1 = 0
            count_prothr_homo_age1_abort1 = 0

            count_pai_ng_age1_abort1 = 0
            count_pai_hetero_age1_abort1 = 0
            count_pai_homo_age1_abort1 = 0

            count_mthfr_ng_age1_abort1 = 0
            count_mthfr_hetero_age1_abort1 = 0
            count_mthfr_homo_age1_abort1 = 0

            for index_age1_abort1 in index_data_array_age1_abort1:
                if sublist_fvl_ng[index_age1_abort1][0] == '1.0':
                    count_fvl_ng_age1_abort1 = count_fvl_ng_age1_abort1 + 1

                elif sublist_fvl_hetero[index_age1_abort1][0] == '1.0':
                    count_fvl_hetero_age1_abort1 = count_fvl_hetero_age1_abort1 + 1

                elif sublist_fvl_homo[index_age1_abort1][0] == '1.0':
                    count_fvl_homo_age1_abort1 = count_fvl_homo_age1_abort1 + 1

                elif sublist_prothr_ng[index_age1_abort1][0] == '1.0':
                    count_prothr_ng_age1_abort1 = count_prothr_ng_age1_abort1 + 1

                elif sublist_prothr_hetero[index_age1_abort1][0] == '1.0':
                    count_prothr_hetero_age1_abort1 = count_prothr_hetero_age1_abort1 + 1

                elif sublist_prothr_homo[index_age1_abort1][0] == '1.0':
                    count_prothr_homo_age1_abort1 = count_prothr_homo_age1_abort1 + 1

                elif sublist_pai_ng[index_age1_abort1][0] == '1.0':
                    count_pai_ng_age1_abort1 = count_pai_ng_age1_abort1 + 1

                elif sublist_pai_hetero[index_age1_abort1][0] == '1.0':
                    count_pai_hetero_age1_abort1 = count_pai_hetero_age1_abort1 + 1

                elif sublist_pai_homo[index_age1_abort1][0] == '1.0':
                    count_pai_homo_age1_abort1 = count_pai_homo_age1_abort1 + 1

                elif sublist_mthfr_ng[index_age1_abort1][0] == '1.0':
                    count_mthfr_ng_age1_abort1 = count_mthfr_ng_age1_abort1 + 1

                elif sublist_mthfr_hetero[index_age1_abort1][0] == '1.0':
                    count_mthfr_hetero_age1_abort1 = count_mthfr_hetero_age1_abort1 + 1

                elif sublist_mthfr_homo[index_age1_abort1][0] == '1.0':
                    count_mthfr_homo_age1_abort1 = count_mthfr_homo_age1_abort1 + 1

                print(sublist_fvl_ng[index_age1_abort1], 'Bravo 1')

            print(count_fvl_ng_age1_abort1)
            # context3['count_fvl_ng_age1_abort1'] = count_fvl_ng_age1_abort1
            # # mutations_age1_abort1_fvl_ng = count_fvl_ng_age1_abort1 / num_patients_abort1 * 100
            # context3['mutations_age1_abort1_fvl_ng'] = mutations_age1_abort1_fvl_ng
            # context3['count_fvl_hetero_age1_abort1'] = count_fvl_hetero_age1_abort1
            # # mutations_age1_abort1_fvl_hetero = count_fvl_hetero_age1_abort1 / num_patients_abort1 * 100
            # context3['mutations_age1_abort1_fvl_hetero'] = mutations_age1_abort1_fvl_hetero
            #
            # context3['count_prothr_ng_age1_abort1'] = count_prothr_ng_age1_abort1
            # # mutations_age1_abort1_prothr_ng = count_prothr_ng_age1_abort1 / num_patients_abort1 * 100
            # context3['mutations_age1_abort1_prothr_ng'] = mutations_age1_abort1_prothr_ng

            # context3['count_prothr_hetero_age1_abort1'] = count_prothr_hetero_age1_abort1
            # mutations_age1_abort1_prothr_hetero = count_prothr_hetero_age1_abort1 / num_patients_abort1 * 100
            # context3['mutations_age1_abort1_prothr_hetero'] = mutations_age1_abort1_prothr_hetero
            #
            # context3['count_prothr_homo_age1_abort1'] = count_prothr_homo_age1_abort1
            # mutations_age1_abort1_prothr_homo = count_prothr_homo_age1_abort1 / num_patients_abort1 * 100
            # context3['mutations_age1_abort1_prothr_homo'] = mutations_age1_abort1_prothr_homo
            #
            # context3['count_pai_ng_age1_abort1'] = count_pai_ng_age1_abort1
            # mutations_age1_abort1_pai_ng = count_pai_ng_age1_abort1 / num_patients_abort1 * 100
            # context3['mutations_age1_abort1_pai_ng'] = mutations_age1_abort1_pai_ng
            #
            # context3['count_pai_hetero_age1_abort1'] = count_pai_hetero_age1_abort1
            # mutations_age1_abort1_pai_hetero = count_pai_hetero_age1_abort1 / num_patients_abort1 * 100
            # context3['mutations_age1_abort1_pai_hetero'] = mutations_age1_abort1_pai_hetero
            #
            # context3['count_pai_homo_age1_abort1'] = count_pai_homo_age1_abort1
            # mutations_age1_abort1_pai_homo = count_pai_homo_age1_abort1 / num_patients_abort1 * 100
            # context3['mutations_age1_abort1_pai_homo'] = mutations_age1_abort1_pai_homo
            #
            # context3['count_mthfr_ng_age1_abort1'] = count_mthfr_ng_age1_abort1
            # mutations_age1_abort1_mthfr_ng = count_mthfr_ng_age1_abort1 / num_patients_abort1 * 100
            # context3['mutations_age1_abort1_mthfr_ng'] = mutations_age1_abort1_mthfr_ng
            #
            # context3['count_mthfr_hetero_age1_abort1'] = count_mthfr_hetero_age1_abort1
            # mutations_age1_abort1_mthfr_hetero = count_mthfr_hetero_age1_abort1 / num_patients_abort1 * 100
            # context3['mutations_age1_abort1_mthfr_hetero'] = mutations_age1_abort1_mthfr_hetero
            #
            # context3['count_mthfr_homo_age1_abort1'] = count_mthfr_homo_age1_abort1
            # mutations_age1_abort1_mthfr_homo = count_mthfr_homo_age1_abort1 / num_patients_abort1 * 100
            # context3['mutations_age1_abort1_mthfr_homo'] = mutations_age1_abort1_mthfr_homo



            # for index_array_age2 in context3['num_array_data_age2']:
            #     if sublist_abort[index_array_age2][0] == '1.0':
            #         num_array_abort1.append(index_array_age2)
            #         print(num_array_abort1, 'Bravo 1')
            #     elif sublist_abort[index_array_age2][0] == '2.0':
            #         num_array_abort2.append(index_array_age2)
            #         print(num_array_abort2, 'Bravo 2')
            #     elif sublist_abort[index_array_age2][0] > '2.0':
            #         num_array_abort3.append(index_array_age2)
            #         print(num_array_abort3, 'Bravo 3')
            #
            # for index_array_age3 in context3['num_array_data_age3']:
            #     if sublist_abort[index_array_age3][0] == '1.0':
            #         num_array_abort1.append(index_array_age3)
            #         print(num_array_abort1, 'Bravo 1')
            #     elif sublist_abort[index_array_age3][0] == '2.0':
            #         num_array_abort2.append(index_array_age3)
            #         print(num_array_abort2, 'Bravo 2')
            #     elif sublist_abort[index_array_age3][0] > '2.0':
            #         num_array_abort3.append(index_array_age3)
            #         print(num_array_abort3, 'Bravo 3')

            context3['count_age1'] = count_age1
            print(sublist_age)
            sublist_fvl_ng = list_fvl_ng[sublist]
            sublist_age = list_age[sublist]
            context3['sublist_age'] = sublist_age
            print(sublist_age)
            sublist_fvl_hetero = list_fvl_hetero[sublist]
            sublist_fvl_homo = list_fvl_homo[sublist]

            sublist_prothr_ng = list_prothr_ng[sublist]
            sublist_prothr_hetero = list_prothr_hetero[sublist]
            sublist_prothr_homo = list_prothr_homo[sublist]

            sublist_pai_ng = list_pai_ng[sublist]
            sublist_pai_hetero = list_pai_hetero[sublist]
            sublist_pai_homo = list_pai_homo[sublist]

            sublist_mthfr_ng = list_mthfr_ng[sublist]
            sublist_mthfr_hetero = list_mthfr_hetero[sublist]
            sublist_mthfr_homo = list_mthfr_homo[sublist]

####################################################
####################### FVL_NG #####################
####################################################
            # count_fvl_ng = 0
            # count_all_fvl_ng_data = 0
            #
            # for fvl_ng_data in sublist_fvl_ng:
            #     count_all_fvl_ng_data = count_all_fvl_ng_data + 1
            #     if fvl_ng_data[0] == '1.0':
            #         count_fvl_ng = count_fvl_ng + 1
            # # print(count_fvl_ng)
            # count_fvl_ng_0 = count_all_fvl_ng_data - count_fvl_ng
            # fvl_1_ng_percent = count_fvl_ng * 100 / count_all_fvl_ng_data

            f_fvl_ng = factor(sublist_fvl_ng)

            context3['count_fvl_ng'] = f_fvl_ng[0]
            context3['count_fvl_ng_0'] = f_fvl_ng[1]
            context3['fvl_1_ng_percent'] = f_fvl_ng[2]
            context3['count_all_fvl_ng_data'] = f_fvl_ng[3]

            # print(sublist_fvl_ng)
####################################################
####################################################

####################################################
####################### FVL_NG_HETERO ##############
####################################################

            # count_fvl_hetero = 0
            # count_all_fvl_hetero_data = 0
            #
            # for fvl_hetero_data in sublist_fvl_hetero:
            #     count_all_fvl_hetero_data = count_all_fvl_hetero_data + 1
            #     if fvl_hetero_data[0] == '1.0':
            #         count_fvl_hetero = count_fvl_hetero + 1
            # print(count_fvl_hetero)
            # count_fvl_hetero_0 = count_all_fvl_hetero_data - count_fvl_hetero
            # fvl_1_hetero_percent = count_fvl_hetero * 100 / count_all_fvl_hetero_data

            f_fvl_hetero = factor(sublist_fvl_hetero)

            context3['count_fvl_hetero'] = f_fvl_hetero[0]
            context3['count_fvl_hetero_0'] = f_fvl_hetero[1]
            context3['fvl_1_hetero_percent'] = f_fvl_hetero[2]
            context3['count_all_fvl_hetero_data'] = f_fvl_hetero[3]

####################################################
####################################################

####################################################
####################### FVL_HOMO ################
####################################################
            # count_fvl_homo = 0
            # count_all_fvl_homo_data = 0
            #
            # for fvl_homo_data in sublist_fvl_homo:
            #     count_all_fvl_homo_data = count_all_fvl_homo_data + 1
            #     if fvl_homo_data[0] == '1.0':
            #         count_fvl_homo = count_fvl_homo + 1
            # print(count_fvl_homo)
            # count_fvl_homo_0 = count_all_fvl_homo_data - count_fvl_homo
            # fvl_1_homo_percent = count_fvl_homo * 100 / count_all_fvl_homo_data

            f_fvl_homo = factor(sublist_fvl_homo)

            context3['count_fvl_homo'] = f_fvl_homo[0]
            context3['count_fvl_homo_0'] = f_fvl_homo[1]
            context3['fvl_1_homo_percent'] = f_fvl_homo[2]
            context3['count_all_fvl_homo_data'] = f_fvl_homo[3]

####################################################
####################################################

####################################################
####################### PROTHR_NG ##################
####################################################

            # count_prothr_ng = 0
            # count_all_prothr_ng_data = 0
            #
            # for prothr_ng_data in sublist_prothr_ng:
            #     count_all_prothr_ng_data = count_all_prothr_ng_data + 1
            #     if prothr_ng_data[0] == '1.0':
            #         count_prothr_ng = count_prothr_ng + 1
            # count_prothr_ng_0 = count_all_prothr_ng_data - count_prothr_ng
            # prothr_1_ng_percent = count_prothr_ng * 100 / count_all_prothr_ng_data

            f_prothr_ng = factor(sublist_prothr_ng)

            context3['count_prothr_ng'] = f_prothr_ng[0]
            context3['count_prothr_ng_0'] = f_prothr_ng[1]
            context3['prothr_1_ng_percent'] = f_prothr_ng[2]
            context3['count_all_prothr_ng_data'] = f_prothr_ng[3]

####################################################
####################################################

####################################################
####################### PROTHR_HETERO ##############
####################################################

            # count_prothr_hetero = 0
            # count_all_prothr_hetero_data = 0
            #
            # for prothr_hetero_data in sublist_prothr_hetero:
            #     count_all_prothr_hetero_data = count_all_prothr_hetero_data + 1
            #     if prothr_hetero_data[0] == '1.0':
            #         count_prothr_hetero = count_prothr_hetero + 1
            # count_prothr_hetero_0 = count_all_prothr_hetero_data - count_prothr_hetero
            # prothr_1_hetero_percent = count_prothr_hetero * 100 / count_all_prothr_hetero_data

            f_prothr_hetero = factor(sublist_prothr_hetero)

            context3['count_prothr_hetero'] = f_prothr_hetero[0]
            context3['count_prothr_hetero_0'] = f_prothr_hetero[1]
            context3['prothr_1_hetero_percent'] = f_prothr_hetero[2]
            context3['count_all_prothr_hetero_data'] = f_prothr_hetero[3]

####################################################
####################################################

####################################################
####################### PROTHR_HOMO ################
####################################################

            # count_prothr_homo = 0
            # count_all_prothr_homo_data = 0
            #
            # for prothr_homo_data in sublist_prothr_homo:
            #     count_all_prothr_homo_data = count_all_prothr_homo_data + 1
            #     if prothr_homo_data[0] == '1.0':
            #         count_prothr_homo = count_prothr_homo + 1
            # count_prothr_homo_0 = count_all_prothr_homo_data - count_prothr_homo
            # prothr_1_homo_percent = count_prothr_homo * 100 / count_all_prothr_homo_data

            f_prothr_homo = factor(sublist_prothr_homo)

            context3['count_prothr_homo'] = f_prothr_homo[0]
            context3['count_prothr_homo_0'] = f_prothr_homo[1]
            context3['prothr_1_homo_percent'] = f_prothr_homo[2]
            context3['count_all_prothr_homo_data'] = f_prothr_homo[3]

####################################################
####################################################

####################################################
####################### PAI_NG #####################
####################################################
            # count_pai_ng = 0
            # count_all_pai_ng_data = 0
            #
            # for pai_ng_data in sublist_pai_ng:
            #     count_all_pai_ng_data = count_all_pai_ng_data + 1
            #     if pai_ng_data[0] == '1.0':
            #         count_pai_ng = count_pai_ng + 1
            # count_pai_ng_0 = count_all_pai_ng_data - count_pai_ng
            # pai_1_ng_percent = count_pai_ng * 100 / count_all_pai_ng_data

            f_pai_ng = factor(sublist_pai_ng)

            context3['count_pai_ng'] = f_pai_ng[0]
            context3['count_pai_ng_0'] = f_pai_ng[1]
            context3['pai_1_ng_percent'] = f_pai_ng[2]
            context3['count_all_pai_ng_data'] = f_pai_ng[3]

####################################################
####################################################

####################################################
####################### PAI_HETERO #################
####################################################
            # count_pai_hetero = 0
            # count_all_pai_hetero_data = 0
            #
            # for pai_hetero_data in sublist_pai_hetero:
            #     count_all_pai_hetero_data = count_all_pai_hetero_data + 1
            #     if pai_hetero_data[0] == '1.0':
            #         count_pai_hetero = count_pai_hetero + 1
            # count_pai_hetero_0 = count_all_pai_hetero_data - count_pai_hetero
            # pai_1_hetero_percent = count_pai_hetero * 100 / count_all_pai_hetero_data

            f_pai_hetero = factor(sublist_pai_hetero)

            context3['count_pai_hetero'] = f_pai_hetero[0]
            context3['count_pai_hetero_0'] = f_pai_hetero[1]
            context3['pai_1_hetero_percent'] = f_pai_hetero[2]
            context3['count_all_pai_hetero_data'] = f_pai_hetero[3]

####################################################
####################################################

####################################################
####################### PAI_HOMO ###################
####################################################
            # count_pai_homo = 0
            # count_all_pai_homo_data = 0
            #
            # for pai_homo_data in sublist_pai_homo:
            #     count_all_pai_homo_data = count_all_pai_homo_data + 1
            #     if pai_homo_data[0] == '1.0':
            #         count_pai_homo = count_pai_homo + 1
            # count_pai_homo_0 = count_all_pai_homo_data - count_pai_homo
            # pai_1_homo_percent = count_pai_homo * 100 / count_all_pai_homo_data

            f_pai_homo = factor(sublist_pai_homo)

            # context3['count_pai_homo'] = count_pai_homo
            # context3['count_pai_homo_0'] = count_pai_homo_0
            # context3['pai_1_homo_percent'] = pai_1_homo_percent
            # context3['count_all_pai_homo_data'] = count_all_pai_homo_data

            context3['count_pai_homo'] = f_pai_homo[0]
            context3['count_pai_homo_0'] = f_pai_homo[1]
            context3['pai_1_homo_percent'] = f_pai_homo[2]
            context3['count_all_pai_homo_data'] = f_pai_homo[3]

####################################################
####################################################

####################################################
####################### MTHFR_NG ###################
####################################################
            # count_mthfr_ng = 0
            # count_all_mthfr_ng_data = 0
            #
            # for mthfr_ng_data in sublist_mthfr_ng:
            #     count_all_mthfr_ng_data = count_all_mthfr_ng_data + 1
            #     if mthfr_ng_data[0] == '1.0':
            #         count_mthfr_ng = count_mthfr_ng + 1
            # count_mthfr_ng_0 = count_all_mthfr_ng_data - count_mthfr_ng
            # mthfr_1_ng_percent = count_mthfr_ng * 100 / count_all_mthfr_ng_data

            f_mthfr_ng = factor(sublist_mthfr_ng)


            # context3['count_mthfr_ng'] = count_mthfr_ng
            # context3['count_mthfr_ng_0'] = count_mthfr_ng_0
            # context3['mthfr_1_ng_percent'] = mthfr_1_ng_percent
            # context3['count_all_mthfr_ng_data'] = count_all_mthfr_ng_data

            context3['count_mthfr_ng'] = f_mthfr_ng[0]
            context3['count_mthfr_ng_0'] = f_mthfr_ng[1]
            context3['mthfr_1_ng_percent'] = f_mthfr_ng[2]
            context3['count_all_mthfr_ng_data'] = f_mthfr_ng[3]


####################################################
####################################################

####################################################
####################### MTHFR_HETERO ###############
####################################################
            # count_mthfr_hetero = 0
            # count_all_mthfr_hetero_data = 0
            #
            # for mthfr_hetero_data in sublist_mthfr_hetero:
            #     count_all_mthfr_hetero_data = count_all_mthfr_hetero_data + 1
            #     if mthfr_hetero_data[0] == '1.0':
            #         count_mthfr_hetero = count_mthfr_hetero + 1
            # count_mthfr_hetero_0 = count_all_mthfr_hetero_data - count_mthfr_hetero
            # mthfr_1_hetero_percent = count_mthfr_hetero * 100 / count_all_mthfr_hetero_data

            f_mthfr_hetero = factor(sublist_mthfr_hetero)


            # context3['count_mthfr_hetero'] = count_mthfr_hetero
            # context3['count_mthfr_hetero_0'] = count_mthfr_hetero_0
            # context3['mthfr_1_hetero_percent'] = mthfr_1_hetero_percent
            # context3['count_all_mthfr_hetero_data'] = count_all_mthfr_hetero_data

            context3['count_mthfr_hetero'] = f_mthfr_hetero[0]
            context3['count_mthfr_hetero_0'] = f_mthfr_hetero[1]
            context3['mthfr_1_hetero_percent'] = f_mthfr_hetero[2]
            context3['count_all_mthfr_hetero_data'] = f_mthfr_hetero[3]

####################################################
####################################################

####################################################
####################### MTHFR_HOMO #################
####################################################
            # count_mthfr_homo = 0
            # count_all_mthfr_homo_data = 0
            #
            # for mthfr_homo_data in sublist_mthfr_homo:
            #     count_all_mthfr_homo_data = count_all_mthfr_homo_data + 1
            #     if mthfr_homo_data[0] == '1.0':
            #         count_mthfr_homo = count_mthfr_homo + 1
            # count_mthfr_homo_0 = count_all_mthfr_homo_data - count_mthfr_homo
            # mthfr_1_homo_percent = count_mthfr_homo * 100 / count_all_mthfr_homo_data
            f_mthfr_homo = factor(sublist_mthfr_homo)

            # context3['count_mthfr_homo'] = count_mthfr_homo
            # context3['count_mthfr_homo_0'] = count_mthfr_homo_0
            # context3['mthfr_1_homo_percent'] = mthfr_1_homo_percent
            # context3['count_all_mthfr_homo_data'] = count_all_mthfr_homo_data

            context3['count_mthfr_homo'] = f_mthfr_homo[0]
            context3['count_mthfr_homo_0'] = f_mthfr_homo[1]
            context3['mthfr_1_homo_percent'] = f_mthfr_homo[2]
            context3['count_all_mthfr_homo_data'] = f_mthfr_homo[3]
####################################################
####################################################


    if request.method == "POST":
        if 'save' in request.POST:
            pk = request.POST.get('save')
            if not pk:
                prida_mutations_form = PridaMutationsForm(request.POST)
            else:
                p_mutations = PridaMutations.objects.get(id=pk)
                prida_mutations_form = PridaMutationsForm(request.POST, instance=p_mutations)

            prida_mutations_form.save()
            prida_mutations_form = PridaMutationsForm()

        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            p_mutations = PridaMutations.objects.get(id=pk)
            p_mutations.delete()
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            p_mutations = PridaMutations.objects.get(id=pk)
            prida_mutations_form = PridaMutationsForm(instance=p_mutations)
            print('Hello')
    print(prida_list_data, len(prida_list_data))
    for select_factor in prida_list_data:
        if select_factor == 'fvl_ng':
            context3['factor_fvl_ng'] = select_factor
        elif select_factor == 'fvl_hetero':
            context3['factor_fvl_hetero'] = select_factor
        print(select_factor)


    if prida_list_data:
        print(prida_list_data[0])

        context3['prida_list_data'] = prida_list_data
        print(context3['prida_list_data'])

    # context3['prida_list_data'] = prida_list_data
    context3['prida_mutations'] = prida_mutations
    context3['prida_mutations_form'] = prida_mutations_form
    context3['st_line'] = start_line

    return render(request, 'proba1.html', context3)


#######################################################№№№№№№№№№№№№№№№№
#### Проверява зададената възрастова граница в списък от възрасти  ####
#### Създава редица от избраната възрастова граница                ####
#### Брои пациентите в избраната възрастова граница                ####
#### Брои всички пациенти                                          ####
#######################################################################
def create_age_array(sublist_age):

    count_age1 = 0
    count_age2 = 0
    count_age3 = 0
    index_array_age1 = []
    index_array_age2 = []
    index_array_age3 = []

    count_index_array_age = 0

    for age in sublist_age:
        if 20 <= age[0] <= 30:
            count_age1 = count_age1 + 1
            index_array_age1.append(count_index_array_age)
        elif 31 <= age[0] <= 40:
            count_age2 = count_age2 + 1
            index_array_age2.append(count_index_array_age)
        elif 41 <= age[0] <= 50:
            count_age3 = count_age3 + 1
            index_array_age3.append(count_index_array_age)
        count_index_array_age = count_index_array_age + 1

    print(index_array_age1, 'OK Age1')
    print(index_array_age2, 'OK Age2')
    print(index_array_age3, 'OK Age3')

    return index_array_age1, index_array_age2, index_array_age3


##################################################################
## За възраст в избрана възрастова граница                      ##
## Създава променливи за:                                       ##
##  - Възрастова граница                                        ##
##  - Rедица от индекси за възрастова граница,                  ##
## Достъпни в html                                              ##
##################################################################

def create_array_age_and_age_interval_access_html(p_age_l, in_array_a1, in_array_a2, in_array_a3):
    create_context = {}
    for age in p_age_l:
        if age == 'age1':
            create_context['index_array_age'] = in_array_a1
            create_context['age_interval'] = age
        elif age == 'age2':
            create_context['index_array_age'] = in_array_a2
            create_context['age_interval'] = age
        elif age == 'age3':
            create_context['index_array_age'] = in_array_a3
            create_context['age_interval'] = age

    return create_context


################################################################
## Създаване на поредица от пациенти с 1, 2 или повече аборти ##
################################################################
def create_abort_index_array(in_array_a_d, subl_abort):
    count_abort1 = 0
    count_abort2 = 0
    count_abort3 = 0

    index_array_abort1 = []
    index_array_abort2 = []
    index_array_abort3 = []

    count_index_array_abort = 0
    for abort in in_array_a_d:
        if subl_abort[abort][0] == '1.0':
            count_abort1 = count_abort1 + 1
            index_array_abort1.append(abort)
        elif subl_abort[abort][0] == '2.0':
            count_abort2 = count_abort2 + 1
            index_array_abort2.append(abort)
        elif subl_abort[abort][0] != '?' or subl_abort[abort][0] != '2.0' or subl_abort[abort][
            0] != '1.0':
            count_abort3 = count_abort3 + 1
            index_array_abort3.append(abort)

        count_index_array_abort = count_index_array_abort + 1

    print(index_array_abort1, 'OK 1')
    print(index_array_abort2, 'OK 1')
    print(index_array_abort3, 'OK 1')

    return index_array_abort1, index_array_abort2, index_array_abort3


#########################################################################
## Създаване на групи от пациенти с 1, 2 и повече аборти и поредица от ##
#########################################################################
def create_dict_index_array_aborts_and_abort_variant_html(p_abort_l, in_array_ab1, in_array_ab2, in_array_ab3):
    create_context = {}
    for abort in p_abort_l:
        if abort == 'abort_1':
            create_context['index_array_abort'] = in_array_ab1
            create_context['abort_variant'] = abort
        elif abort == 'abort_2':
            create_context['index_array_abort'] = in_array_ab2
            create_context['abort_variant'] = abort
        elif abort == 'abort_3':
            create_context['index_array_abort'] = in_array_ab3
            create_context['abort_variant'] = abort

    create_context['number_abort_patients'] = len(create_context['index_array_abort'])

    print(create_context['index_array_abort'], 'OK', create_context['number_abort_patients'])

    return create_context


def func1(
        in_array_d,
        in_array_a_d,
        subl_fvl_ng,
        subl_fvl_hetero,
        subl_fvl_homo,
        subl_prothr_ng,
        subl_prothr_hetero,
        subl_prothr_homo,
        subl_pai_ng,
        subl_pai_hetero,
        subl_pai_homo,
        subl_mthfr_ng,
        subl_mthfr_hetero,
        subl_mthfr_homo,
        subl_abort,
        cli_list):
    count_fvl_ng_mutations = 0
    count_fvl_hetero_mutations = 0

    count_mutations = 0
    count_mutations_abort1 = 0
    count_mutations_abort2 = 0
    count_mutations_abort3 = 0

    count_mutations_abort1 = 0
    count__mutations_abort2 = 0
    count_mutations_abort3 = 0

    count_fvl_ng_mutations_abort1 = 0
    count_fvl_ng_mutations_abort2 = 0
    count_fvl_ng_mutations_abort3 = 0

    count_fvl_hetero_mutations_abort1 = 0
    count_fvl_hetero_mutations_abort2 = 0
    count_fvl_hetero_mutations_abort3 = 0

    res_count_fvl_ng_mutations_abort1 = 0
    res_count_fvl_ng_mutations_abort2 = 0
    res_count_fvl_ng_mutations_abort3 = 0
    percent_mutations_abort1 = 0
    percent_mutations_abort2 = 0
    percent_mutations_abort3 = 0

    res_count_mutations_abort1 = 0
    res_count_mutations_abort2 = 0
    res_count_mutations_abort3 = 0

    create_context = {}
    factor_type = in_array_d[0]
    # for factor_type in in_array_d:
    sublist_factor = []
    if factor_type == 'fvl_ng':
        sublist_factor = subl_fvl_ng
    elif factor_type == 'fvl_hetero':
        sublist_factor = subl_fvl_hetero
    elif factor_type == 'fvl_homo':
        sublist_factor = subl_fvl_homo
    elif factor_type == 'prothr_ng':
        sublist_factor = subl_prothr_ng
    elif factor_type == 'prothr_hetero':
        sublist_factor = subl_prothr_hetero
    elif factor_type == 'prothr_homo':
        sublist_factor = subl_prothr_homo
    elif factor_type == 'pai_ng':
        sublist_factor = subl_pai_ng
    elif factor_type == 'pai_hetero':
        sublist_factor = subl_pai_hetero
    elif factor_type == 'pai_homo':
        sublist_factor = subl_pai_homo
    elif factor_type == 'mthfr_ng':
        sublist_factor = subl_mthfr_ng
    elif factor_type == 'mthfr_hetero':
        sublist_factor = subl_mthfr_hetero
    elif factor_type == 'mthfr_homo':
        sublist_factor = subl_mthfr_homo
    for factor_index in in_array_a_d:
        print(sublist_factor[factor_index][0], 'Sublist FVL NG')
        if sublist_factor[factor_index][0] == '1.0':
            count_mutations = count_mutations + 1
            print('OKK')
            if subl_abort[factor_index][0] == '1.0':
                count_mutations_abort1 = count_mutations_abort1 + 1
                print(count_mutations_abort1)
            elif subl_abort[factor_index][0] == '2.0':
                count_mutations_abort2 = count_mutations_abort2 + 1
                print(count_mutations_abort2)
            else:
                count_mutations_abort3 = count_mutations_abort3 + 1
                print(count_mutations_abort3)
    # elif factor_type == 'fvl_hetero':
    #     for factor_index in in_array_a_d:
    #         print(subl_fvl_hetero[factor_index][0], 'Sublist FVL HETERO')
    #         if subl_fvl_hetero[factor_index][0] == '1.0':
    #             count_fvl_hetero_mutations = count_fvl_hetero_mutations + 1
    #             print('OKK')
    #             if subl_abort[factor_index][0] == '1.0':
    #                 count_fvl_hetero_mutations_abort1 = count_fvl_hetero_mutations_abort1 + 1
    #                 print(count_fvl_hetero_mutations_abort1)
    #             elif subl_abort[factor_index][0] == '2.0':
    #                 count_fvl_hetero_mutations_abort2 = count_fvl_hetero_mutations_abort2 + 1
    #                 print(count_fvl_hetero_mutations_abort2)
    #             else:
    #                 count_fvl_hetero_mutations_abort3 = count_fvl_hetero_mutations_abort3 + 1
    #                 print(count_fvl_hetero_mutations_abort3)
    #
    #     print('FVL_Hetero')
    #     pass
    # elif factor_type == 'fvl_homo':
    #     pass
    # elif factor_type == 'prothr_ng':
    #     pass
    # elif factor_type == 'prothr_hetero':
    #     pass
    # elif factor_type == 'prothr_homo':
    #     pass
    # elif factor_type == 'pai_ng':
    #     pass
    # elif factor_type == 'pai_hetero':
    #     pass
    # elif factor_type == 'pai_homo':
    #     pass
    # elif factor_type == 'mthfr_ng':
    #     pass
    # elif factor_type == 'mthfr_hetero':
    #     pass
    # elif factor_type == 'mthfr_homo':
    #     pass
    #
    # create_context['factor_type'] = factor_type
        # for factor_index in in_array_a_d:
        #     # print(sublist_fvl_ng[factor_index][0])
        #     break

    res_count_mutations_abort1 = count_mutations_abort1
    print('Start')
    print(res_count_mutations_abort1)
    # create_context['count_mutations_abort1'] = count_fvl_ng_mutations_abort1
    percent_mutations_abort1 = round(res_count_mutations_abort1 * 100 / cli_list, 2)
    # create_context['percent_mutations_abort1'] = round(count_fvl_ng_mutations_abort1 * 100 /
    #                                                    create_context['clients_list'], 2)
    print(percent_mutations_abort1)
    res_count_mutations_abort2 = count_mutations_abort2
    print(res_count_mutations_abort2)
    # create_context['count_mutations_abort2'] = count_fvl_ng_mutations_abort2
    percent_mutations_abort2 = round(res_count_mutations_abort2 * 100 / cli_list, 2)
    print(percent_mutations_abort2)
    # create_context['percent_mutations_abort2'] = round(count_fvl_ng_mutations_abort2 * 100 /
    #                                                    create_context['clients_list'], 2)
    res_count_mutations_abort3 = count_mutations_abort3
    print(res_count_mutations_abort3)
    # create_context['count_mutations_abort3'] = count_fvl_ng_mutations_abort3
    percent_mutations_abort3 = round(res_count_mutations_abort3 * 100 / cli_list, 2)
    print(percent_mutations_abort3)
    # create_context['percent_mutations_abort3'] = round(count_fvl_ng_mutations_abort3 * 100 / cli_list, 2)
    print('Stop')
    return res_count_mutations_abort1, percent_mutations_abort1, \
        res_count_mutations_abort2, percent_mutations_abort2, \
        res_count_mutations_abort3, percent_mutations_abort3


######################################################################################
######################################################################################
# for factor_type in prida_list_data:
#     if factor_type == 'fvl_ng':
#         context3['factor_type'] = 'fvl_ng'
#         for factor_index in context3['index_array_age']:
#             print(sublist_fvl_ng[factor_index][0])
#             if sublist_fvl_ng[factor_index][0] == '1.0':
#                 count_fvl_ng_mutations = count_fvl_ng_mutations + 1
#                 if sublist_abort[factor_index][0] == '1.0':
#                     count_fvl_ng_mutations_abort1 = count_fvl_ng_mutations_abort1 + 1
#                 elif sublist_abort[factor_index][0] == '2.0':
#                     count_fvl_ng_mutations_abort2 = count_fvl_ng_mutations_abort2 + 1
#                 else:
#                     count_fvl_ng_mutations_abort3 = count_fvl_ng_mutations_abort3 + 1
#         context3['count_mutations_abort1'] = count_fvl_ng_mutations_abort1
#         context3['percent_mutations_abort1'] = round(count_fvl_ng_mutations_abort1 * 100 /
#                                                      context3['clients_list'], 2)
#         context3['count_mutations_abort2'] = count_fvl_ng_mutations_abort2
#         context3['percent_mutations_abort2'] = round(count_fvl_ng_mutations_abort2 * 100 /
#                                                      context3['clients_list'], 2)
#         context3['count_mutations_abort3'] = count_fvl_ng_mutations_abort3
#         context3['percent_mutations_abort3'] = round(count_fvl_ng_mutations_abort3 * 100 /
#                                                      context3['clients_list'], 2)
#     elif factor_type == 'fvl_hetero':
#         context3['factor_type'] = 'fvl_hetero'
#         for factor_index in context3['index_array_age']:
#             print(sublist_fvl_hetero[factor_index][0])
#             if sublist_fvl_hetero[factor_index][0] == '1.0':
#                 count_fvl_hetero_mutations = count_fvl_hetero_mutations + 1
#                 if sublist_abort[factor_index][0] == '1.0':
#                     count_fvl_hetero_mutations_abort1 = count_fvl_hetero_mutations_abort1 + 1
#                 elif sublist_abort[factor_index][0] == '2.0':
#                     count_fvl_hetero_mutations_abort2 = count_fvl_hetero_mutations_abort2 + 1
#                 else:
#                     count_fvl_hetero_mutations_abort3 = count_fvl_hetero_mutations_abort3 + 1
#         context3['count_mutations_abort1'] = count_fvl_hetero_mutations_abort1
#         context3['percent_mutations_abort1'] = round(count_fvl_hetero_mutations_abort1 * 100 /
#                                                      context3['clients_list'], 2)
#         context3['count_mutations_abort2'] = count_fvl_hetero_mutations_abort2
#         context3['percent_mutations_abort2'] = round(count_fvl_hetero_mutations_abort2 * 100 /
#                                                      context3['clients_list'], 2)
#         context3['count_mutations_abort3'] = count_fvl_hetero_mutations_abort3
#         context3['percent_mutations_abort3'] = round(count_fvl_hetero_mutations_abort3 * 100 /
#                                                      context3['clients_list'], 2)

        ###############################################################################
        ###############################################################################



def factor(sublist_factor):
    # count_mthfr_homo = 0
    # count_all_mthfr_homo_data = 0
    count_factor_ones = 0
    count_all_factor_data = 0

    # for mthfr_homo_data in sublist_factor:
    #     count_all_mthfr_homo_data = count_all_mthfr_homo_data + 1
    #     if mthfr_homo_data[0] == '1.0':
    #         count_mthfr_homo = count_mthfr_homo + 1
    # count_mthfr_homo_0 = count_all_mthfr_homo_data - count_mthfr_homo
    # mthfr_1_homo_percent = count_mthfr_homo * 100 / count_all_mthfr_homo_data

    for factor_data in sublist_factor:
        print(sublist_factor, 'Sublist')
        count_all_factor_data = count_all_factor_data + 1
        if factor_data[0] == '1.0':
            count_factor_ones = count_factor_ones + 1
    count_factor_zero = count_all_factor_data - count_factor_ones
    factor_ones_percent = count_factor_ones * 100 / count_all_factor_data
    # print(type(count_factor_ones))

    return count_factor_ones, count_factor_zero, factor_ones_percent, count_all_factor_data


def simple_upload(request):
    context4 = {}
    scores = Person.objects.all()
    context4['scores'] = scores
    # pass
    if request.method == "POST":
        person_resource = PersonResource()
        dataset = Dataset()
        # new_person = request.FILES['myfile']

        # if not new_person.name.endswith('xls'):
        #     messages.info(request, 'wrong format')
        #     return render(request, 'proba1.html')
        #
        # imported_data = dataset.load(new_person.read(),format='xls')
        # for data in imported_data:
        #     value = Person(
        #         data[0],
        #         data[1],
        #         data[2],
        #         data[3]
        #     )
        #     value.save()

    return render(request, 'proba1.html')


def generate_objects(request):
    for i in range(5):
        p = PatientProba(name=f"Post{i}")
        p.save()
    # with open('/Users/tihomir/PycharmProjects/projectproba/pridastartpr/pridastartapp/proba.csv', 'r') as f:
        # reader = csv.reader(f)
        # content = [line for line in reader if len(line) > 0]
        # print(content)
    # for i in range(len(content)):
        # print(content)
    return redirect('blog')

# Create your views here.


# {% if not prida_mutations_form.instance.id %}
# <tr>
# <td> {{pm.id}} </td>
# {% include 'save.html' %}
# </tr>
# {% endif %}
# {%for pm in prida_mutations %}

# {% if prida_mutations_form.instance.id == pm.id %}
#                         <td>{{ pm.id }}</td>
#                         {% include 'save.html' %}
#
#                         {% else %}

# {%for field in prida_mutations_form %}


# Raboti


# <tr>
#
#
#                         <td></td>
#                         {% for field in prida_mutations_form %}
#                         <td>
#                             {{ field }}
#                         </td>
#                             {% endfor %}
#                         <td>
#                             <button name="save" class="btn btn-primary btn-lg">Save</button></td>
#                     </tr>
#                     {% for pm in prida_mutations %}
#                     <tr>
#                         <td>{{ pm.id }}</td>
#                         <td>{{ pm.code }}</td>
#                         <td>{{ pm.birth_year }}</td>
#                         <td>{{ pm.age }}</td>
#
#                         <td>{{ pm.fvl_ng }}</td>
#                         <td>{{ pm.fvl_hetero }}</td>
#                         <td>{{ pm.fvl_homo }}</td>
#
#                         <td>{{ pm.prothr_ng }}</td>
#                         <td>{{ pm.prothr_hetero }}</td>
#                         <td>{{ pm.prothr_homo }}</td>
#
#                         <td>{{ pm.pai_ng }}</td>
#                         <td>{{ pm.pai_hetero }}</td>
#                         <td>{{ pm.pai_homo }}</td>
#
#                         <td>{{ pm.mthfr_ng }}</td>
#                         <td>{{ pm.mthfr_hetero }}</td>
#                         <td>{{ pm.mthfr_homo }}</td>
#
#                         <td>
#                             <button formnovalidate name="edit" value="{{ pm.id }}" class="btn btn-primary btn-lg">Edit</button>
#                             <button formnovalidate name="delete" value="{{ pm.id }}" class="btn btn-primary btn-lg">Delete</button>
#                         </td>
#                     </tr>
#                     {% endfor %}
