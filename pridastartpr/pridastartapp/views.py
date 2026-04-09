from django.shortcuts import render, redirect
from .models import Patients, PatientProba, Score, Prida, Person, PridaMutations, PridaControli
from .forms import PreeclampsiaForm, RegisterForm, PatientProbaForm, ScoreForm, PridaForm, PridaMutationsForm, \
    PridaControliForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from typing import Tuple
import sqlite3
from tablib import Dataset
from .resources import PersonResource
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

from openpyxl import Workbook


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/proba1')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


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

def conclusions(request):
    return render(request, 'conclusions.html')


def correlation(request):
    # if request.method == 'POST':
    #     form = AuthenticationForm(data=request.POST)
    #     if form.is_valid():
    #         login(request, form.get_user())
    #         return redirect('/')
    # else:
    #     form = AuthenticationForm()
    return render(request, 'correlation.html')


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


def mutations_3_abort(list_factor_1, list_factor_2, list_factor_3):
    list_abort = PridaControli.objects.values_list('abort')
    cnt_factor_1_2_3_abort_1 = 0
    cnt_factor_1_2_3_abort_more = 0

    for in_abort in range(len(list_abort)):
        if ((list_factor_1[in_abort][0] == list_factor_2[in_abort][0] == list_factor_3[in_abort][0])
                == '1.0'):
            if list_abort[in_abort][0] == '1.0':
                cnt_factor_1_2_3_abort_1 = cnt_factor_1_2_3_abort_1 + 1
            else:
                cnt_factor_1_2_3_abort_more = cnt_factor_1_2_3_abort_more + 1

    return cnt_factor_1_2_3_abort_1, cnt_factor_1_2_3_abort_more


def mutations_2_abort(list_abort: Tuple, list_factor_1: Tuple, list_factor_2: Tuple):
    # list_abort = PridaControli.objects.values_list('abort')

    # prida_mutations = PridaMutations.objects.all()
    # list_abort = PridaMutations.objects.values_list('abort')
    # print('LIST FACTOR 1', list_factor_1)
    cnt_factor_1_2_abort_1 = 0
    cnt_factor_1_2_abort_more = 0
    cnt_factor_1_2_abort_0 = 0

    for in_abort in range(len(list_abort)):
        # print('list_factor_2', list_factor_2[in_abort][0][0])
        if (list_factor_1[in_abort][0] == '1.0' and list_factor_2[in_abort][0]) == '1.0':
            if list_abort[in_abort][0] == '1.0':
                cnt_factor_1_2_abort_1 = cnt_factor_1_2_abort_1 + 1
            elif list_abort[in_abort][0] == '0.0':
                cnt_factor_1_2_abort_0 = cnt_factor_1_2_abort_0 + 1
            elif (
                    list_abort[in_abort][0] == '2.0' or
                    list_abort[in_abort][0] == '3.0' or
                    list_abort[in_abort][0] == '4.0' or
                    list_abort[in_abort][0] == '5.0' or
                    list_abort[in_abort][0] == '6.0' or
                    list_abort[in_abort][0] == '7.0' or
                    list_abort[in_abort][0] == '-' or
                    list_abort[in_abort][0] == ''):

                # print("ABORTS", cnt_factor_1_2_abort_more)
                cnt_factor_1_2_abort_more = cnt_factor_1_2_abort_more + 1
    # print('LIST COUNT FACTORS', cnt_factor_1_2_abort_0, cnt_factor_1_2_abort_1, cnt_factor_1_2_abort_more)
    return cnt_factor_1_2_abort_0, cnt_factor_1_2_abort_1, cnt_factor_1_2_abort_more


def calc_patients_more_mut_controli(request):
    context3 = {}
    prida_controli = PridaControli.objects.all()

    list_fvl_ng = PridaControli.objects.values_list('fvl_ng')
    list_fvl_hetero = PridaControli.objects.values_list('fvl_hetero')
    list_fvl_homo = PridaControli.objects.values_list('fvl_homo')

    list_prothr_ng = PridaControli.objects.values_list('prothr_ng')
    list_prothr_hetero = PridaControli.objects.values_list('prothr_hetero')
    list_prothr_homo = PridaControli.objects.values_list('prothr_homo')

    list_pai_ng = PridaControli.objects.values_list('pai_ng')
    list_pai_hetero = PridaControli.objects.values_list('pai_hetero')
    list_pai_homo = PridaControli.objects.values_list('pai_homo')

    list_mthfr_ng = PridaControli.objects.values_list('mthfr_ng')
    list_mthfr_hetero = PridaControli.objects.values_list('mthfr_hetero')
    list_mthfr_homo = PridaControli.objects.values_list('mthfr_homo')

    list_abort = PridaControli.objects.values_list('abort')
    prida_age_list_controli = request.POST.getlist('age')  ## Spisak s izbrana ot usera vazrast
    print('CONTROLI1')
    if request.method == 'POST':
        if 'btn_patients_more_mut_controli' in request.POST:
            print('CONTROLI2')

            ######################################################
            ### Heterozygous Factor V Leiden               #######
            ###  and Prothr Hetero Mutation                #######
            ######################################################

            c_cnt_fvl_hetero_prothr_hetero_mut = 0

            for fvl_hetero in range(len(list_fvl_hetero)):

                if list_fvl_hetero[fvl_hetero][0] == list_prothr_hetero[fvl_hetero][0] == '1.0':
                    c_cnt_fvl_hetero_prothr_hetero_mut = c_cnt_fvl_hetero_prothr_hetero_mut + 1


            context3['c_cnt_fvl_hetero_prothr_hetero_mut'] = c_cnt_fvl_hetero_prothr_hetero_mut
            ######################################################
            ### Heterozygous Factor V Leiden            ##########
            ### and PROTHROMBIN Homo Mutation           ##########
            ######################################################

            c_cnt_fvl_hetero_prothr_homo_mut = 0

            for fvl_hetero in range(len(list_fvl_hetero)):
                if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                    c_cnt_fvl_hetero_prothr_homo_mut = c_cnt_fvl_hetero_prothr_homo_mut + 1

            context3['c_cnt_fvl_hetero_prothr_homo_mut'] = c_cnt_fvl_hetero_prothr_homo_mut

            ######################################################
            ### Start Count Heterozygous Factor V       ##########
            ### Leiden and PAI I Homo Mutation          ##########
            ######################################################

            c_cnt_fvl_hetero_pai_homo_mut = 0

            for fvl_hetero in range(len(list_fvl_hetero)):
                if list_fvl_hetero[fvl_hetero][0] == list_pai_homo[fvl_hetero][0] == '1.0':
                    c_cnt_fvl_hetero_pai_homo_mut = c_cnt_fvl_hetero_pai_homo_mut + 1

            context3['c_cnt_fvl_hetero_pai_homo_mut'] = c_cnt_fvl_hetero_pai_homo_mut


            ######################################################
            ### Start Count Heterozygous Factor V       ##########
            ### Leiden and MTHFR Homo Mutation        ##########
            ######################################################

            c_cnt_fvl_hetero_mthfr_homo_mut = 0

            for fvl_hetero in range(len(list_fvl_hetero)):
                if list_fvl_hetero[fvl_hetero][0] == list_mthfr_homo[fvl_hetero][0] == '1.0':
                    c_cnt_fvl_hetero_mthfr_homo_mut = c_cnt_fvl_hetero_mthfr_homo_mut + 1

            context3['c_cnt_fvl_hetero_mthfr_homo_mut'] = c_cnt_fvl_hetero_mthfr_homo_mut

            # ######################################################
            # ### Start Count Homozygous Factor V         ##########
            # ### Leiden and Prothrombin Hetero Mutation  ##########
            # ######################################################

            c_cnt_fvl_homo_prothr_hetero_mut = 0

            for fvl_homo in range(len(list_fvl_homo)):
                if list_fvl_homo[fvl_homo][0] == list_prothr_hetero[fvl_homo][0] == '1.0':
                    c_cnt_fvl_homo_prothr_hetero_mut = c_cnt_fvl_homo_prothr_hetero_mut + 1

            context3['c_cnt_fvl_homo_prothr_hetero_mut'] = c_cnt_fvl_homo_prothr_hetero_mut

            # ######################################################
            # ### Start Count Homozygous Factor V         ##########
            # ### Leiden and Prothrombin Homo Mutation    ##########
            # ######################################################

            c_cnt_fvl_homo_prothr_homo_mut = 0

            for fvl_homo in range(len(list_fvl_homo)):
                if list_fvl_homo[fvl_homo][0] == list_prothr_homo[fvl_homo][0] == '1.0':
                    c_cnt_fvl_homo_prothr_homo_mut = c_cnt_fvl_homo_prothr_homo_mut + 1

            context3['c_cnt_fvl_homo_prothr_homo_mut'] = c_cnt_fvl_homo_prothr_homo_mut

            # ######################################################
            # ### Start Count Homozygous Factor V         ##########
            # ### Leiden and PAI I Homo Mutation          ##########
            # ######################################################

            c_cnt_fvl_homo_pai_homo_mut = 0

            for fvl_homo in range(len(list_fvl_homo)):
                if list_fvl_homo[fvl_homo][0] == list_pai_homo[fvl_homo][0] == '1.0':
                    c_cnt_fvl_homo_pai_homo_mut = c_cnt_fvl_homo_pai_homo_mut + 1

            context3['c_cnt_fvl_homo_pai_homo_mut'] = c_cnt_fvl_homo_pai_homo_mut

            # ######################################################
            # ### Start Count Homozygous Factor V         ##########
            # ### Leiden and MTHFR Homo Mutation          ##########
            # ######################################################

            c_cnt_fvl_homo_mthfr_homo_mut = 0

            for fvl_homo in range(len(list_fvl_homo)):
                if list_fvl_homo[fvl_homo][0] == list_mthfr_homo[fvl_homo][0] == '1.0':
                    c_cnt_fvl_homo_mthfr_homo_mut = c_cnt_fvl_homo_mthfr_homo_mut + 1

            context3['c_cnt_fvl_homo_mthfr_homo_mut'] = c_cnt_fvl_homo_mthfr_homo_mut

            # ######################################################
            # ### Start Count Heterozygous Prothrombin    ##########
            # ### and PAI I Homo Mutation                 ##########
            # ######################################################

            c_cnt_prothr_hetero_pai_homo_mut = 0

            for prothr_hetero in range(len(list_prothr_hetero)):
                if list_prothr_hetero[prothr_hetero][0] == list_pai_homo[prothr_hetero][0] == '1.0':
                    c_cnt_prothr_hetero_pai_homo_mut = c_cnt_prothr_hetero_pai_homo_mut + 1

            context3['c_cnt_prothr_hetero_pai_homo_mut'] = c_cnt_prothr_hetero_pai_homo_mut

            # ######################################################
            # ### Start Count Heterozygous Prothrombin    ##########
            # ### and MTHFR Homo Mutation                 ##########
            # ######################################################

            c_cnt_prothr_hetero_mthfr_homo_mut = 0

            for prothr_hetero in range(len(list_prothr_hetero)):
                if list_prothr_hetero[prothr_hetero][0] == list_mthfr_homo[prothr_hetero][0] == '1.0':
                    c_cnt_prothr_hetero_mthfr_homo_mut = c_cnt_prothr_hetero_mthfr_homo_mut + 1

            context3['c_cnt_prothr_hetero_mthfr_homo_mut'] = c_cnt_prothr_hetero_mthfr_homo_mut

            # ######################################################
            # ### Start Count Homozygous PAI I            ##########
            # ### and MTHFR Homo Mutation                 ##########
            # ######################################################

            c_cnt_pai_homo_mthfr_homo_mut = 0

            for pai_homo in range(len(list_pai_homo)):
                if list_pai_homo[pai_homo][0] == list_mthfr_homo[pai_homo][0] == '1.0':
                    c_cnt_pai_homo_mthfr_homo_mut = c_cnt_pai_homo_mthfr_homo_mut + 1

            context3['c_cnt_pai_homo_mthfr_homo_mut'] = c_cnt_pai_homo_mthfr_homo_mut








        if 'btn_patients_more_mutations' in request.POST:
            print('UraUraUra')
            print('Aborts List', list_abort)
            print('List FVL', list_abort[3][0])

            print('A 2 M1_0', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_hetero)[0])
            print('A 2 M1_1', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_hetero)[1])
            print('A 2 M1_2', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_hetero)[2])

            # print('1 A 2 M1 ', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_hetero)[0])
            context3['cnt_fvl_hetero_pr_hetero_abort_0_c'] = \
            mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_hetero)[0]

            # print('MORE A 2 M1 ', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_hetero)[1])
            # context3['cnt_fvl_hetero_pr_hetero_abort_1_c'] = mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_hetero)[1]

            ######################################################
            ### Start Count Heterozygous Factor V       ##########
            ### Leiden and Prothr Homo Mutation         ##########
            ######################################################

            # cnt_fvl_hetero_prothr_homo_mutations = 0
            # cnt_fvl_hetero_prothr_homo_mut_abort1 = 0
            # cnt_fvl_hetero_prothr_homo_mut_aborts = 0
            #
            # for fvl_hetero in range(len(list_fvl_homo)):
            #     if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
            #         if list_abort[fvl_hetero][0] == '1.0':
            #             cnt_fvl_hetero_prothr_homo_mut_abort1 = cnt_fvl_hetero_prothr_homo_mut_abort1 + 1
            #         else:
            #             cnt_fvl_hetero_prothr_homo_mut_aborts = cnt_fvl_hetero_prothr_homo_mut_aborts + 1
            #         cnt_fvl_hetero_prothr_homo_mutations = cnt_fvl_hetero_prothr_homo_mutations + 1
            #
            # print('FVL Hetero and PROTHR Homo Mutations are:', cnt_fvl_hetero_prothr_homo_mutations)
            # print('FVL Hetero and PROTHR Homo Mutations for Patients with 1 Abort are:')
            # print(cnt_fvl_hetero_prothr_homo_mut_abort1)

            print('A 2 M2_0', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_homo)[0])
            print('A 2 M2_1', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_homo)[1])
            print('A 2 M2_2', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_homo)[2])

            # print('1 A 2 M2 ', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_homo)[0])
            context3['cnt_fvl_hetero_pr_homo_abort_0_c'] = \
            mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_homo)[0]

            # print('MORE A 2 M2 ', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_homo)[1])
            # context3['cnt_fvl_hetero_pr_homo_abort_1_c'] = mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_homo)[1]

            ######################################################
            ### Start Count Heterozygous Factor V       ##########
            ### Leiden and PAI I Homo Mutation        ##########
            ######################################################

            # cnt_fvl_hetero_pai_homo_mutations = 0
            # cnt_fvl_hetero_pai_homo_mut_abort1 = 0
            # cnt_fvl_hetero_pai_homo_mut_aborts = 0
            #
            # for fvl_hetero in range(len(list_fvl_homo)):
            #     if list_fvl_hetero[fvl_hetero][0] == list_pai_homo[fvl_hetero][0] == '1.0':
            #         if list_abort[fvl_hetero][0] == '1.0':
            #             cnt_fvl_hetero_pai_homo_mut_abort1 = cnt_fvl_hetero_pai_homo_mut_abort1 + 1
            #         else:
            #             cnt_fvl_hetero_pai_homo_mut_aborts = cnt_fvl_hetero_pai_homo_mut_aborts + 1
            #         cnt_fvl_hetero_pai_homo_mutations = cnt_fvl_hetero_pai_homo_mutations + 1
            #
            # print('FVL Hetero and PAI I Homo Mutations are:', cnt_fvl_hetero_pai_homo_mutations)
            # print('FVL Hetero and PAI I Homo Mutations for Patients with 1 Abort are:')
            # print(cnt_fvl_hetero_pai_homo_mut_abort1)

            print('A 2 M3_0', mutations_2_abort(list_abort, list_fvl_hetero, list_pai_homo)[0])
            print('A 2 M3_1', mutations_2_abort(list_abort, list_fvl_hetero, list_pai_homo)[1])
            print('A 2 M3_2', mutations_2_abort(list_abort, list_fvl_hetero, list_pai_homo)[2])

            # print('1 A 2 M3 ', mutations_2_abort(list_abort, list_fvl_hetero, list_pai_homo)[0])
            context3['cnt_fvl_hetero_pai_homo_abort_0_c'] = \
            mutations_2_abort(list_abort, list_fvl_hetero, list_pai_homo)[0]

            # print('MORE A 2 M3 ', mutations_2_abort(list_abort, list_fvl_hetero, list_pai_homo)[1])
            # context3['cnt_fvl_hetero_pai_homo_abort_1_c'] = mutations_2_abort(list_abort, list_fvl_hetero, list_pai_homo)[1]

            ######################################################
            ### Start Count Heterozygous Factor V       ##########
            ### Leiden and MTHFR Homo Mutation        ##########
            ######################################################

            # cnt_fvl_hetero_mthfr_homo_mutations = 0
            # cnt_fvl_hetero_mthfr_homo_mut_abort1 = 0
            # cnt_fvl_hetero_mthfr_homo_mut_aborts = 0
            #
            # for fvl_hetero in range(len(list_fvl_homo)):
            #     if list_fvl_hetero[fvl_hetero][0] == list_mthfr_homo[fvl_hetero][0] == '1.0':
            #         if list_abort[fvl_hetero][0] == '1.0':
            #             cnt_fvl_hetero_mthfr_homo_mut_abort1 = cnt_fvl_hetero_mthfr_homo_mut_abort1 + 1
            #         else:
            #             cnt_fvl_hetero_mthfr_homo_mut_aborts = cnt_fvl_hetero_mthfr_homo_mut_aborts + 1
            #         cnt_fvl_hetero_mthfr_homo_mutations = cnt_fvl_hetero_mthfr_homo_mutations + 1
            #
            # print('FVL Hetero and MTHFR Homo Mutations are:', cnt_fvl_hetero_mthfr_homo_mutations)
            # print('FVL Hetero and MTHFR Homo Mutations for Patients with 1 Abort are:')
            # print(cnt_fvl_hetero_mthfr_homo_mut_abort1)

            print('A 2 M4_0', mutations_2_abort(list_abort, list_fvl_hetero, list_mthfr_homo)[0])
            print('A 2 M4_1', mutations_2_abort(list_abort, list_fvl_hetero, list_mthfr_homo)[1])
            print('A 2 M4_2', mutations_2_abort(list_abort, list_fvl_hetero, list_mthfr_homo)[2])

            # print('1 A 2 M4 ', mutations_2_abort(list_abort, list_fvl_hetero, list_mthfr_homo)[0])
            context3['cnt_fvl_hetero_mthfr_homo_abort_0_c'] = \
            mutations_2_abort(list_abort, list_fvl_hetero, list_mthfr_homo)[0]

            # print('MORE A 2 M4 ', mutations_2_abort(list_abort, list_fvl_hetero, list_mthfr_homo)[1])
            # context3['cnt_fvl_hetero_mthfr_homo_abort_1_c'] = mutations_2_abort(list_abort, list_fvl_hetero, list_mthfr_homo)[1]

            ######################################################
            ### Start Count Homozygous Factor V         ##########
            ### Leiden and Prothrombin Hetero Mutation  ##########
            ######################################################

            # cnt_fvl_homo_prothr_hetero_mutations = 0
            # cnt_fvl_homo_prothr_hetero_mut_abort1 = 0
            # cnt_fvl_homo_prothr_hetero_mut_aborts = 0
            #
            # for fvl_homo in range(len(list_fvl_homo)):
            #     if list_fvl_homo[fvl_homo][0] == list_prothr_hetero[fvl_homo][0] == '1.0':
            #         if list_abort[fvl_homo][0] == '1.0':
            #             cnt_fvl_homo_prothr_hetero_mut_abort1 = cnt_fvl_homo_prothr_hetero_mut_abort1 + 1
            #         else:
            #             cnt_fvl_homo_prothr_hetero_mut_aborts = cnt_fvl_homo_prothr_hetero_mut_aborts + 1
            #         cnt_fvl_homo_prothr_hetero_mutations = cnt_fvl_homo_prothr_hetero_mutations + 1
            # print('FVL Homo and Prothr Hetero Mutations are:', cnt_fvl_homo_prothr_hetero_mutations)
            # print('FVL Homo and Prothr Hetero Mutations for Patients with 1 Abort are:')
            # print(cnt_fvl_homo_prothr_hetero_mut_abort1)

            print('A 2 M5_0', mutations_2_abort(list_abort, list_fvl_homo, list_prothr_hetero)[0])
            print('A 2 M5_1', mutations_2_abort(list_abort, list_fvl_homo, list_prothr_hetero)[1])
            print('A 2 M5_2', mutations_2_abort(list_abort, list_fvl_homo, list_prothr_hetero)[2])

            # print('1 A 2 M5 ', mutations_2_abort(list_abort, list_fvl_homo, list_prothr_hetero)[0])
            context3['cnt_fvl_homo_prothr_hetero_abort_0_c'] = \
            mutations_2_abort(list_abort, list_fvl_homo, list_prothr_hetero)[0]

            # print('MORE A 2 M5 ', mutations_2_abort(list_abort, list_fvl_homo, list_prothr_hetero)[1])
            # context3['cnt_fvl_homo_prothr_hetero_abort_1_c'] = mutations_2_abort(list_abort, list_fvl_homo, list_prothr_hetero)[1]

            ######################################################
            ### Start Count Homozygous Factor V         ##########
            ### Leiden and Prothrombin Homo Mutation    ##########
            ######################################################

            # cnt_fvl_homo_prothr_homo_mutations = 0
            # cnt_fvl_homo_prothr_homo_mut_abort1 = 0
            # cnt_fvl_homo_prothr_homo_mut_aborts = 0
            #
            # for fvl_homo in range(len(list_fvl_homo)):
            #     if list_fvl_homo[fvl_homo][0] == list_prothr_homo[fvl_homo][0] == '1.0':
            #         if list_abort[fvl_homo][0] == '1.0':
            #             cnt_fvl_homo_prothr_homo_mut_abort1 = cnt_fvl_homo_prothr_homo_mut_abort1 + 1
            #         else:
            #             cnt_fvl_homo_prothr_homo_mut_aborts = cnt_fvl_homo_prothr_homo_mut_aborts + 1
            #         cnt_fvl_homo_prothr_homo_mutations = cnt_fvl_homo_prothr_homo_mutations + 1
            # print('FVL Homo and Prothr Homo Mutations are:', cnt_fvl_homo_prothr_homo_mutations)
            # print('FVL Homo and Prothr Homo Mutations for Patients with 1 Abort are:')
            # print(cnt_fvl_homo_prothr_homo_mut_abort1)

            print('A 2 M6_0', mutations_2_abort(list_abort, list_fvl_homo, list_prothr_homo)[0])
            print('A 2 M6_1', mutations_2_abort(list_abort, list_fvl_homo, list_prothr_homo)[1])
            print('A 2 M6_2', mutations_2_abort(list_abort, list_fvl_homo, list_prothr_homo)[2])

            # print('1 A 2 M6 ', mutations_2_abort(list_abort, list_fvl_homo, list_prothr_homo)[0])
            context3['cnt_fvl_homo_prothr_homo_abort_0_c'] = \
            mutations_2_abort(list_abort, list_fvl_homo, list_prothr_homo)[0]

            # print('MORE A 2 M6 ', mutations_2_abort(list_abort, list_fvl_homo, list_prothr_homo)[1])
            # context3['cnt_fvl_homo_prothr_homo_abort_1_c'] = mutations_2_abort(list_abort, list_fvl_homo, list_prothr_homo)[1]

            ######################################################
            ### Start Count Homozygous Factor V         ##########
            ### Leiden and PAI I Homo Mutation          ##########
            ######################################################

            # cnt_fvl_homo_pai_homo_mutations = 0
            # cnt_fvl_homo_pai_homo_mut_abort1 = 0
            # cnt_fvl_homo_pai_homo_mut_aborts = 0
            #
            # for fvl_homo in range(len(list_fvl_homo)):
            #     if list_fvl_homo[fvl_homo][0] == list_pai_homo[fvl_homo][0] == '1.0':
            #         if list_abort[fvl_homo][0] == '1.0':
            #             cnt_fvl_homo_pai_homo_mut_abort1 = cnt_fvl_homo_pai_homo_mut_abort1 + 1
            #         else:
            #             cnt_fvl_homo_pai_homo_mut_aborts = cnt_fvl_homo_pai_homo_mut_aborts + 1
            #         cnt_fvl_homo_pai_homo_mutations = cnt_fvl_homo_pai_homo_mutations + 1
            # print('FVL Homo and PAI I Homo Mutations are:', cnt_fvl_homo_pai_homo_mutations)
            # print('FVL Homo and PAI I Homo Mutations for Patients with 1 Abort are:')
            # print(cnt_fvl_homo_pai_homo_mut_abort1)

            print('A 2 M7_0', mutations_2_abort(list_abort, list_fvl_homo, list_pai_homo)[0])
            print('A 2 M7_1', mutations_2_abort(list_abort, list_fvl_homo, list_pai_homo)[1])
            print('A 2 M7_2', mutations_2_abort(list_abort, list_fvl_homo, list_pai_homo)[2])

            # print('1 A 2 M7 ', mutations_2_abort(list_abort, list_fvl_homo, list_pai_homo)[0])
            context3['cnt_fvl_homo_pai_homo_abort_0_c'] = mutations_2_abort(list_abort, list_fvl_homo, list_pai_homo)[0]

            # print('MORE A 2 M7 ', mutations_2_abort(list_abort, list_fvl_homo, list_pai_homo)[1])
            # context3['cnt_fvl_homo_pai_homo_abort_1_c'] = mutations_2_abort(list_abort, list_fvl_homo, list_pai_homo)[1]

            ######################################################
            ### Start Count Homozygous Factor V         ##########
            ### Leiden and MTHFR Homo Mutation          ##########
            ######################################################

            # cnt_fvl_homo_mthfr_homo_mutations = 0
            # cnt_fvl_homo_mthfr_homo_mut_abort1 = 0
            # cnt_fvl_homo_mthfr_homo_mut_aborts = 0
            #
            # for fvl_homo in range(len(list_fvl_homo)):
            #     if list_fvl_homo[fvl_homo][0] == list_mthfr_homo[fvl_homo][0] == '1.0':
            #         if list_abort[fvl_homo][0] == '1.0':
            #             cnt_fvl_homo_mthfr_homo_mut_abort1 = cnt_fvl_homo_mthfr_homo_mut_abort1 + 1
            #         else:
            #             cnt_fvl_homo_mthfr_homo_mut_aborts = cnt_fvl_homo_mthfr_homo_mut_aborts + 1
            #         cnt_fvl_homo_mthfr_homo_mutations = cnt_fvl_homo_mthfr_homo_mutations + 1
            # print('FVL Homo and MTHFR Homo Mutations are:', cnt_fvl_homo_mthfr_homo_mutations)
            # print('FVL Homo and MTHFR Homo Mutations for Patients with 1 Abort are:')
            # print(cnt_fvl_homo_mthfr_homo_mut_abort1)

            print('A 2 M8_0', mutations_2_abort(list_abort, list_fvl_homo, list_mthfr_homo)[0])
            print('A 2 M8_1', mutations_2_abort(list_abort, list_fvl_homo, list_mthfr_homo)[1])
            print('A 2 M8_2', mutations_2_abort(list_abort, list_fvl_homo, list_mthfr_homo)[2])

            # print('1 A 2 M8 ', mutations_2_abort(list_abort, list_fvl_homo, list_mthfr_homo)[0])
            context3['cnt_fvl_homo_mrhfr_homo_abort_0_c'] = \
            mutations_2_abort(list_abort, list_fvl_homo, list_mthfr_homo)[0]

            # print('MORE A 2 M8 ', mutations_2_abort(list_abort, list_fvl_homo, list_mthfr_homo)[1])
            # context3['cnt_fvl_homo_mrhfr_homo_abort_1_c'] = mutations_2_abort(list_abort, list_fvl_homo, list_mthfr_homo)[1]

            ######################################################
            ### Start Count Heterozygous Prothrombin    ##########
            ### and PAI I Homo Mutation                 ##########
            ######################################################

            # cnt_prothr_hetero_pai_homo_mutations = 0
            # cnt_prothr_hetero_pai_homo_mut_abort0 = 0
            # cnt_prothr_hetero_pai_homo_mut_abort1 = 0
            # cnt_prothr_hetero_pai_homo_mut_aborts = 0
            #
            # for prothr_hetero in range(len(list_prothr_hetero)):
            #     if list_prothr_hetero[prothr_hetero][0] == '1.0' and list_pai_homo[prothr_hetero][0] == '1.0':
            #         if list_abort[prothr_hetero][0] == '1.0':
            #             cnt_prothr_hetero_pai_homo_mut_abort1 = cnt_prothr_hetero_pai_homo_mut_abort1 + 1
            #         elif list_abort[prothr_hetero][0] == '0.0':
            #             cnt_prothr_hetero_pai_homo_mut_abort0 = cnt_prothr_hetero_pai_homo_mut_abort0 + 1
            #         elif (
            #             list_abort[prothr_hetero][0] == '2.0' or
            #             list_abort[prothr_hetero][0] == '3.0' or
            #             list_abort[prothr_hetero][0] == '4.0' or
            #             list_abort[prothr_hetero][0] == '5.0' or
            #             list_abort[prothr_hetero][0] == '6.0' or
            #             list_abort[prothr_hetero][0] == '7.0' or
            #             list_abort[prothr_hetero][0] == '-' or
            #             list_abort[prothr_hetero][0] == ''):
            #
            #             cnt_prothr_hetero_pai_homo_mut_aborts = cnt_prothr_hetero_pai_homo_mut_aborts + 1
            #         cnt_prothr_hetero_pai_homo_mutations = cnt_prothr_hetero_pai_homo_mutations + 1
            # print('Prothrombin Hetero and PAI I Homo Mutations 0 Aborts are:', cnt_prothr_hetero_pai_homo_mut_abort0)
            # print('Prothrombin Hetero and PAI I Homo Mutations 1 Abort are: ', cnt_prothr_hetero_pai_homo_mut_abort1)
            # print('Prothrombin Hetero and PAI I Homo Mutations MORE Aborts are:', cnt_prothr_hetero_pai_homo_mut_aborts)

            # print('Prothrombin Hetero and PAI I Homo Mutations for Patients with 1 Abort are:')
            # print(cnt_prothr_hetero_pai_homo_mut_abort1)
            print('A 2 M9_0', mutations_2_abort(list_abort, list_prothr_hetero, list_pai_homo)[0])
            print('A 2 M9_1', mutations_2_abort(list_abort, list_prothr_hetero, list_pai_homo)[1])
            print('A 2 M9_2', mutations_2_abort(list_abort, list_prothr_hetero, list_pai_homo)[2])

            # print('1 A 2 M9 ', mutations_2_abort(list_abort, list_prothr_hetero, list_pai_homo)[0])
            context3['cnt_prothr_hetero_pai_homo_abort_0_c'] = mutations_2_abort(list_abort,
                                                                                 list_prothr_hetero,
                                                                                 list_pai_homo)[0]

            # print('MORE A 2 M9 ', mutations_2_abort(list_abort, list_prothr_hetero, list_pai_homo)[1])
            # context3['cnt_prothr_hetero_pai_homo_abort_1_c'] = mutations_2_abort(list_abort,
            #                                                                         list_prothr_hetero,
            #                                                                         list_pai_homo)[1]

            ######################################################
            ### Start Count Heterozygous Prothrombin    ##########
            ### and MTHFR Homo Mutation                 ##########
            ######################################################

            # cnt_prothr_hetero_mthfr_homo_mutations = 0
            # cnt_prothr_hetero_mthfr_homo_mut_abort1 = 0
            # cnt_prothr_hetero_mthfr_homo_mut_aborts = 0
            # cnt_prothr_hetero_mthfr_homo_mut_abort0 = 0
            #
            #
            # for prothr_hetero in range(len(list_prothr_hetero)):
            #     if list_prothr_hetero[prothr_hetero][0] == '1.0' and list_mthfr_homo[prothr_hetero][0] == '1.0':
            #         if list_abort[prothr_hetero][0] == '1.0':
            #             cnt_prothr_hetero_mthfr_homo_mut_abort1 = cnt_prothr_hetero_mthfr_homo_mut_abort1 + 1
            #         elif list_abort[prothr_hetero][0] == '0.0':
            #             cnt_prothr_hetero_mthfr_homo_mut_abort0 = cnt_prothr_hetero_mthfr_homo_mut_abort0 + 1
            #         elif (
            #             list_abort[prothr_hetero][0] == '2.0' or
            #             list_abort[prothr_hetero][0] == '3.0' or
            #             list_abort[prothr_hetero][0] == '4.0' or
            #             list_abort[prothr_hetero][0] == '5.0' or
            #             list_abort[prothr_hetero][0] == '6.0' or
            #             list_abort[prothr_hetero][0] == '7.0' or
            #             list_abort[prothr_hetero][0] == '-' or
            #             list_abort[prothr_hetero][0] == ''):
            #
            #             cnt_prothr_hetero_mthfr_homo_mut_aborts = cnt_prothr_hetero_mthfr_homo_mut_aborts + 1
            #         # cnt_prothr_hetero_pai_homo_mutations = cnt_prothr_hetero_pai_homo_mutations + 1
            # print('Prothrombin Hetero and MTHFR Homo Mutations 0 Aborts are:', cnt_prothr_hetero_mthfr_homo_mut_abort0)
            # print('Prothrombin Hetero and MTHFR Homo Mutations 1 Abort are: ', cnt_prothr_hetero_mthfr_homo_mut_abort1)
            # print('Prothrombin Hetero and MTHFR Homo Mutations MORE Aborts are:', cnt_prothr_hetero_mthfr_homo_mut_aborts)

            # for prothr_hetero in range(len(list_prothr_hetero)):
            #     if list_prothr_hetero[prothr_hetero][0] == list_mthfr_homo[prothr_hetero][0] == '1.0':
            #         if list_abort[prothr_hetero][0] == '1.0':
            #             cnt_prothr_hetero_mthfr_homo_mut_abort1 = cnt_prothr_hetero_mthfr_homo_mut_abort1 + 1
            #         else:
            #             cnt_prothr_hetero_mthfr_homo_mut_aborts = cnt_prothr_hetero_mthfr_homo_mut_aborts + 1
            #         cnt_prothr_hetero_mthfr_homo_mutations = cnt_prothr_hetero_mthfr_homo_mutations + 1
            # print('Prothrombin Hetero and MTHFR Homo Mutations are:', cnt_prothr_hetero_mthfr_homo_mutations)
            # print('Prothrombin Hetero and MTHFR Homo Mutations for Patients with 1 Abort are:')
            # print(cnt_prothr_hetero_mthfr_homo_mut_abort1)

            print('A 2 M10_0', mutations_2_abort(list_abort, list_prothr_hetero, list_mthfr_homo)[0])
            print('A 2 M10_1', mutations_2_abort(list_abort, list_prothr_hetero, list_mthfr_homo)[1])
            print('A 2 M10_2', mutations_2_abort(list_abort, list_prothr_hetero, list_mthfr_homo)[2])

            context3['cnt_prothr_hetero_mthfr_homo_abort_0_c'] = mutations_2_abort(list_abort,
                                                                                   list_prothr_hetero,
                                                                                   list_mthfr_homo)[0]

            # print('MORE A 2 M10', mutations_2_abort(list_abort, list_prothr_hetero, list_mthfr_homo)[1])
            # context3['cnt_prothr_hetero_mthfr_homo_abort_1_c'] = mutations_2_abort(list_abort,
            #                                                                           list_prothr_hetero,
            #                                                                           list_mthfr_homo)[1]

            ######################################################
            ### Start Count Homozygous PAI I            ##########
            ### and MTHFR Homo Mutation                 ##########
            ######################################################

            # cnt_pai_homo_mthfr_homo_mutations = 0
            # cnt_pai_homo_mthfr_homo_mut_abort1= 0
            # cnt_pai_homo_mthfr_homo_mut_aborts= 0
            #
            # for pai_homo in range(len(list_pai_homo)):
            #     if list_pai_homo[pai_homo][0] == list_mthfr_homo[pai_homo][0] == '1.0':
            #         if list_abort[pai_homo][0] == '1.0':
            #             cnt_pai_homo_mthfr_homo_mut_abort1 = cnt_pai_homo_mthfr_homo_mut_abort1 + 1
            #         else:
            #             cnt_pai_homo_mthfr_homo_mut_aborts = cnt_pai_homo_mthfr_homo_mut_aborts + 1
            #         cnt_pai_homo_mthfr_homo_mutations = cnt_pai_homo_mthfr_homo_mutations + 1
            # print('PAI I Homo and MTHFR Homo Mutations are:', cnt_pai_homo_mthfr_homo_mutations)
            # print('PAI I Homo and MTHFR Homo Mutations for Patients with 1 Abort are:')
            # print(cnt_pai_homo_mthfr_homo_mut_abort1)

            print('A 2 M11_0', mutations_2_abort(list_abort, list_pai_homo, list_mthfr_homo)[0])
            print('A 2 M11_1', mutations_2_abort(list_abort, list_pai_homo, list_mthfr_homo)[1])
            print('A 2 M11_2', mutations_2_abort(list_abort, list_pai_homo, list_mthfr_homo)[2])

            # print('1 A 2 M11', mutations_2_abort(list_abort, list_pai_homo, list_mthfr_homo)[0])
            context3['cnt_pai_homo_mthfr_homo_abort_0_c'] = mutations_2_abort(list_abort, list_pai_homo,
                                                                              list_mthfr_homo)[0]

            # print('MORE A 2 M11', mutations_2_abort(list_abort, list_pai_homo, list_mthfr_homo)[1])
            # context3['cnt_pai_homo_mthfr_homo_abort_1_c'] = mutations_2_abort(list_abort, list_pai_homo,
            #                                                                   list_mthfr_homo)[1]

            ######################################################
            ### Start Count Heterozygous Factor V       ##########
            ### Leiden Mutation for 1 Abort             ##########
            ######################################################
            cnt_fvl_hetero_mut_1_abort = 0
            for in_fvl_hetero_abort_1 in range(len(list_abort)):
                if ((list_abort[in_fvl_hetero_abort_1][0] == '1.0') and
                        list_fvl_hetero[in_fvl_hetero_abort_1][0] == '1.0'):
                    cnt_fvl_hetero_mut_1_abort = cnt_fvl_hetero_mut_1_abort + 1
            print('FVL Hetero Mutations for 1 abort:', cnt_fvl_hetero_mut_1_abort)

            ######################################################
            ### Start Count Homozygous Factor V         ##########
            ### Leiden Mutation for 1 Abort             ##########
            ######################################################
            cnt_fvl_homo_mut_1_abort = 0
            for in_fvl_homo_abort_1 in range(len(list_abort)):
                if ((list_abort[in_fvl_homo_abort_1][0] == '1.0') and
                        list_fvl_homo[in_fvl_homo_abort_1][0] == '1.0'):
                    cnt_fvl_homo_mut_1_abort = cnt_fvl_homo_mut_1_abort + 1
            print('FVL Homo Mutations for 1 abort:', cnt_fvl_homo_mut_1_abort)

            ######################################################
            ### Start Count Factor II(Prothrombin)            ####
            ### Heterozygous Mutation for 1 Abort             ####
            ######################################################
            cnt_prothr_hetero_mut_1_abort = 0
            for in_prothr_hetero_abort_1 in range(len(list_abort)):
                if ((list_abort[in_prothr_hetero_abort_1][0] == '1.0') and
                        list_prothr_hetero[in_prothr_hetero_abort_1][0] == '1.0'):
                    cnt_prothr_hetero_mut_1_abort = cnt_prothr_hetero_mut_1_abort + 1
            print('FVL Hetero Mutations for 1 abort:', cnt_prothr_hetero_mut_1_abort)

            ######################################################
            ### Start Count Factor II(Prothrombin)            ####
            ### Homozygous Mutation for 1 Abort               ####
            ######################################################
            cnt_prothr_homo_mut_1_abort = 0
            for in_prothr_homo_abort_1 in range(len(list_abort)):
                if ((list_abort[in_prothr_homo_abort_1][0] == '1.0') and
                        list_prothr_homo[in_prothr_homo_abort_1][0] == '1.0'):
                    cnt_prothr_homo_mut_1_abort = cnt_prothr_homo_mut_1_abort + 1
            print('PROTHR Homo Mutations for 1 abort:', cnt_prothr_homo_mut_1_abort)

            ######################################################
            ### Start Count Factor PAI I Homozigous           ####
            ### Mutation for 1 Abort                          ####
            ######################################################
            cnt_pai_homo_mut_1_abort = 0
            for in_pai_homo_abort_1 in range(len(list_abort)):
                if ((list_abort[in_pai_homo_abort_1][0] == '1.0') and
                        list_pai_homo[in_pai_homo_abort_1][0] == '1.0'):
                    cnt_pai_homo_mut_1_abort = cnt_pai_homo_mut_1_abort + 1
            print('PAI I Homo Mutations for 1 abort:', cnt_pai_homo_mut_1_abort)

            ######################################################
            ### Start Count Factor MTHFR                      ####
            ### Homozygous Mutation for 1 Abort               ####
            ######################################################
            cnt_mthfr_homo_mut_1_abort = 0
            for in_mthfr_homo_abort_1 in range(len(list_abort)):
                if ((list_abort[in_mthfr_homo_abort_1][0] == '1.0') and
                        list_mthfr_homo[in_mthfr_homo_abort_1][0] == '1.0'):
                    cnt_mthfr_homo_mut_1_abort = cnt_mthfr_homo_mut_1_abort + 1
            print('MTHFR Homo Mutations for 1 abort:', cnt_mthfr_homo_mut_1_abort)

            ######################################################
            ### Start Count Count Heterozygous Factor V ##########
            ### Leiden Mutation for 2 or 3 Aborts       ##########
            ###        1 MUTATION FOR 2 OR MORE ABORTS        ####
            ######################################################
            cnt_fvl_hetero_mut_2_3_aborts = 0
            for in_fvl_hetero_aborts_2 in range(len(list_abort)):
                if ((list_abort[in_fvl_hetero_aborts_2][0] == '2.0' or
                     list_abort[in_fvl_hetero_aborts_2][0] == '3.0' or
                     list_abort[in_fvl_hetero_aborts_2][0] == '4.0' or
                     list_abort[in_fvl_hetero_aborts_2][0] == '5.0' or
                     list_abort[in_fvl_hetero_aborts_2][0] == '6.0' or
                     list_abort[in_fvl_hetero_aborts_2][0] == '7.0' or
                     list_abort[in_fvl_hetero_aborts_2][0] == '-' or
                     list_abort[in_fvl_hetero_aborts_2][0] == ''
                ) and
                        list_fvl_hetero[in_fvl_hetero_aborts_2][0] == '1.0'):
                    cnt_fvl_hetero_mut_2_3_aborts = cnt_fvl_hetero_mut_2_3_aborts + 1
            print('FVL Hetero Mutations 2 or more are:', cnt_fvl_hetero_mut_2_3_aborts)

            ######################################################
            ### End Count Count Heterozygous Factor V   ##########
            ### Leiden Mutation for 2 or 3 Aborts       ##########
            ###        1 MUTATION FOR 2 OR MORE ABORTS        ####
            ######################################################

            ######################################################
            ### Start Count Count Homozygous Factor V   ##########
            ### Leiden Mutation for 2 or 3 Aborts       ##########
            ###        1 MUTATION FOR 2 OR MORE ABORTS        ####
            ######################################################
            cnt_fvl_homo_mut_2_3_aborts = 0
            for in_fvl_homo_aborts_2 in range(len(list_abort)):
                if ((list_abort[in_fvl_homo_aborts_2][0] == '2.0' or
                     list_abort[in_fvl_homo_aborts_2][0] == '3.0' or
                     list_abort[in_fvl_homo_aborts_2][0] == '4.0' or
                     list_abort[in_fvl_homo_aborts_2][0] == '5.0' or
                     list_abort[in_fvl_homo_aborts_2][0] == '6.0' or
                     list_abort[in_fvl_homo_aborts_2][0] == '7.0' or
                     list_abort[in_fvl_homo_aborts_2][0] == '-' or
                     list_abort[in_fvl_homo_aborts_2][0] == ''
                ) and
                        list_fvl_homo[in_fvl_homo_aborts_2][0] == '1.0'):
                    cnt_fvl_homo_mut_2_3_aborts = cnt_fvl_homo_mut_2_3_aborts + 1
            print('FVL Homo Mutations 2 or more are:', cnt_fvl_homo_mut_2_3_aborts)

            ######################################################
            ###       Start Count Factor II(Prothrombin)      ####
            ###             Heterozygous Mutation             ####
            ###        1 MUTATION FOR 2 OR MORE ABORTS        ####
            ######################################################
            cnt_prothr_hetero_mut_2_3_aborts = 0
            for in_prothr_hetero_aborts_2 in range(len(list_abort)):
                if ((list_abort[in_prothr_hetero_aborts_2][0] == '2.0' or
                     list_abort[in_prothr_hetero_aborts_2][0] == '3.0' or
                     list_abort[in_prothr_hetero_aborts_2][0] == '4.0' or
                     list_abort[in_prothr_hetero_aborts_2][0] == '5.0' or
                     list_abort[in_prothr_hetero_aborts_2][0] == '6.0' or
                     list_abort[in_prothr_hetero_aborts_2][0] == '7.0' or
                     list_abort[in_prothr_hetero_aborts_2][0] == '-' or
                     list_abort[in_prothr_hetero_aborts_2][0] == ''
                ) and
                        list_prothr_hetero[in_prothr_hetero_aborts_2][0] == '1.0'):
                    cnt_prothr_hetero_mut_2_3_aborts = cnt_prothr_hetero_mut_2_3_aborts + 1
            print('PROTHR Hetero Mutations 2 or more are:', cnt_prothr_hetero_mut_2_3_aborts)
            ######################################################
            ###       Start Count Factor II(Prothrombin)      ####
            ###             Homozygous Mutation               ####
            ###        1 MUTATION FOR 2 OR MORE ABORTS        ####
            ######################################################
            cnt_prothr_homo_mut_2_3_aborts = 0
            for in_prothr_homo_aborts_2 in range(len(list_abort)):
                if ((list_abort[in_prothr_homo_aborts_2][0] == '2.0' or
                     list_abort[in_prothr_homo_aborts_2][0] == '3.0' or
                     list_abort[in_prothr_homo_aborts_2][0] == '4.0' or
                     list_abort[in_prothr_homo_aborts_2][0] == '5.0' or
                     list_abort[in_prothr_homo_aborts_2][0] == '6.0' or
                     list_abort[in_prothr_homo_aborts_2][0] == '7.0' or
                     list_abort[in_prothr_homo_aborts_2][0] == '-' or
                     list_abort[in_prothr_homo_aborts_2][0] == ''
                ) and
                        list_prothr_homo[in_prothr_homo_aborts_2][0] == '1.0'):
                    cnt_prothr_homo_mut_2_3_aborts = cnt_prothr_homo_mut_2_3_aborts + 1
            print('PROTHR Homo Mutations 2 or more are:', cnt_prothr_homo_mut_2_3_aborts)
            ######################################################
            ### Start Count Factor PAI I Homozigous Mutation  ####
            ###        1 MUTATION FOR 2 OR MORE ABORTS        ####
            ######################################################
            cnt_pai_homo_mut_2_3_aborts = 0
            for in_pai_homo_aborts_2 in range(len(list_abort)):
                if ((list_abort[in_pai_homo_aborts_2][0] == '2.0' or
                     list_abort[in_pai_homo_aborts_2][0] == '3.0' or
                     list_abort[in_pai_homo_aborts_2][0] == '4.0' or
                     list_abort[in_pai_homo_aborts_2][0] == '5.0' or
                     list_abort[in_pai_homo_aborts_2][0] == '6.0' or
                     list_abort[in_pai_homo_aborts_2][0] == '7.0' or
                     list_abort[in_pai_homo_aborts_2][0] == '-' or
                     list_abort[in_pai_homo_aborts_2][0] == ''
                ) and
                        list_pai_homo[in_pai_homo_aborts_2][0] == '1.0'):
                    cnt_pai_homo_mut_2_3_aborts = cnt_pai_homo_mut_2_3_aborts + 1
            print('PAI Homo Mutations 2 or more are:', cnt_pai_homo_mut_2_3_aborts)
            ######################################################
            ### Start Count Factor MTHFR Homozigous Mutation  ####
            ###        1 MUTATION FOR 2 OR MORE ABORTS        ####
            ######################################################
            cnt_mthfr_homo_mut_2_3_aborts = 0
            for in_mthfr_homo_aborts_2 in range(len(list_abort)):
                if ((list_abort[in_mthfr_homo_aborts_2][0] == '2.0' or
                     list_abort[in_mthfr_homo_aborts_2][0] == '3.0' or
                     list_abort[in_mthfr_homo_aborts_2][0] == '4.0' or
                     list_abort[in_mthfr_homo_aborts_2][0] == '5.0' or
                     list_abort[in_mthfr_homo_aborts_2][0] == '6.0' or
                     list_abort[in_mthfr_homo_aborts_2][0] == '7.0' or
                     list_abort[in_mthfr_homo_aborts_2][0] == '-' or
                     list_abort[in_mthfr_homo_aborts_2][0] == ''
                ) and
                        list_mthfr_homo[in_mthfr_homo_aborts_2][0] == '1.0'):
                    cnt_mthfr_homo_mut_2_3_aborts = cnt_mthfr_homo_mut_2_3_aborts + 1
            print('MTHFR Homo Mutations 2 or more are:', cnt_mthfr_homo_mut_2_3_aborts)
            ######################################################
            ### Start Count Factor FVL Heterozigous Mutation  ####
            ###                ALL PATIENTS                   ####
            ######################################################
            cnt_fvl_hetero_mutations = 0
            for fvl_hetero_data in list_fvl_hetero:
                if fvl_hetero_data[0] == '1.0':
                    cnt_fvl_hetero_mutations = cnt_fvl_hetero_mutations + 1
            print('FVL Hetero Mutations are:', cnt_fvl_hetero_mutations)
            ######################################################
            ### Start Count Factor FVL Homozygous Mutation    ####
            ###                ALL PATIENTS                   ####
            ######################################################
            cnt_fvl_homo_mutations = 0
            for fvl_homo_data in list_fvl_homo:
                if fvl_homo_data[0] == '1.0':
                    cnt_fvl_homo_mutations = cnt_fvl_homo_mutations + 1
            print('FVL Homo Mutations are:', cnt_fvl_homo_mutations)
            ######################################################
            ###       Start Count Factor II(Prothrombin)      ####
            ###             Heterozygous Mutation             ####
            ###                ALL PATIENTS                   ####
            ######################################################
            cnt_prothr_hetero_mutations = 0
            for prothr_hetero_data in list_prothr_hetero:
                if prothr_hetero_data[0] == '1.0':
                    cnt_prothr_hetero_mutations = cnt_prothr_hetero_mutations + 1
            print('PROTHR Hetero Mutations are:', cnt_prothr_hetero_mutations)
            ######################################################
            ###       Start Count Factor II(Prothrombin)      ####
            ###             Homozygous Mutation               ####
            ###                ALL PATIENTS                   ####
            ######################################################
            cnt_prothr_homo_mutations = 0
            for prothr_homo_data in list_prothr_homo:
                if prothr_homo_data[0] == '1.0':
                    cnt_prothr_homo_mutations = cnt_prothr_homo_mutations + 1
            print('PROTHR Homo Mutations are:', cnt_prothr_homo_mutations)
            ######################################################
            ### Start Count Factor PAI I Homozygous Mutation  ####
            ###                ALL PATIENTS                   ####
            ######################################################
            cnt_pai_homo_mutations = 0
            for pai_homo_data in list_pai_homo:
                if pai_homo_data[0] == '1.0':
                    cnt_pai_homo_mutations = cnt_pai_homo_mutations + 1
            print('PAI Homo Mutations are:', cnt_pai_homo_mutations)
            ######################################################
            ### Start Count Factor MTHFR Homozygous Mutation  ####
            ###                ALL PATIENTS                   ####
            ######################################################
            cnt_mthfr_homo_mutations = 0
            for mthfr_homo_data in list_mthfr_homo:
                if mthfr_homo_data[0] == '1.0':
                    cnt_mthfr_homo_mutations = cnt_mthfr_homo_mutations + 1
            print('MTHFR Homo Mutations are:', cnt_mthfr_homo_mutations)

            context3['fvl_hetero_mut_1_abort'] = cnt_fvl_hetero_mut_1_abort
            context3['fvl_homo_mut_1_abort'] = cnt_fvl_homo_mut_1_abort
            context3['prothr_hetero_mut_1_abort'] = cnt_prothr_hetero_mut_1_abort
            context3['prothr_homo_mut_1_abort'] = cnt_prothr_homo_mut_1_abort
            context3['pai_homo_mut_1_abort'] = cnt_pai_homo_mut_1_abort
            context3['mthfr_homo_mut_1_abort'] = cnt_mthfr_homo_mut_1_abort

            # context3['cnt_fvl_hetero_prothr_hetero_mutations'] = cnt_fvl_hetero_prothr_hetero_mutations
            # context3['cnt_fvl_hetero_prothr_homo_mutations'] = cnt_fvl_hetero_prothr_homo_mutations
            # context3['cnt_fvl_hetero_pai_homo_mutations'] = cnt_fvl_hetero_pai_homo_mutations
            # context3['cnt_fvl_hetero_mthfr_homo_mutations'] = cnt_fvl_hetero_mthfr_homo_mutations
            # context3['cnt_fvl_homo_prothr_hetero_mutations'] = cnt_fvl_homo_prothr_hetero_mutations
            # context3['cnt_fvl_homo_prothr_homo_mutations'] = cnt_fvl_homo_prothr_homo_mutations
            # context3['cnt_fvl_homo_pai_homo_mutations'] = cnt_fvl_homo_pai_homo_mutations
            # context3['cnt_fvl_homo_mthfr_homo_mutations'] = cnt_fvl_homo_mthfr_homo_mutations
            # context3['cnt_prothr_hetero_pai_homo_mutations'] = cnt_prothr_hetero_pai_homo_mutations
            # context3['cnt_prothr_hetero_mthfr_homo_mutations'] = cnt_prothr_hetero_mthfr_homo_mutations
            # context3['cnt_pai_homo_mthfr_homo_mutations'] = cnt_pai_homo_mthfr_homo_mutations

            # context3['cnt_fvl_hetero_prothr_hetero_mut_abort1'] = cnt_fvl_hetero_prothr_hetero_mut_abort1
            # context3['cnt_fvl_hetero_prothr_homo_mut_abort1'] = cnt_fvl_hetero_prothr_homo_mut_abort1
            # context3['cnt_fvl_hetero_pai_homo_mut_abort1'] = cnt_fvl_hetero_pai_homo_mut_abort1
            # context3['cnt_fvl_hetero_mthfr_homo_mut_abort1'] = cnt_fvl_hetero_mthfr_homo_mut_abort1
            # context3['cnt_fvl_homo_prothr_hetero_mut_abort1'] = cnt_fvl_homo_prothr_hetero_mut_abort1
            # context3['cnt_fvl_homo_prothr_homo_mut_abort1'] = cnt_fvl_homo_prothr_homo_mut_abort1
            # context3['cnt_fvl_homo_pai_homo_mut_abort1'] = cnt_fvl_homo_pai_homo_mut_abort1
            # context3['cnt_fvl_homo_mthfr_homo_mut_abort1'] = cnt_fvl_homo_mthfr_homo_mut_abort1
            # context3['cnt_prothr_hetero_pai_homo_mut_abort1'] = cnt_prothr_hetero_pai_homo_mut_abort1
            # context3['cnt_prothr_hetero_mthfr_homo_mut_abort1'] = cnt_prothr_hetero_mthfr_homo_mut_abort1
            # context3['cnt_pai_homo_mthfr_homo_mut_abort1'] = cnt_pai_homo_mthfr_homo_mut_abort1

            # context3['cnt_fvl_hetero_prothr_hetero_mut_aborts'] = cnt_fvl_hetero_prothr_hetero_mut_aborts
            # context3['cnt_fvl_hetero_prothr_homo_mut_aborts'] = cnt_fvl_hetero_prothr_homo_mut_aborts
            # context3['cnt_fvl_hetero_pai_homo_mut_aborts'] = cnt_fvl_hetero_pai_homo_mut_aborts
            # context3['cnt_fvl_hetero_mthfr_homo_mut_aborts'] = cnt_fvl_hetero_mthfr_homo_mut_aborts
            # context3['cnt_fvl_homo_prothr_hetero_mut_aborts'] = cnt_fvl_homo_prothr_hetero_mut_aborts
            # context3['cnt_fvl_homo_prothr_homo_mut_aborts'] = cnt_fvl_homo_prothr_homo_mut_aborts
            # context3['cnt_fvl_homo_pai_homo_mut_aborts'] = cnt_fvl_homo_pai_homo_mut_aborts
            # context3['cnt_fvl_homo_mthfr_homo_mut_aborts'] = cnt_fvl_homo_mthfr_homo_mut_aborts
            # context3['cnt_prothr_hetero_pai_homo_mut_aborts'] = cnt_prothr_hetero_pai_homo_mut_aborts
            # context3['cnt_prothr_hetero_mthfr_homo_mut_aborts'] = cnt_prothr_hetero_mthfr_homo_mut_aborts
            # context3['cnt_pai_homo_mthfr_homo_mut_aborts'] = cnt_pai_homo_mthfr_homo_mut_aborts

            ###        1 MUTATION FOR ALL PATIENTS           ####
            context3['mthfr_homo_mut'] = cnt_mthfr_homo_mutations
            context3['pai_homo_mut'] = cnt_pai_homo_mutations
            context3['prothr_homo_mut'] = cnt_prothr_homo_mutations
            context3['prothr_hetero_mut'] = cnt_prothr_hetero_mutations
            context3['fvl_homo_mut'] = cnt_fvl_homo_mutations
            context3['fvl_hetero_mut'] = cnt_fvl_hetero_mutations
            ###        1 MUTATION FOR 2 OR MORE ABORTS        ####
            context3['2_3_aborts_mthfr_homo_mut'] = cnt_mthfr_homo_mut_2_3_aborts
            context3['2_3_aborts_pai_homo_mut'] = cnt_pai_homo_mut_2_3_aborts
            context3['2_3_aborts_prothr_homo_mut'] = cnt_prothr_homo_mut_2_3_aborts
            context3['2_3_aborts_prothr_hetero_mut'] = cnt_prothr_hetero_mut_2_3_aborts
            context3['2_3_aborts_fvl_homo_mut'] = cnt_fvl_homo_mut_2_3_aborts
            context3['2_3_aborts_fvl_hetero_mut'] = cnt_fvl_hetero_mut_2_3_aborts

    return render(request, 'calc_patients_more_mut_controli.html', context3)


# Function, izvikana ot button "Results: Mutations" za Patients
def calc_patients_more_mut_p(request):
    context3 = {}
    prida_mutations = PridaMutations.objects.all()

    list_age = PridaMutations.objects.values_list('age')
    print('AGE', list_age)

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
    # print('LIST ABORT', list_abort)
    # x = slice(0, 900)
    # print('LIST ABORT 2', list_abort[x])
    # print('LIST FVL HETERO', list_fvl_hetero[x])
    # print('LIST FVL HOMO  ', list_fvl_homo[x])
    # print('LIST PRo HETERO', list_prothr_hetero[x])
    # print('LIST PRo HOMO  ', list_prothr_homo[x])
    # print('LIST PAI HOMO  ', list_pai_homo[x])
    # print('LIST MTHFR HOMO', list_mthfr_homo[x])

    if request.method == 'POST':
        if 'btn_patients_more_mutations' in request.POST:
            print('Patients')
            #####################################################
            ### Start 1 Abort 3 Mutations #######################
            #####################################################
            count_abort1_mutations3 = 0
            for in_abort in range(20):

                # for in_abort in range(len(list_abort)):
                if ((list_abort[in_abort][0] == '1.0')
                        and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][
                            0] == '1.0'
                             or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                             or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] ==
                             list_pai_homo[in_abort][0] == '1.0'
                             or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] ==
                             list_pai_homo[in_abort][0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][
                                 0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                        )
                ):
                    count_abort1_mutations3 = count_abort1_mutations3 + 1
            print('1 Abort and 3 mutations: ', count_abort1_mutations3)
            context3['cnt_abort1_mutations3'] = count_abort1_mutations3

            #####################################################
            ### End 1 Abort 3 Mutations #########################
            #####################################################

            #####################################################
            ### Start 2 Aborts 3 Mutations ######################
            #####################################################
            count_abort2_mutations3 = 0
            for in_abort in range(10):

                # for in_abort in range(len(list_abort)):
                if ((list_abort[in_abort][0] == '2.0')
                        and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][
                            0] == '1.0'
                             or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                             or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] ==
                             list_pai_homo[in_abort][0] == '1.0'
                             or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] ==
                             list_pai_homo[in_abort][0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][
                                 0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                        )
                ):
                    count_abort2_mutations3 = count_abort2_mutations3 + 1
            print('2 Aborts and 3 mutations: ', count_abort2_mutations3)

            #####################################################
            ### End 2 Aborts 3 Mutations ########################
            #####################################################

            #####################################################
            ### Start 3 Aborts 3 Mutations ######################
            #####################################################
            count_abort3_mutations3 = 0
            for in_abort in range(len(list_abort)):
                if ((list_abort[in_abort][0] == '3.0')
                        and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][
                            0] == '1.0'
                             or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                             or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] ==
                             list_pai_homo[in_abort][0] == '1.0'
                             or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] ==
                             list_pai_homo[in_abort][0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][
                                 0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                        )
                ):
                    count_abort3_mutations3 = count_abort3_mutations3 + 1
            print('3 Aborts and 3 mutations: ', count_abort3_mutations3)

            #####################################################
            ### End 3 Aborts 3 Mutations ########################
            #####################################################

            #####################################################
            ### Start 4 Aborts 3 Mutations ######################
            #####################################################
            count_abort4_mutations3 = 0
            for in_abort in range(len(list_abort)):
                if ((list_abort[in_abort][0] == '4.0')
                        and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][
                            0] == '1.0'
                             or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                             or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] ==
                             list_pai_homo[in_abort][0] == '1.0'
                             or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] ==
                             list_pai_homo[in_abort][0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][
                                 0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                        )
                ):
                    count_abort4_mutations3 = count_abort4_mutations3 + 1
            print('4 Aborts and 3 mutations: ', count_abort4_mutations3)
            print('\n')

            #####################################################
            ### End 4 Aborts 3 Mutations ########################
            #####################################################

            #####################################################
            ### Start 1 Abort 2 Mutations ######################
            #####################################################
            # count_abort1_mutations_2 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '1.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_pai_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0')
            #     ):
            #         count_abort1_mutations_2 = count_abort1_mutations_2 + 1
            # print('1 Abort and 2 mutations: ', count_abort1_mutations_2)

            #####################################################
            ### End 1 Abort 2 Mutations #########################
            #####################################################

            ######################################################
            ### Start 2 Aborts and 2 mutations ###################
            ######################################################
            # count_abort2_mutations2 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '2.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_pai_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0')
            #     ):
            #         count_abort2_mutations2 = count_abort2_mutations2 + 1
            # print('2 Aborts and 2 mutations: ', count_abort2_mutations2)

            ######################################################
            ### End 2 Aborts and 2 mutations #####################
            ######################################################

            ######################################################
            ### Start 3 Aborts and 2 mutations ###################
            ######################################################
            # count_abort3_mutations2 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '3.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_pai_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0')
            #     ):
            #         count_abort3_mutations2 = count_abort3_mutations2 + 1
            # print('3 Aborts and 2 mutations: ', count_abort3_mutations2)

            ######################################################
            ### End 3 Aborts and 2 mutations #####################
            ######################################################

            ######################################################
            ### Start 4 Aborts and 2 mutations ###################
            ######################################################
            # count_abort4_mutations2 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '4.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_pai_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0')
            #     ):
            #         count_abort4_mutations2 = count_abort4_mutations2 + 1
            # print('4 Aborts and 2 mutations: ', count_abort4_mutations2)

            ######################################################
            ### End 4 Aborts and 2 mutations #####################
            ######################################################

            ######################################################
            ### Start 5 Aborts and 2 mutations ###################
            ######################################################
            # count_abort5_mutations2 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '5.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_pai_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0')
            #     ):
            #         count_abort5_mutations2 = count_abort5_mutations2 + 1
            # print('5 Aborts and 2 mutations: ', count_abort5_mutations2)

            ######################################################
            ### End 5 Aborts and 2 mutations #####################
            ######################################################

            ######################################################
            ### Start 6 Aborts and 2 mutations ###################
            ######################################################
            # count_abort6_mutations2 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '6.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_pai_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0')
            #     ):
            #         count_abort6_mutations2 = count_abort6_mutations2 + 1
            # print('6 Aborts and 2 mutations: ', count_abort6_mutations2)

            ######################################################
            ### End 6 Aborts and 2 mutations #####################
            ######################################################

            ######################################################
            ### Start 7 Aborts and 2 mutations ###################
            ######################################################
            # count_abort7_mutations2 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '7.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_pai_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0')
            #     ):
            #         count_abort7_mutations2 = count_abort7_mutations2 + 1
            # print('7 Aborts and 2 mutations: ', count_abort7_mutations2)
            # print('\n')
            ######################################################
            ### End 7 Aborts and 2 mutations #####################
            ######################################################

            ######################################################
            ###    Heterozygous Factor V Leiden Mutation    ######
            ###  Factor II (Prothrombin) Heterozygous Mutation ###
            ###        Factor PAI I Homozygous Mutation      #####
            ###         3 Mutations 1 Abort                    ###
            ######################################################

            cnt_fvl_hetero_pr_hetero_pai_homo_mutations = 0
            cnt_fvl_hetero_pr_hetero_pai_homo_mut_abort1 = 0
            cnt_fvl_hetero_pr_hetero_pai_homo_mut_aborts = 0

            for fvl_hetero in range(len(list_fvl_hetero)):
                if (
                        list_fvl_hetero[fvl_hetero][0] == '1.0' and
                        list_prothr_hetero[fvl_hetero][0] == '1.0' and
                        list_pai_homo[fvl_hetero][0] == '1.0'):

                    if list_abort[fvl_hetero][0] == '1.0':
                        cnt_fvl_hetero_pr_hetero_pai_homo_mut_abort1 = cnt_fvl_hetero_pr_hetero_pai_homo_mut_abort1 + 1
                    else:
                        cnt_fvl_hetero_pr_hetero_pai_homo_mut_aborts = cnt_fvl_hetero_pr_hetero_pai_homo_mut_aborts + 1
                    cnt_fvl_hetero_pr_hetero_pai_homo_mutations = cnt_fvl_hetero_pr_hetero_pai_homo_mutations + 1

            print('FVL Hetero, PROTHR Hetero, PAI Homo Mutations, 1 Abort are:',
                  cnt_fvl_hetero_pr_hetero_pai_homo_mut_abort1)
            print('FVL Hetero and PROTHR Hetero, PAI Homo Mutations 2 more Aborts are:',
                  cnt_fvl_hetero_pr_hetero_pai_homo_mut_aborts)
            print('All Patients are:', cnt_fvl_hetero_pr_hetero_pai_homo_mutations)

            context3['cnt_fvl_hetero_pr_hetero_pai_homo_mutations'] = cnt_fvl_hetero_pr_hetero_pai_homo_mutations
            context3['cnt_fvl_hetero_pr_hetero_pai_homo_mut_abort1'] = cnt_fvl_hetero_pr_hetero_pai_homo_mut_abort1
            context3['cnt_fvl_hetero_pr_hetero_pai_homo_mut_aborts'] = cnt_fvl_hetero_pr_hetero_pai_homo_mut_aborts

            ######################################################
            ###    Heterozygous Factor V Leiden Mutation    ######
            ###  Factor II (Prothrombin) Heterozygous Mutation ###
            ###        Factor MTHFR Homozygous Mutation      #####
            ###         3 Mutations 1 Abort                    ###
            ######################################################

            cnt_fvl_hetero_pr_hetero_mthfr_homo_mutations = 0
            cnt_fvl_hetero_pr_hetero_mthfr_homo_mut_abort1 = 0
            cnt_fvl_hetero_pr_hetero_mthfr_homo_mut_aborts = 0

            for fvl_hetero in range(len(list_fvl_hetero)):
                if (
                        list_fvl_hetero[fvl_hetero][0] == '1.0' and
                        list_prothr_hetero[fvl_hetero][0] == '1.0' and
                        list_mthfr_homo[fvl_hetero][0] == '1.0'):

                    if list_abort[fvl_hetero][0] == '1.0':
                        cnt_fvl_hetero_pr_hetero_mthfr_homo_mut_abort1 = cnt_fvl_hetero_pr_hetero_mthfr_homo_mut_abort1 + 1
                    else:
                        cnt_fvl_hetero_pr_hetero_mthfr_homo_mut_aborts = cnt_fvl_hetero_pr_hetero_mthfr_homo_mut_aborts + 1
                    cnt_fvl_hetero_pr_hetero_mthfr_homo_mutations = cnt_fvl_hetero_pr_hetero_mthfr_homo_mutations + 1

            print('All Patients are:', cnt_fvl_hetero_pr_hetero_mthfr_homo_mutations)
            print('FVL Hetero, PROTHR Hetero, MTHFR Homo Mutations, 1 Abort are:',
                  cnt_fvl_hetero_pr_hetero_mthfr_homo_mut_abort1)
            print('FVL Hetero and PROTHR Hetero, MTHFR Homo Mutations 2 more Aborts are:',
                  cnt_fvl_hetero_pr_hetero_mthfr_homo_mut_aborts)

            context3['cnt_fvl_hetero_pr_hetero_mthfr_homo_mutations'] = cnt_fvl_hetero_pr_hetero_mthfr_homo_mutations
            context3['cnt_fvl_hetero_pr_hetero_mthfr_homo_mut_abort1'] = cnt_fvl_hetero_pr_hetero_mthfr_homo_mut_abort1
            context3['cnt_fvl_hetero_pr_hetero_mthfr_homo_mut_aborts'] = cnt_fvl_hetero_pr_hetero_mthfr_homo_mut_aborts

            ######################################################
            ###    Heterozygous Factor V Leiden Mutation    ######
            ###  Factor II (Prothrombin) Homozygous Mutation   ###
            ###        Factor PAI I Homozygous Mutation      #####
            ###         3 Mutations 1 Abort                    ###
            ######################################################

            cnt_fvl_hetero_pr_homo_pai_homo_mutations = 0
            cnt_fvl_hetero_pr_homo_pai_homo_mut_abort1 = 0
            cnt_fvl_hetero_pr_homo_pai_homo_mut_aborts = 0

            for fvl_hetero in range(len(list_fvl_hetero)):
                if (
                        list_fvl_hetero[fvl_hetero][0] == '1.0' and
                        list_prothr_homo[fvl_hetero][0] == '1.0' and
                        list_pai_homo[fvl_hetero][0] == '1.0'):

                    if list_abort[fvl_hetero][0] == '1.0':
                        cnt_fvl_hetero_pr_homo_pai_homo_mut_abort1 = cnt_fvl_hetero_pr_homo_pai_homo_mut_abort1 + 1
                    else:
                        cnt_fvl_hetero_pr_homo_pai_homo_mut_aborts = cnt_fvl_hetero_pr_homo_pai_homo_mut_aborts + 1
                    cnt_fvl_hetero_pr_homo_pai_homo_mutations = cnt_fvl_hetero_pr_homo_pai_homo_mutations + 1

            print('All Patients are:', cnt_fvl_hetero_pr_homo_pai_homo_mutations)
            print('FVL Hetero, PROTHR Homo, PAI Homo Mutations, 1 Abort are:',
                  cnt_fvl_hetero_pr_homo_pai_homo_mut_abort1)
            print('FVL Hetero and PROTHR Homo, PAI Homo Mutations 2 more Aborts are:',
                  cnt_fvl_hetero_pr_homo_pai_homo_mut_aborts)

            context3['cnt_fvl_hetero_pr_homo_pai_homo_mutations'] = cnt_fvl_hetero_pr_homo_pai_homo_mutations
            context3['cnt_fvl_hetero_pr_homo_pai_homo_mut_abort1'] = cnt_fvl_hetero_pr_homo_pai_homo_mut_abort1
            context3['cnt_fvl_hetero_pr_homo_pai_homo_mut_aborts'] = cnt_fvl_hetero_pr_homo_pai_homo_mut_aborts

            ######################################################
            ###    Heterozygous Factor V Leiden Mutation    ######
            ###  Factor II (Prothrombin) Homozygous Mutation   ###
            ###        Factor MTHFR Homozygous Mutation      #####
            ###         3 Mutations 1 Abort                    ###
            ######################################################

            cnt_fvl_hetero_pr_homo_mthfr_homo_mutations = 0
            cnt_fvl_hetero_pr_homo_mthfr_homo_mut_abort1 = 0
            cnt_fvl_hetero_pr_homo_mthfr_homo_mut_aborts = 0

            for fvl_hetero in range(len(list_fvl_hetero)):
                if (
                        list_fvl_hetero[fvl_hetero][0] == '1.0' and
                        list_prothr_homo[fvl_hetero][0] == '1.0' and
                        list_mthfr_homo[fvl_hetero][0] == '1.0'):

                    if list_abort[fvl_hetero][0] == '1.0':
                        cnt_fvl_hetero_pr_homo_mthfr_homo_mut_abort1 = cnt_fvl_hetero_pr_homo_mthfr_homo_mut_abort1 + 1
                    else:
                        cnt_fvl_hetero_pr_homo_mthfr_homo_mut_aborts = cnt_fvl_hetero_pr_homo_mthfr_homo_mut_aborts + 1
                    cnt_fvl_hetero_pr_homo_mthfr_homo_mutations = cnt_fvl_hetero_pr_homo_mthfr_homo_mutations + 1

            print('All Patients are:', cnt_fvl_hetero_pr_homo_mthfr_homo_mutations)
            print('FVL Hetero, PROTHR Homo, MTHFR Homo Mutations, 1 Abort are:',
                  cnt_fvl_hetero_pr_homo_mthfr_homo_mut_abort1)
            print('FVL Hetero and PROTHR Homo, MTHFR Homo Mutations 2 more Aborts are:',
                  cnt_fvl_hetero_pr_homo_mthfr_homo_mut_aborts)

            context3['cnt_fvl_hetero_pr_homo_mthfr_homo_mutations'] = cnt_fvl_hetero_pr_homo_mthfr_homo_mutations
            context3['cnt_fvl_hetero_pr_homo_mthfr_homo_mut_abort1'] = cnt_fvl_hetero_pr_homo_mthfr_homo_mut_abort1
            context3['cnt_fvl_hetero_pr_homo_mthfr_homo_mut_aborts'] = cnt_fvl_hetero_pr_homo_mthfr_homo_mut_aborts

            ######################################################
            ###    Homoozygous Factor V Leiden Mutation     ######
            ###  Factor II (Prothrombin) Heterozygous Mutation ###
            ###        Factor PAI I Homozygous Mutation      #####
            ###         3 Mutations 1 Abort                    ###
            ######################################################

            cnt_fvl_homo_pr_hetero_pai_homo_mutations = 0
            cnt_fvl_homo_pr_hetero_pai_homo_mut_abort1 = 0
            cnt_fvl_homo_pr_hetero_pai_homo_mut_aborts = 0

            for fvl_homo in range(len(list_fvl_homo)):
                if (
                        list_fvl_homo[fvl_homo][0] == '1.0' and
                        list_prothr_hetero[fvl_homo][0] == '1.0' and
                        list_pai_homo[fvl_hetero][0] == '1.0'):

                    if list_abort[fvl_homo][0] == '1.0':
                        cnt_fvl_homo_pr_hetero_pai_homo_mut_abort1 = cnt_fvl_homo_pr_hetero_pai_homo_mut_abort1 + 1
                    else:
                        cnt_fvl_homo_pr_hetero_pai_homo_mut_aborts = cnt_fvl_homo_pr_hetero_pai_homo_mut_aborts + 1
                    cnt_fvl_homo_pr_hetero_pai_homo_mutations = cnt_fvl_homo_pr_hetero_pai_homo_mutations + 1

            print('All Patients are:', cnt_fvl_homo_pr_hetero_pai_homo_mutations)
            print('FVL Hetero, PROTHR Hetero, PAI Homo Mutations, 1 Abort are:',
                  cnt_fvl_hetero_pr_homo_mthfr_homo_mut_abort1)
            print('FVL Hetero and PROTHR Hetero, PAI Homo Mutations 2 more Aborts are:',
                  cnt_fvl_homo_pr_hetero_pai_homo_mut_aborts)

            context3['cnt_fvl_homo_pr_hetero_pai_homo_mutations'] = cnt_fvl_homo_pr_hetero_pai_homo_mutations
            context3['cnt_fvl_homo_pr_hetero_pai_homo_mut_abort1'] = cnt_fvl_homo_pr_hetero_pai_homo_mut_abort1
            context3['cnt_fvl_homo_pr_hetero_pai_homo_mut_aborts'] = cnt_fvl_homo_pr_hetero_pai_homo_mut_aborts

            ######################################################
            ###    Homoozygous Factor V Leiden Mutation     ######
            ###  Factor II (Prothrombin) Heterozygous Mutation ###
            ###        Factor MTHFR Homozygous Mutation      #####
            ###         3 Mutations 1 Abort                    ###
            ######################################################

            cnt_fvl_homo_pr_hetero_mthfr_homo_mutations = 0
            cnt_fvl_homo_pr_hetero_mthfr_homo_mut_abort1 = 0
            cnt_fvl_homo_pr_hetero_mthfr_homo_mut_aborts = 0

            for fvl_homo in range(len(list_fvl_homo)):
                if (
                        list_fvl_homo[fvl_homo][0] == '1.0' and
                        list_prothr_hetero[fvl_homo][0] == '1.0' and
                        list_mthfr_homo[fvl_hetero][0] == '1.0'):

                    if list_abort[fvl_homo][0] == '1.0':
                        cnt_fvl_homo_pr_hetero_mthfr_homo_mut_abort1 = cnt_fvl_homo_pr_hetero_mthfr_homo_mut_abort1 + 1
                    else:
                        cnt_fvl_homo_pr_hetero_mthfr_homo_mut_aborts = cnt_fvl_homo_pr_hetero_mthfr_homo_mut_aborts + 1
                    cnt_fvl_homo_pr_hetero_mthfr_homo_mutations = cnt_fvl_homo_pr_hetero_mthfr_homo_mutations + 1

            print('All Patients are:', cnt_fvl_homo_pr_hetero_mthfr_homo_mutations)
            print('FVL Hetero, PROTHR Hetero, MTHFR Homo Mutations, 1 Abort are:',
                  cnt_fvl_homo_pr_hetero_mthfr_homo_mut_abort1)
            print('FVL Hetero and PROTHR Hetero, MTHFR Homo Mutations 2 more Aborts are:',
                  cnt_fvl_homo_pr_hetero_mthfr_homo_mut_aborts)

            context3['cnt_fvl_homo_pr_hetero_mthfr_homo_mutations'] = cnt_fvl_homo_pr_hetero_mthfr_homo_mutations
            context3['cnt_fvl_homo_pr_hetero_mthfr_homo_mut_abort1'] = cnt_fvl_homo_pr_hetero_mthfr_homo_mut_abort1
            context3['cnt_fvl_homo_pr_hetero_mthfr_homo_mut_aborts'] = cnt_fvl_homo_pr_hetero_mthfr_homo_mut_aborts

            ######################################################
            ###    Homoozygous Factor V Leiden Mutation     ######
            ###  Factor II (Prothrombin) Homozygous Mutation   ###
            ###        Factor PAI I Homozygous Mutation      #####
            ###         3 Mutations 1 Abort                    ###
            ######################################################

            cnt_fvl_homo_pr_homo_pai_homo_mutations = 0
            cnt_fvl_homo_pr_homo_pai_homo_mut_abort1 = 0
            cnt_fvl_homo_pr_homo_pai_homo_mut_aborts = 0

            for fvl_homo in range(len(list_fvl_homo)):
                if (
                        list_fvl_homo[fvl_homo][0] == '1.0' and
                        list_prothr_homo[fvl_homo][0] == '1.0' and
                        list_pai_homo[fvl_hetero][0] == '1.0'):

                    if list_abort[fvl_homo][0] == '1.0':
                        cnt_fvl_homo_pr_homo_pai_homo_mut_abort1 = cnt_fvl_homo_pr_homo_pai_homo_mut_abort1 + 1
                    else:
                        cnt_fvl_homo_pr_homo_pai_homo_mut_aborts = cnt_fvl_homo_pr_homo_pai_homo_mut_aborts + 1
                    cnt_fvl_homo_pr_homo_pai_homo_mutations = cnt_fvl_homo_pr_homo_pai_homo_mutations + 1

            print('All Patients are:', cnt_fvl_homo_pr_homo_pai_homo_mutations)
            print('FVL Hetero, PROTHR Homo, PAI Homo Mutations, 1 Abort are:',
                  cnt_fvl_homo_pr_homo_pai_homo_mut_abort1)
            print('FVL Hetero and PROTHR Homo, PAI Homo Mutations 2 more Aborts are:',
                  cnt_fvl_homo_pr_homo_pai_homo_mut_aborts)

            context3['cnt_fvl_homo_pr_homo_pai_homo_mutations'] = cnt_fvl_homo_pr_homo_pai_homo_mutations
            context3['cnt_fvl_homo_pr_homo_pai_homo_mut_abort1'] = cnt_fvl_homo_pr_homo_pai_homo_mut_abort1
            context3['cnt_fvl_homo_pr_homo_pai_homo_mut_aborts'] = cnt_fvl_homo_pr_homo_pai_homo_mut_aborts

            ######################################################
            ###    Homoozygous Factor V Leiden Mutation     ######
            ###  Factor II (Prothrombin) Homozygous Mutation   ###
            ###        Factor MTHFR Homozygous Mutation      #####
            ###         3 Mutations 1 Abort                    ###
            ######################################################

            cnt_fvl_homo_pr_homo_mthfr_homo_mutations = 0
            cnt_fvl_homo_pr_homo_mthfr_homo_mut_abort1 = 0
            cnt_fvl_homo_pr_homo_mthfr_homo_mut_aborts = 0

            for fvl_homo in range(len(list_fvl_homo)):
                if (
                        list_fvl_homo[fvl_homo][0] == '1.0' and
                        list_prothr_homo[fvl_homo][0] == '1.0' and
                        list_mthfr_homo[fvl_hetero][0] == '1.0'):

                    if list_abort[fvl_homo][0] == '1.0':
                        cnt_fvl_homo_pr_homo_mthfr_homo_mut_abort1 = cnt_fvl_homo_pr_homo_mthfr_homo_mut_abort1 + 1
                    else:
                        cnt_fvl_homo_pr_homo_mthfr_homo_mut_aborts = cnt_fvl_homo_pr_homo_mthfr_homo_mut_aborts + 1
                    cnt_fvl_homo_pr_homo_mthfr_homo_mutations = cnt_fvl_homo_pr_homo_mthfr_homo_mutations + 1

            print('All Patients are:', cnt_fvl_homo_pr_homo_mthfr_homo_mutations)
            print('FVL Hetero, PROTHR Homo, MTHFR Homo Mutations, 1 Abort are:',
                  cnt_fvl_homo_pr_homo_mthfr_homo_mut_abort1)
            print('FVL Hetero and PROTHR Homo, MTHFR Homo Mutations 2 more Aborts are:',
                  cnt_fvl_homo_pr_homo_mthfr_homo_mut_aborts)

            context3['cnt_fvl_homo_pr_homo_mthfr_homo_mutations'] = cnt_fvl_homo_pr_homo_mthfr_homo_mutations
            context3['cnt_fvl_homo_pr_homo_mthfr_homo_mut_abort1'] = cnt_fvl_homo_pr_homo_mthfr_homo_mut_abort1
            context3['cnt_fvl_homo_pr_homo_mthfr_homo_mut_aborts'] = cnt_fvl_homo_pr_homo_mthfr_homo_mut_aborts

            #########################################################
            ###    Factor II (Prothrombin) Heterozygous Mutation  ###
            ###            Factor PAI I Homozygous Mutation       ###
            ###            Factor MTHFR Homozygous Mutation       ###
            ###                 3 Mutations 1 Abort               ###
            #########################################################

            cnt_pr_hetero_pai_homo_mthfr_homo_mutations = 0
            cnt_pr_hetero_pai_homo_mthfr_homo_mut_abort1 = 0
            cnt_pr_hetero_pai_homo_mthfr_homo_mut_aborts = 0

            for pr_hetero in range(len(list_prothr_hetero)):
                if (
                        list_prothr_hetero[pr_hetero][0] == '1.0' and
                        list_pai_homo[pr_hetero][0] == '1.0' and
                        list_mthfr_homo[pr_hetero][0] == '1.0'):

                    if list_abort[pr_hetero][0] == '1.0':
                        cnt_pr_hetero_pai_homo_mthfr_homo_mut_abort1 = cnt_pr_hetero_pai_homo_mthfr_homo_mut_abort1 + 1
                    else:
                        cnt_pr_hetero_pai_homo_mthfr_homo_mut_aborts = cnt_pr_hetero_pai_homo_mthfr_homo_mut_aborts + 1
                    cnt_pr_hetero_pai_homo_mthfr_homo_mutations = cnt_pr_hetero_pai_homo_mthfr_homo_mutations + 1

            print('All Patients are:', cnt_pr_hetero_pai_homo_mthfr_homo_mutations)
            print('PROTHR Hetero, PAI Homo, MTHFR Homo Mutations, 1 Abort are:',
                  cnt_pr_hetero_pai_homo_mthfr_homo_mut_abort1)
            print('PROTHR Hetero, PAI Homo, MTHFR Homo Mutations 2 more Aborts are:',
                  cnt_pr_hetero_pai_homo_mthfr_homo_mut_aborts)

            context3['cnt_pr_hetero_pai_homo_mthfr_homo_mutations'] = cnt_pr_hetero_pai_homo_mthfr_homo_mutations
            context3['cnt_pr_hetero_pai_homo_mthfr_homo_mut_abort1'] = cnt_pr_hetero_pai_homo_mthfr_homo_mut_abort1
            context3['cnt_pr_hetero_pai_homo_mthfr_homo_mut_aborts'] = cnt_pr_hetero_pai_homo_mthfr_homo_mut_aborts

            #########################################################
            ###    Factor II (Prothrombin) Homozygous Mutation    ###
            ###            Factor PAI I Homozygous Mutation       ###
            ###            Factor MTHFR Homozygous Mutation       ###
            ###                 3 Mutations 1 Abort               ###
            #########################################################

            cnt_pr_homo_pai_homo_mthfr_homo_mutations = 0
            cnt_pr_homo_pai_homo_mthfr_homo_mut_abort1 = 0
            cnt_pr_homo_pai_homo_mthfr_homo_mut_aborts = 0

            for pr_homo in range(len(list_prothr_homo)):
                if (
                        list_prothr_homo[pr_homo][0] == '1.0' and
                        list_pai_homo[pr_homo][0] == '1.0' and
                        list_mthfr_homo[pr_homo][0] == '1.0'):

                    if list_abort[pr_homo][0] == '1.0':
                        cnt_pr_homo_pai_homo_mthfr_homo_mut_abort1 = cnt_pr_homo_pai_homo_mthfr_homo_mut_abort1 + 1
                    else:
                        cnt_pr_homo_pai_homo_mthfr_homo_mut_aborts = cnt_pr_homo_pai_homo_mthfr_homo_mut_aborts + 1
                    cnt_pr_homo_pai_homo_mthfr_homo_mutations = cnt_pr_homo_pai_homo_mthfr_homo_mutations + 1

            print('All Patients are:', cnt_pr_homo_pai_homo_mthfr_homo_mutations)
            print('PROTHR Homo, PAI Homo, MTHFR Homo Mutations, 1 Abort are:',
                  cnt_pr_homo_pai_homo_mthfr_homo_mut_abort1)
            print('PROTHR Homo, PAI Homo, MTHFR Homo Mutations 2 more Aborts are:',
                  cnt_pr_homo_pai_homo_mthfr_homo_mut_aborts)

            context3['cnt_pr_homo_pai_homo_mthfr_homo_mutations'] = cnt_pr_homo_pai_homo_mthfr_homo_mutations
            context3['cnt_pr_homo_pai_homo_mthfr_homo_mut_abort1'] = cnt_pr_homo_pai_homo_mthfr_homo_mut_abort1
            context3['cnt_pr_homo_pai_homo_mthfr_homo_mut_aborts'] = cnt_pr_homo_pai_homo_mthfr_homo_mut_aborts
            ######################################################
            ### Heterozygous Factor V Leiden               #######
            ###  and Prothr Hetero Mutation                #######
            ######################################################

            # cnt_fvl_hetero_prothr_hetero_mutations = 0
            # cnt_fvl_hetero_prothr_hetero_mut_abort1 = 0
            # cnt_fvl_hetero_prothr_hetero_mut_aborts = 0
            #
            # for fvl_hetero in range(len(list_fvl_hetero)):
            #
            #     if list_fvl_hetero[fvl_hetero][0] == list_prothr_hetero[fvl_hetero][0] == '1.0':
            #         cnt_fvl_hetero_prothr_hetero_mut_abort1 = cnt_fvl_hetero_prothr_hetero_mut_abort1 + 1
            #         cnt_fvl_hetero_prothr_hetero_mut_aborts = cnt_fvl_hetero_prothr_hetero_mut_aborts + 1
            #     cnt_fvl_hetero_prothr_hetero_mutations = cnt_fvl_hetero_prothr_hetero_mutations + 1
            #
            # print('FVL Hetero and PROTHR Hetero Mutations are:', cnt_fvl_hetero_prothr_hetero_mut_abort1)
            # print('FVL Hetero and PROTHR Hetero Mutations are:', cnt_fvl_hetero_prothr_hetero_mutations)
            # print('FVL Hetero and PROTHR Hetero Mutations for Patients with 1 Abort are:')
            # # print(cnt_fvl_hetero_prothr_hetero_mut_abort1)
            #
            # # print('A 2 M1_0', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_hetero)[0])
            # # print('A 2 M1_1', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_hetero)[1])
            # # print('A 2 M1_2', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_hetero)[2])
            #
            # # print('1 A 2 M1 ', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_hetero)[0])
            # context3['cnt_fvl_hetero_pr_hetero_abort_0'] = mutations_2_abort(list_abort,
            #                                                                  list_fvl_hetero,
            #                                                                  list_prothr_hetero)[0]
            #
            # # print('MORE A 2 M1 ', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_hetero)[1])
            # context3['cnt_fvl_hetero_pr_hetero_abort_1'] = mutations_2_abort(list_abort,
            #                                                                  list_fvl_hetero,
            #                                                                  list_prothr_hetero)[1]

            ######################################################
            ### Start Count Heterozygous Factor V       ##########
            ### Leiden and Prothr Homo Mutation         ##########
            ######################################################

            cnt_fvl_hetero_prothr_homo_mutations = 0
            cnt_fvl_hetero_prothr_homo_mut_abort1 = 0
            cnt_fvl_hetero_prothr_homo_mut_aborts = 0

            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts1_2030 = 0
            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts2_2030 = 0
            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts3_2030 = 0

            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts1_3140 = 0
            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts2_3140 = 0
            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts3_3140 = 0

            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts1_4150 = 0
            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts2_4150 = 0
            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts3_4150 = 0

            cnt_age1_fvl_hetero_prothr_homo_mut_aborts1_2030 = 0
            cnt_age1_fvl_hetero_prothr_homo_mut_aborts2_2030 = 0
            cnt_age1_fvl_hetero_prothr_homo_mut_aborts3_2030 = 0

            cnt_age1_fvl_hetero_prothr_homo_mut_aborts1_3140 = 0
            cnt_age1_fvl_hetero_prothr_homo_mut_aborts2_3140 = 0
            cnt_age1_fvl_hetero_prothr_homo_mut_aborts3_3140 = 0

            cnt_age1_fvl_hetero_prothr_homo_mut_aborts1_4150 = 0
            cnt_age1_fvl_hetero_prothr_homo_mut_aborts2_4150 = 0
            cnt_age1_fvl_hetero_prothr_homo_mut_aborts3_4150 = 0

            cnt_age1_fvl_hetero_pai_homo_mut_aborts1_2030 = 0
            cnt_age1_fvl_hetero_pai_homo_mut_aborts2_2030 = 0
            cnt_age1_fvl_hetero_pai_homo_mut_aborts3_2030 = 0

            cnt_age1_fvl_hetero_pai_homo_mut_aborts1_3140 = 0
            cnt_age1_fvl_hetero_pai_homo_mut_aborts2_3140 = 0
            cnt_age1_fvl_hetero_pai_homo_mut_aborts3_3140 = 0

            cnt_age1_fvl_hetero_pai_homo_mut_aborts1_4150 = 0
            cnt_age1_fvl_hetero_pai_homo_mut_aborts2_4150 = 0
            cnt_age1_fvl_hetero_pai_homo_mut_aborts3_4150 = 0

            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts1_2030 = 0
            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts2_2030 = 0
            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts3_2030 = 0

            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts1_3140 = 0
            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts2_3140 = 0
            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts3_3140 = 0

            cnt_age1_fvl_homo_prothr_hetero_mut_aborts1_2030 = 0
            cnt_age1_fvl_homo_prothr_hetero_mut_aborts2_2030 = 0
            cnt_age1_fvl_homo_prothr_hetero_mut_aborts3_2030 = 0

            cnt_age1_fvl_homo_prothr_hetero_mut_aborts1_3140 = 0
            cnt_age1_fvl_homo_prothr_hetero_mut_aborts2_3140 = 0
            cnt_age1_fvl_homo_prothr_hetero_mut_aborts3_3140 = 0

            cnt_age1_fvl_homo_prothr_hetero_mut_aborts1_4150 = 0
            cnt_age1_fvl_homo_prothr_hetero_mut_aborts2_4150 = 0
            cnt_age1_fvl_homo_prothr_hetero_mut_aborts3_4150 = 0

            cnt_age1_fvl_homo_prothr_homo_mut_aborts1_2030 = 0
            cnt_age1_fvl_homo_prothr_homo_mut_aborts2_2030 = 0
            cnt_age1_fvl_homo_prothr_homo_mut_aborts3_2030 = 0

            cnt_age1_fvl_homo_prothr_homo_mut_aborts1_3140 = 0
            cnt_age1_fvl_homo_prothr_homo_mut_aborts2_3140 = 0
            cnt_age1_fvl_homo_prothr_homo_mut_aborts3_3140 = 0

            cnt_age1_fvl_homo_prothr_homo_mut_aborts1_4150 = 0
            cnt_age1_fvl_homo_prothr_homo_mut_aborts2_4150 = 0
            cnt_age1_fvl_homo_prothr_homo_mut_aborts3_4150 = 0

            cnt_age1_fvl_homo_pai_homo_mut_aborts1_2030 = 0
            cnt_age1_fvl_homo_pai_homo_mut_aborts2_2030 = 0
            cnt_age1_fvl_homo_pai_homo_mut_aborts3_2030 = 0

            cnt_age1_fvl_homo_pai_homo_mut_aborts1_3140 = 0
            cnt_age1_fvl_homo_pai_homo_mut_aborts2_3140 = 0
            cnt_age1_fvl_homo_pai_homo_mut_aborts3_3140 = 0

            cnt_age1_fvl_homo_pai_homo_mut_aborts1_4150 = 0
            cnt_age1_fvl_homo_pai_homo_mut_aborts2_4150 = 0
            cnt_age1_fvl_homo_pai_homo_mut_aborts3_4150 = 0

            cnt_age1_fvl_homo_mthfr_homo_mut_aborts1_2030 = 0
            cnt_age1_fvl_homo_mthfr_homo_mut_aborts2_2030 = 0
            cnt_age1_fvl_homo_mthfr_homo_mut_aborts3_2030 = 0

            cnt_age1_fvl_homo_mthfr_homo_mut_aborts1_3140 = 0
            cnt_age1_fvl_homo_mthfr_homo_mut_aborts2_3140 = 0
            cnt_age1_fvl_homo_mthfr_homo_mut_aborts3_3140 = 0

            cnt_age1_fvl_homo_mthfr_homo_mut_aborts1_4150 = 0
            cnt_age1_fvl_homo_mthfr_homo_mut_aborts2_4150 = 0
            cnt_age1_fvl_homo_mthfr_homo_mut_aborts3_4150 = 0

            cnt_age1_prothr_hetero_pai_homo_mut_aborts1_2030 = 0
            cnt_age1_prothr_hetero_pai_homo_mut_aborts2_2030 = 0
            cnt_age1_prothr_hetero_pai_homo_mut_aborts3_2030 = 0

            cnt_age1_prothr_hetero_pai_homo_mut_aborts1_3140 = 0
            cnt_age1_prothr_hetero_pai_homo_mut_aborts2_3140 = 0
            cnt_age1_prothr_hetero_pai_homo_mut_aborts3_3140 = 0

            cnt_age1_prothr_hetero_pai_homo_mut_aborts1_4150 = 0
            cnt_age1_prothr_hetero_pai_homo_mut_aborts2_4150 = 0
            cnt_age1_prothr_hetero_pai_homo_mut_aborts3_4150 = 0

            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1_2030 = 0
            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2_2030 = 0
            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3_2030 = 0

            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1_3140 = 0
            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2_3140 = 0
            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3_3140 = 0

            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1_4150 = 0
            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2_4150 = 0
            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3_4150 = 0

            cnt_age1_pai_homo_mthfr_homo_mut_aborts1_2030 = 0
            cnt_age1_pai_homo_mthfr_homo_mut_aborts2_2030 = 0
            cnt_age1_pai_homo_mthfr_homo_mut_aborts3_2030 = 0

            cnt_age1_pai_homo_mthfr_homo_mut_aborts1_3140 = 0
            cnt_age1_pai_homo_mthfr_homo_mut_aborts2_3140 = 0
            cnt_age1_pai_homo_mthfr_homo_mut_aborts3_3140 = 0

            cnt_age1_pai_homo_mthfr_homo_mut_aborts1_4150 = 0
            cnt_age1_pai_homo_mthfr_homo_mut_aborts2_4150 = 0
            cnt_age1_pai_homo_mthfr_homo_mut_aborts3_4150 = 0

            cnt_age1_fvl_hetero_pai_homo_mut_aborts1 = 0
            cnt_age1_fvl_hetero_pai_homo_mut_aborts2 = 0
            cnt_age1_fvl_hetero_pai_homo_mut_aborts3 = 0

            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts1 = 0
            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts2 = 0
            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts3 = 0

            cnt_age1_fvl_homo_prothr_hetero_mut_aborts1 = 0
            cnt_age1_fvl_homo_prothr_hetero_mut_aborts2 = 0
            cnt_age1_fvl_homo_prothr_hetero_mut_aborts3 = 0

            cnt_age1_fvl_homo_prothr_homo_mut_aborts1 = 0
            cnt_age1_fvl_homo_prothr_homo_mut_aborts2 = 0
            cnt_age1_fvl_homo_prothr_homo_mut_aborts3 = 0

            cnt_age1_fvl_homo_pai_homo_mut_aborts1 = 0
            cnt_age1_fvl_homo_pai_homo_mut_aborts2 = 0
            cnt_age1_fvl_homo_pai_homo_mut_aborts3 = 0

            cnt_age1_fvl_homo_mthfr_homo_mut_aborts1 = 0
            cnt_age1_fvl_homo_mthfr_homo_mut_aborts2 = 0
            cnt_age1_fvl_homo_mthfr_homo_mut_aborts3 = 0

            cnt_age1_prothr_hetero_pai_homo_mut_aborts1 = 0
            cnt_age1_prothr_hetero_pai_homo_mut_aborts2 = 0
            cnt_age1_prothr_hetero_pai_homo_mut_aborts3 = 0

            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1 = 0
            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2 = 0
            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3 = 0

            cnt_age1_prothr_homo_pai_homo_mut_aborts1 = 0
            cnt_age1_prothr_homo_pai_homo_mut_aborts2 = 0
            cnt_age1_prothr_homo_pai_homo_mut_aborts3 = 0

            cnt_age1_prothr_homo_mthfr_homo_mut_aborts1 = 0
            cnt_age1_prothr_homo_mthfr_homo_mut_aborts2 = 0
            cnt_age1_prothr_homo_mthfr_homo_mut_aborts3 = 0

            cnt_age1_pai_homo_mthfr_homo_mut_aborts1 = 0
            cnt_age1_pai_homo_mthfr_homo_mut_aborts2 = 0
            cnt_age1_pai_homo_mthfr_homo_mut_aborts3 = 0

            ##############################################
            ####    FVL Hetero and Prothrombin Hetero ####
            ##############################################
            for fvl_hetero in range(len(list_fvl_hetero)):
                if 20 <= list_age[fvl_hetero][0] <= 30:
                    if list_abort[fvl_hetero][0] == '1.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts1_2030 = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts1_2030 + 1
                    elif list_abort[fvl_hetero][0] == '2.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts2_2030 = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts2_2030 + 1
                    else:
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts3_2030 = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts3_2030 + 1

                elif 31 <= list_age[fvl_hetero][0] <= 40:
                    if list_abort[fvl_hetero][0] == '1.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts1_3140 = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts1_3140 + 1
                    elif list_abort[fvl_hetero][0] == '2.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts2_3140 = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts2_3140 + 1
                    else:
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts3_3140 = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts3_3140 + 1
                elif 41 <= list_age[fvl_hetero][0] <= 50:
                    if list_abort[fvl_hetero][0] == '1.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts1_4150 = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts1_4150 + 1
                    elif list_abort[fvl_hetero][0] == '2.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts2_4150 = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts2_4150 + 1
                    else:
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_hetero_mut_aborts3_4150 = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts3_4150 + 1

            print('AGE 1', cnt_age1_fvl_hetero_prothr_hetero_mut_aborts1_2030,
                  cnt_age1_fvl_hetero_prothr_hetero_mut_aborts2_2030,
                  cnt_age1_fvl_hetero_prothr_hetero_mut_aborts3_2030)
            ############################################
            #####   FVL Hetero and Prothrombin Homo ####
            ############################################
            for fvl_hetero in range(len(list_fvl_hetero)):
                # print('Vlizam1', list_fvl_hetero[fvl_hetero][0],
                #       list_prothr_homo[fvl_hetero][0], list_age[fvl_hetero][0])

                if 20 <= list_age[fvl_hetero][0] <= 30:
                    if list_abort[fvl_hetero][0] == '1.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_homo_mut_aborts1_2030 = cnt_age1_fvl_hetero_prothr_homo_mut_aborts1_2030 + 1
                    elif list_abort[fvl_hetero][0] == '2.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_homo_mut_aborts2_2030 = cnt_age1_fvl_hetero_prothr_homo_mut_aborts2_2030 + 1
                    else:
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_homo_mut_aborts3_2030 = cnt_age1_fvl_hetero_prothr_homo_mut_aborts3_2030 + 1

                elif 31 <= list_age[fvl_hetero][0] <= 40:
                    if list_abort[fvl_hetero][0] == '1.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_homo_mut_aborts1_3140 = cnt_age1_fvl_hetero_prothr_homo_mut_aborts1_3140 + 1
                    elif list_abort[fvl_hetero][0] == '2.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_homo_mut_aborts2_3140 = cnt_age1_fvl_hetero_prothr_homo_mut_aborts2_3140 + 1
                    else:
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_homo_mut_aborts3_3140 = cnt_age1_fvl_hetero_prothr_homo_mut_aborts3_3140 + 1

                    # print('LIST AGE 11', list_age[fvl_hetero][0], list_abort[fvl_hetero][0],
                    #       list_fvl_hetero[fvl_hetero][0])
                elif 41 <= list_age[fvl_hetero][0] <= 50:
                    # print('LIST AGE 11', list_age[fvl_hetero][0], list_abort[fvl_hetero][0], list_prothr_homo[fvl_hetero][0])
                    if list_abort[fvl_hetero][0] == '1.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_homo_mut_aborts1_4150 = cnt_age1_fvl_hetero_prothr_homo_mut_aborts1_4150 + 1
                    elif list_abort[fvl_hetero][0] == '2.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_homo_mut_aborts2_4150 = cnt_age1_fvl_hetero_prothr_homo_mut_aborts2_4150 + 1
                    else:
                        if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_prothr_homo_mut_aborts3_4150 = cnt_age1_fvl_hetero_prothr_homo_mut_aborts3_4150 + 1

            # print('AGE 2', cnt_age1_fvl_hetero_prothr_homo_mut_aborts1,
            #       cnt_age1_fvl_hetero_prothr_homo_mut_aborts2,
            #       cnt_age1_fvl_hetero_prothr_homo_mut_aborts3)

            ############################################
            #####   FVL Hetero and PAI Homo         ####
            ############################################
            # for fvl_hetero in range(0, 110):
            for fvl_hetero in range(len(list_fvl_hetero)):
                # print('Vlizam1', list_fvl_hetero[fvl_hetero][0],
                #       list_prothr_homo[fvl_hetero][0], list_age[fvl_hetero][0],
                #       fvl_hetero)

                if 20 <= list_age[fvl_hetero][0] <= 30:
                    if list_abort[fvl_hetero][0] == '1.0':
                        # print('Vlizam1', list_fvl_hetero[fvl_hetero][0],
                        #       list_prothr_homo[fvl_hetero][0], list_age[fvl_hetero][0])
                        if list_fvl_hetero[fvl_hetero][0] == list_pai_homo[fvl_hetero][0] == '1.0':
                            # print('Vlizam-hetero1')
                            cnt_age1_fvl_hetero_pai_homo_mut_aborts1_2030 = cnt_age1_fvl_hetero_pai_homo_mut_aborts1_2030 + 1
                    elif list_abort[fvl_hetero][0] == '2.0':
                        # print('Vlizam2')
                        if list_fvl_hetero[fvl_hetero][0] == list_pai_homo[fvl_hetero][0] == '1.0':
                            # print('Vlizam-hetero2')
                            cnt_age1_fvl_hetero_pai_homo_mut_aborts2_2030 = cnt_age1_fvl_hetero_pai_homo_mut_aborts2_2030 + 1
                    else:
                        # print('Vlizam3')
                        if list_fvl_hetero[fvl_hetero][0] == list_pai_homo[fvl_hetero][0] == '1.0':
                            # print('Vlizam-hetero3')
                            cnt_age1_fvl_hetero_pai_homo_mut_aborts3_2030 = cnt_age1_fvl_hetero_pai_homo_mut_aborts3_2030 + 1

                elif 31 <= list_age[fvl_hetero][0] <= 40:
                    if list_abort[fvl_hetero][0] == '1.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_pai_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_pai_homo_mut_aborts1_3140 = cnt_age1_fvl_hetero_pai_homo_mut_aborts1_3140 + 1
                    elif list_abort[fvl_hetero][0] == '2.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_pai_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_pai_homo_mut_aborts2_3140 = cnt_age1_fvl_hetero_pai_homo_mut_aborts2_3140 + 1
                    else:
                        if list_fvl_hetero[fvl_hetero][0] == list_pai_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_pai_homo_mut_aborts3_3140 = cnt_age1_fvl_hetero_pai_homo_mut_aborts3_3140 + 1

                    # print('LIST AGE 11', list_age[fvl_hetero][0], list_abort[fvl_hetero][0],
                    #       list_fvl_hetero[fvl_hetero][0])
                elif 41 <= list_age[fvl_hetero][0] <= 50:
                    if list_abort[fvl_hetero][0] == '1.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_pai_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_pai_homo_mut_aborts1_4150 = cnt_age1_fvl_hetero_pai_homo_mut_aborts1_4150 + 1
                    elif list_abort[fvl_hetero][0] == '2.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_pai_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_pai_homo_mut_aborts2_4150 = cnt_age1_fvl_hetero_pai_homo_mut_aborts2_4150 + 1
                    else:
                        if list_fvl_hetero[fvl_hetero][0] == list_pai_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_pai_homo_mut_aborts3_4150 = cnt_age1_fvl_hetero_pai_homo_mut_aborts3_4150 + 1

            print('AGE 3', cnt_age1_fvl_hetero_pai_homo_mut_aborts1,
                  cnt_age1_fvl_hetero_pai_homo_mut_aborts2,
                  cnt_age1_fvl_hetero_pai_homo_mut_aborts3)

            ############################################
            #####   FVL Hetero and MTHFR Homo       ####
            ############################################
            for fvl_hetero in range(len(list_fvl_hetero)):

                if 20 <= list_age[fvl_hetero][0] <= 30:
                    if list_abort[fvl_hetero][0] == '1.0':
                        # print('Vlizam1', list_fvl_hetero[fvl_hetero][0],
                        #       list_prothr_homo[fvl_hetero][0], list_age[fvl_hetero][0])
                        if ((list_fvl_hetero[fvl_hetero][0] == list_mthfr_homo[fvl_hetero][0]) and
                                (list_fvl_hetero[fvl_hetero][0] == '1.0')):
                            # print('Vlizam-hetero1')
                            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts1_2030 = cnt_age1_fvl_hetero_mthfr_homo_mut_aborts1_2030 + 1
                    elif list_abort[fvl_hetero][0] == '2.0':
                        # print('Vlizam2')
                        if list_fvl_hetero[fvl_hetero][0] == list_mthfr_homo[fvl_hetero][0] == '1.0':
                            # print('Vlizam-hetero2')
                            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts2_2030 = cnt_age1_fvl_hetero_mthfr_homo_mut_aborts2_2030 + 1
                    else:
                        # print('Vlizam3')
                        if list_fvl_hetero[fvl_hetero][0] == list_mthfr_homo[fvl_hetero][0] == '1.0':
                            # print('Vlizam-hetero3')
                            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts3_2030 = cnt_age1_fvl_hetero_mthfr_homo_mut_aborts3_2030 + 1

                elif 31 <= list_age[fvl_hetero][0] <= 40:
                    if list_abort[fvl_hetero][0] == '1.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_mthfr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts1_3140 = cnt_age1_fvl_hetero_mthfr_homo_mut_aborts1_3140 + 1
                    elif list_abort[fvl_hetero][0] == '2.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_mthfr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts2_3140 = cnt_age1_fvl_hetero_mthfr_homo_mut_aborts2_3140 + 1
                    else:
                        if list_fvl_hetero[fvl_hetero][0] == list_mthfr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts3_3140 = cnt_age1_fvl_hetero_mthfr_homo_mut_aborts3_3140 + 1

                    # print('LIST AGE 11', list_age[fvl_hetero][0], list_abort[fvl_hetero][0],
                    #       list_fvl_hetero[fvl_hetero][0])
                elif 41 <= list_age[fvl_hetero][0] <= 50:
                    # print('LIST AGE 11', list_age[fvl_hetero][0], list_abort[fvl_hetero][0], list_prothr_homo[fvl_hetero][0])
                    if list_abort[fvl_hetero][0] == '1.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_mthfr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts1 = cnt_age1_fvl_hetero_mthfr_homo_mut_aborts1 + 1
                    elif list_abort[fvl_hetero][0] == '2.0':
                        if list_fvl_hetero[fvl_hetero][0] == list_mthfr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts2 = cnt_age1_fvl_hetero_mthfr_homo_mut_aborts2 + 1
                    else:
                        if list_fvl_hetero[fvl_hetero][0] == list_mthfr_homo[fvl_hetero][0] == '1.0':
                            cnt_age1_fvl_hetero_mthfr_homo_mut_aborts3 = cnt_age1_fvl_hetero_mthfr_homo_mut_aborts3 + 1

            print('AGE 4', cnt_age1_fvl_hetero_mthfr_homo_mut_aborts1,
                  cnt_age1_fvl_hetero_mthfr_homo_mut_aborts2,
                  cnt_age1_fvl_hetero_mthfr_homo_mut_aborts3)

            ##############################################
            ####    FVL Homo and Prothrombin Hetero ####
            ##############################################
            for fvl_homo in range(len(list_fvl_homo)):
                if 20 <= list_age[fvl_homo][0] <= 30:
                    if list_abort[fvl_homo][0] == '1.0':
                        if list_fvl_homo[fvl_homo][0] == list_prothr_hetero[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_prothr_hetero_mut_aborts1_2030 = cnt_age1_fvl_homo_prothr_hetero_mut_aborts1_2030 + 1
                    elif list_abort[fvl_homo][0] == '2.0':
                        if list_fvl_homo[fvl_homo][0] == list_prothr_hetero[fvl_homo][0] == '1.0':
                            # print('Vlizam-hetero2')
                            cnt_age1_fvl_homo_prothr_hetero_mut_aborts2_2030 = cnt_age1_fvl_homo_prothr_hetero_mut_aborts2_2030 + 1
                    else:
                        # print('Vlizam3')
                        if list_fvl_homo[fvl_homo][0] == list_prothr_hetero[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_prothr_hetero_mut_aborts3_2030 = cnt_age1_fvl_homo_prothr_hetero_mut_aborts3_2030 + 1

                elif 31 <= list_age[fvl_homo][0] <= 40:
                    if list_abort[fvl_homo][0] == '1.0':
                        if list_fvl_homo[fvl_homo][0] == list_prothr_hetero[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_prothr_hetero_mut_aborts1_3140 = cnt_age1_fvl_homo_prothr_hetero_mut_aborts1_3140 + 1
                    elif list_abort[fvl_homo][0] == '2.0':
                        if list_fvl_hetero[fvl_homo][0] == list_prothr_hetero[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_prothr_hetero_mut_aborts2_3140 = cnt_age1_fvl_homo_prothr_hetero_mut_aborts2_3140 + 1
                    else:
                        if list_fvl_homo[fvl_homo][0] == list_prothr_hetero[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_prothr_hetero_mut_aborts3_3140 = cnt_age1_fvl_homo_prothr_hetero_mut_aborts3_3140 + 1

                elif 41 <= list_age[fvl_homo][0] <= 50:
                    if list_abort[fvl_homo][0] == '1.0':
                        if list_fvl_homo[fvl_homo][0] == list_prothr_hetero[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_prothr_hetero_mut_aborts1_4150 = cnt_age1_fvl_homo_prothr_hetero_mut_aborts1_4150 + 1
                    elif list_abort[fvl_homo][0] == '2.0':
                        if list_fvl_homo[fvl_homo][0] == list_prothr_hetero[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_prothr_hetero_mut_aborts2_4150 = cnt_age1_fvl_homo_prothr_hetero_mut_aborts2_4150 + 1
                    else:
                        if list_fvl_homo[fvl_homo][0] == list_prothr_hetero[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_prothr_hetero_mut_aborts3_4150 = cnt_age1_fvl_homo_prothr_hetero_mut_aborts3_4150 + 1

            print('AGE 5', cnt_age1_fvl_homo_prothr_hetero_mut_aborts1,
                  cnt_age1_fvl_homo_prothr_hetero_mut_aborts2,
                  cnt_age1_fvl_homo_prothr_hetero_mut_aborts3)

            ##############################################
            ####    FVL Homo and Prothrombin Hомo     ####
            ##############################################
            for fvl_homo in range(len(list_fvl_homo)):
                if 20 <= list_age[fvl_homo][0] <= 30:
                    if list_abort[fvl_homo][0] == '1.0':
                        if list_fvl_homo[fvl_homo][0] == list_prothr_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_prothr_homo_mut_aborts1_2030 = cnt_age1_fvl_homo_prothr_homo_mut_aborts1_2030 + 1
                    elif list_abort[fvl_homo][0] == '2.0':
                        if list_fvl_homo[fvl_homo][0] == list_prothr_homo[fvl_homo][0] == '1.0':
                            # print('Vlizam-hetero2')
                            cnt_age1_fvl_homo_prothr_homo_mut_aborts2_2030 = cnt_age1_fvl_homo_prothr_homo_mut_aborts2_2030 + 1
                    else:
                        # print('Vlizam3')
                        if list_fvl_homo[fvl_homo][0] == list_prothr_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_prothr_homo_mut_aborts3_2030 = cnt_age1_fvl_homo_prothr_homo_mut_aborts3_2030 + 1

                elif 31 <= list_age[fvl_homo][0] <= 40:
                    if list_abort[fvl_homo][0] == '1.0':
                        if list_fvl_homo[fvl_homo][0] == list_prothr_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_prothr_homo_mut_aborts1_3140 = cnt_age1_fvl_homo_prothr_homo_mut_aborts1_3140 + 1
                    elif list_abort[fvl_homo][0] == '2.0':
                        if list_fvl_hetero[fvl_homo][0] == list_prothr_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_prothr_homo_mut_aborts2_3140 = cnt_age1_fvl_homo_prothr_homo_mut_aborts2_3140 + 1
                    else:
                        if list_fvl_homo[fvl_homo][0] == list_prothr_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_prothr_homo_mut_aborts3_3140 = cnt_age1_fvl_homo_prothr_homo_mut_aborts3_3140 + 1

                elif 41 <= list_age[fvl_homo][0] <= 50:
                    if list_abort[fvl_homo][0] == '1.0':
                        if list_fvl_homo[fvl_homo][0] == list_prothr_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_prothr_homo_mut_aborts1_4150 = cnt_age1_fvl_homo_prothr_homo_mut_aborts1_4150 + 1
                    elif list_abort[fvl_homo][0] == '2.0':
                        if list_fvl_homo[fvl_homo][0] == list_prothr_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_prothr_homo_mut_aborts2_4150 = cnt_age1_fvl_homo_prothr_homo_mut_aborts2_4150 + 1
                    else:
                        if list_fvl_homo[fvl_homo][0] == list_prothr_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_prothr_homo_mut_aborts3_4150 = cnt_age1_fvl_homo_prothr_homo_mut_aborts3_4150 + 1

            print('AGE 6', cnt_age1_fvl_homo_prothr_homo_mut_aborts1,
                  cnt_age1_fvl_homo_prothr_homo_mut_aborts2,
                  cnt_age1_fvl_homo_prothr_homo_mut_aborts3)

            ##############################################
            ####    FVL Homo and PAI Hомo             ####
            ##############################################
            for fvl_homo in range(len(list_fvl_homo)):
                if 20 <= list_age[fvl_homo][0] <= 30:
                    if list_abort[fvl_homo][0] == '1.0':
                        if list_fvl_homo[fvl_homo][0] == list_pai_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_pai_homo_mut_aborts1_2030 = cnt_age1_fvl_homo_pai_homo_mut_aborts1_2030 + 1
                    elif list_abort[fvl_homo][0] == '2.0':
                        if list_fvl_homo[fvl_homo][0] == list_pai_homo[fvl_homo][0] == '1.0':
                            # print('Vlizam-hetero2')
                            cnt_age1_fvl_homo_pai_homo_mut_aborts2_2030 = cnt_age1_fvl_homo_pai_homo_mut_aborts2_2030 + 1
                    else:
                        # print('Vlizam3')
                        if list_fvl_homo[fvl_homo][0] == list_pai_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_pai_homo_mut_aborts3_2030 = cnt_age1_fvl_homo_pai_homo_mut_aborts3_2030 + 1

                elif 31 <= list_age[fvl_homo][0] <= 40:
                    if list_abort[fvl_homo][0] == '1.0':
                        if list_fvl_homo[fvl_homo][0] == list_pai_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_pai_homo_mut_aborts1_3140 = cnt_age1_fvl_homo_pai_homo_mut_aborts1_3140 + 1
                    elif list_abort[fvl_homo][0] == '2.0':
                        if list_fvl_hetero[fvl_homo][0] == list_pai_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_pai_homo_mut_aborts2_3140 = cnt_age1_fvl_homo_pai_homo_mut_aborts2_3140 + 1
                    else:
                        if list_fvl_homo[fvl_homo][0] == list_pai_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_pai_homo_mut_aborts3_3140 = cnt_age1_fvl_homo_pai_homo_mut_aborts3_3140 + 1

                    # print('LIST AGE 11', list_age[fvl_hetero][0], list_abort[fvl_hetero][0],
                    #       list_fvl_hetero[fvl_hetero][0])
                elif 41 <= list_age[fvl_homo][0] <= 50:
                    # print('LIST AGE 11', list_age[fvl_hetero][0], list_abort[fvl_hetero][0], list_prothr_homo[fvl_hetero][0])
                    if list_abort[fvl_homo][0] == '1.0':
                        if list_fvl_homo[fvl_homo][0] == list_pai_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_pai_homo_mut_aborts1_4150 = cnt_age1_fvl_homo_pai_homo_mut_aborts1_4150 + 1
                    elif list_abort[fvl_homo][0] == '2.0':
                        if list_fvl_homo[fvl_homo][0] == list_pai_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_pai_homo_mut_aborts2_4150 = cnt_age1_fvl_homo_pai_homo_mut_aborts2_4150 + 1
                    else:
                        if list_fvl_homo[fvl_homo][0] == list_pai_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_pai_homo_mut_aborts3_4150 = cnt_age1_fvl_homo_pai_homo_mut_aborts3_4150 + 1

            print('AGE 7', cnt_age1_fvl_homo_pai_homo_mut_aborts1,
                  cnt_age1_fvl_homo_pai_homo_mut_aborts2,
                  cnt_age1_fvl_homo_pai_homo_mut_aborts3)

            ##############################################
            ####    FVL Homo and MTHFR Hомo           ####
            ##############################################
            for fvl_homo in range(len(list_fvl_homo)):
                if 20 <= list_age[fvl_homo][0] <= 30:
                    if list_abort[fvl_homo][0] == '1.0':
                        if list_fvl_homo[fvl_homo][0] == list_mthfr_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_mthfr_homo_mut_aborts1_2030 = cnt_age1_fvl_homo_mthfr_homo_mut_aborts1_2030 + 1
                    elif list_abort[fvl_homo][0] == '2.0':
                        if list_fvl_homo[fvl_homo][0] == list_mthfr_homo[fvl_homo][0] == '1.0':
                            # print('Vlizam-hetero2')
                            cnt_age1_fvl_homo_mthfr_homo_mut_aborts2_2030 = cnt_age1_fvl_homo_mthfr_homo_mut_aborts2_2030 + 1
                    else:
                        # print('Vlizam3')
                        if list_fvl_homo[fvl_homo][0] == list_mthfr_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_mthfr_homo_mut_aborts3_2030 = cnt_age1_fvl_homo_mthfr_homo_mut_aborts3_2030 + 1

                elif 31 <= list_age[fvl_homo][0] <= 40:
                    if list_abort[fvl_homo][0] == '1.0':
                        if list_fvl_homo[fvl_homo][0] == list_mthfr_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_mthfr_homo_mut_aborts1_3140 = cnt_age1_fvl_homo_mthfr_homo_mut_aborts1_3140 + 1
                    elif list_abort[fvl_homo][0] == '2.0':
                        if list_fvl_hetero[fvl_homo][0] == list_mthfr_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_mthfr_homo_mut_aborts2_3140 = cnt_age1_fvl_homo_mthfr_homo_mut_aborts2_3140 + 1
                    else:
                        if list_fvl_homo[fvl_homo][0] == list_mthfr_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_mthfr_homo_mut_aborts3_3140 = cnt_age1_fvl_homo_mthfr_homo_mut_aborts3_3140 + 1

                    # print('LIST AGE 11', list_age[fvl_hetero][0], list_abort[fvl_hetero][0],
                    #       list_fvl_hetero[fvl_hetero][0])
                elif 41 <= list_age[fvl_homo][0] <= 50:
                    # print('LIST AGE 11', list_age[fvl_hetero][0], list_abort[fvl_hetero][0], list_prothr_homo[fvl_hetero][0])
                    if list_abort[fvl_homo][0] == '1.0':
                        if list_fvl_homo[fvl_homo][0] == list_mthfr_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_mthfr_homo_mut_aborts1_4150 = cnt_age1_fvl_homo_mthfr_homo_mut_aborts1_4150 + 1
                    elif list_abort[fvl_homo][0] == '2.0':
                        if list_fvl_homo[fvl_homo][0] == list_mthfr_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_mthfr_homo_mut_aborts2_4150 = cnt_age1_fvl_homo_mthfr_homo_mut_aborts2_4150 + 1
                    else:
                        if list_fvl_homo[fvl_homo][0] == list_mthfr_homo[fvl_homo][0] == '1.0':
                            cnt_age1_fvl_homo_mthfr_homo_mut_aborts3_4150 = cnt_age1_fvl_homo_mthfr_homo_mut_aborts3_4150 + 1

            print('AGE 8', cnt_age1_fvl_homo_mthfr_homo_mut_aborts1,
                  cnt_age1_fvl_homo_mthfr_homo_mut_aborts2,
                  cnt_age1_fvl_homo_mthfr_homo_mut_aborts3)

            ##############################################
            ####    Prothrombin Hetero and PAI Hомo   ####
            ##############################################
            for prothr_hetero in range(len(list_prothr_hetero)):
                if 20 <= list_age[prothr_hetero][0] <= 30:
                    if list_abort[prothr_hetero][0] == '1.0':
                        if list_prothr_hetero[prothr_hetero][0] == list_pai_homo[prothr_hetero][0] == '1.0':
                            cnt_age1_prothr_hetero_pai_homo_mut_aborts1_2030 = cnt_age1_prothr_hetero_pai_homo_mut_aborts1_2030 + 1
                    elif list_abort[prothr_hetero][0] == '2.0':
                        if list_prothr_hetero[prothr_hetero][0] == list_pai_homo[prothr_hetero][0] == '1.0':
                            # print('Vlizam-hetero2')
                            cnt_age1_prothr_hetero_pai_homo_mut_aborts2_2030 = cnt_age1_prothr_hetero_pai_homo_mut_aborts2_2030 + 1
                    else:
                        # print('Vlizam3')
                        if list_prothr_hetero[prothr_hetero][0] == list_pai_homo[prothr_hetero][0] == '1.0':
                            cnt_age1_prothr_hetero_pai_homo_mut_aborts3_2030 = cnt_age1_prothr_hetero_pai_homo_mut_aborts3_2030 + 1

                elif 31 <= list_age[prothr_hetero][0] <= 40:
                    if list_abort[prothr_hetero][0] == '1.0':
                        if list_prothr_hetero[prothr_hetero][0] == list_pai_homo[prothr_hetero][0] == '1.0':
                            cnt_age1_prothr_hetero_pai_homo_mut_aborts1_3140 = cnt_age1_prothr_hetero_pai_homo_mut_aborts1_3140 + 1
                    elif list_abort[prothr_hetero][0] == '2.0':
                        if list_prothr_hetero[prothr_hetero][0] == list_pai_homo[prothr_hetero][0] == '1.0':
                            cnt_age1_prothr_hetero_pai_homo_mut_aborts2_3140 = cnt_age1_prothr_hetero_pai_homo_mut_aborts2_3140 + 1
                    else:
                        if list_prothr_hetero[prothr_hetero][0] == list_pai_homo[prothr_hetero][0] == '1.0':
                            cnt_age1_prothr_hetero_pai_homo_mut_aborts3_3140 = cnt_age1_prothr_hetero_pai_homo_mut_aborts3_3140 + 1

                elif 41 <= list_age[prothr_hetero][0] <= 50:
                    if list_abort[prothr_hetero][0] == '1.0':
                        if list_prothr_homo[prothr_hetero][0] == list_pai_homo[prothr_hetero][0] == '1.0':
                            cnt_age1_prothr_hetero_pai_homo_mut_aborts1_4150 = cnt_age1_prothr_hetero_pai_homo_mut_aborts1_4150 + 1
                    elif list_abort[prothr_hetero][0] == '2.0':
                        if list_prothr_homo[prothr_hetero][0] == list_pai_homo[prothr_hetero][0] == '1.0':
                            cnt_age1_prothr_hetero_pai_homo_mut_aborts2_4150 = cnt_age1_prothr_hetero_pai_homo_mut_aborts2_4150 + 1
                    else:
                        if list_prothr_homo[prothr_hetero][0] == list_pai_homo[prothr_hetero][0] == '1.0':
                            cnt_age1_prothr_hetero_pai_homo_mut_aborts3_4150 = cnt_age1_prothr_hetero_pai_homo_mut_aborts3_4150 + 1

            print('AGE 9', cnt_age1_prothr_hetero_pai_homo_mut_aborts1,
                  cnt_age1_prothr_hetero_pai_homo_mut_aborts2,
                  cnt_age1_prothr_hetero_pai_homo_mut_aborts3)

            ##############################################
            ####    Prothrombin Hetero and MTHFR Hомo ####
            ##############################################
            for prothr_hetero in range(len(list_prothr_hetero)):
                if 20 <= list_age[prothr_hetero][0] <= 30:
                    if list_abort[prothr_hetero][0] == '1.0':
                        if list_prothr_hetero[prothr_hetero][0] == list_mthfr_homo[prothr_hetero][0] == '1.0':
                            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1_2030 = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1_2030 + 1
                    elif list_abort[prothr_hetero][0] == '2.0':
                        if list_prothr_hetero[prothr_hetero][0] == list_mthfr_homo[prothr_hetero][0] == '1.0':
                            # print('Vlizam-hetero2')
                            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2_2030 = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2_2030 + 1
                    else:
                        # print('Vlizam3')
                        if list_prothr_hetero[prothr_hetero][0] == list_mthfr_homo[prothr_hetero][0] == '1.0':
                            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3_2030 = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3_2030 + 1

                elif 31 <= list_age[prothr_hetero][0] <= 40:
                    if list_abort[prothr_hetero][0] == '1.0':
                        if list_prothr_hetero[prothr_hetero][0] == list_mthfr_homo[prothr_hetero][0] == '1.0':
                            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1_3140 = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1_3140 + 1
                    elif list_abort[prothr_hetero][0] == '2.0':
                        if list_prothr_hetero[prothr_hetero][0] == list_mthfr_homo[prothr_hetero][0] == '1.0':
                            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2_3140 = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2_3140 + 1
                    else:
                        if list_prothr_hetero[prothr_hetero][0] == list_mthfr_homo[prothr_hetero][0] == '1.0':
                            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3_3140 = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3_3140 + 1

                elif 41 <= list_age[prothr_hetero][0] <= 50:
                    # print('LIST AGE 11', list_age[fvl_hetero][0], list_abort[fvl_hetero][0], list_prothr_homo[fvl_hetero][0])
                    if list_abort[prothr_hetero][0] == '1.0':
                        if list_prothr_homo[prothr_hetero][0] == list_mthfr_homo[prothr_hetero][0] == '1.0':
                            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1_4150 = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1_4150 + 1
                    elif list_abort[prothr_hetero][0] == '2.0':
                        if list_prothr_homo[prothr_hetero][0] == list_mthfr_homo[prothr_hetero][0] == '1.0':
                            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2_4150 = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2_4150 + 1
                    else:
                        if list_prothr_homo[prothr_hetero][0] == list_mthfr_homo[prothr_hetero][0] == '1.0':
                            cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3_4150 = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3_4150 + 1

            print('AGE 10', cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1,
                  cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2,
                  cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3)

            ##############################################
            ####    Prothrombin Homo and PAI Hомo     ####
            ##############################################
            # for prothr_homo in range(len(list_prothr_homo)):
            #     if 20 <= list_age[prothr_homo][0] <= 30:
            #         if list_abort[prothr_homo][0] == '1.0':
            #             if list_prothr_homo[prothr_homo][0] == list_pai_homo[prothr_homo][0] == '1.0':
            #                 cnt_age1_prothr_homo_pai_homo_mut_aborts1 = cnt_age1_prothr_homo_pai_homo_mut_aborts1 + 1
            #         elif list_abort[prothr_homo][0] == '2.0':
            #             if list_prothr_homo[prothr_homo][0] == list_pai_homo[prothr_homo][0] == '1.0':
            #                 # print('Vlizam-hetero2')
            #                 cnt_age1_prothr_homo_pai_homo_mut_aborts2 = cnt_age1_prothr_homo_pai_homo_mut_aborts2 + 1
            #         else:
            #             # print('Vlizam3')
            #             if list_prothr_homo[prothr_homo][0] == list_pai_homo[prothr_homo][0] == '1.0':
            #                 cnt_age1_prothr_homo_pai_homo_mut_aborts3 = cnt_age1_prothr_homo_pai_homo_mut_aborts3 + 1
            #
            #     elif 40 <= list_age[prothr_homo][0] <= 31:
            #         if list_abort[prothr_homo][0] == '1.0':
            #             if list_prothr_homo[prothr_homo][0] == list_pai_homo[prothr_homo][0] == '1.0':
            #                 cnt_age1_prothr_homo_pai_homo_mut_aborts1 = cnt_age1_prothr_homo_pai_homo_mut_aborts1 + 1
            #         elif list_abort[prothr_homo][0] == '2.0':
            #             if list_prothr_homo[prothr_homo][0] == list_pai_homo[prothr_homo][0] == '1.0':
            #                 cnt_age1_prothr_homo_pai_homo_mut_aborts2 = cnt_age1_prothr_homo_pai_homo_mut_aborts2 + 1
            #         else:
            #             if list_prothr_homo[prothr_homo][0] == list_pai_homo[prothr_homo][0] == '1.0':
            #                 cnt_age1_prothr_homo_pai_homo_mut_aborts3 = cnt_age1_prothr_homo_pai_homo_mut_aborts3 + 1
            #     elif 50 <= list_age[prothr_homo][0] <= 41:
            #         if list_abort[prothr_homo][0] == '1.0':
            #             if list_prothr_homo[prothr_homo][0] == list_pai_homo[prothr_homo][0] == '1.0':
            #                 cnt_age1_prothr_homo_pai_homo_mut_aborts1 = cnt_age1_prothr_homo_pai_homo_mut_aborts1 + 1
            #         elif list_abort[prothr_homo][0] == '2.0':
            #             if list_prothr_homo[prothr_homo][0] == list_pai_homo[prothr_homo][0] == '1.0':
            #                 cnt_age1_prothr_homo_pai_homo_mut_aborts2 = cnt_age1_prothr_homo_pai_homo_mut_aborts2 + 1
            #         else:
            #             if list_prothr_homo[prothr_homo][0] == list_pai_homo[prothr_homo][0] == '1.0':
            #                 cnt_age1_prothr_homo_pai_homo_mut_aborts3 = cnt_age1_prothr_homo_pai_homo_mut_aborts3 + 1
            #
            # print('AGE 11', cnt_age1_prothr_homo_pai_homo_mut_aborts1,
            #       cnt_age1_prothr_homo_pai_homo_mut_aborts2,
            #       cnt_age1_prothr_homo_pai_homo_mut_aborts3)

            ##############################################
            ####    Prothrombin Homo and MTHR Hомo    ####
            ##############################################
            # for prothr_homo in range(len(list_prothr_homo)):
            #     if 20 <= list_age[prothr_homo][0] <= 30:
            #         if list_abort[prothr_homo][0] == '1.0':
            #             if list_prothr_homo[prothr_homo][0] == list_mthfr_homo[prothr_homo][0] == '1.0':
            #                 cnt_age1_prothr_homo_mthfr_homo_mut_aborts1 = cnt_age1_prothr_homo_mthfr_homo_mut_aborts1 + 1
            #         elif list_abort[prothr_homo][0] == '2.0':
            #             if list_prothr_homo[prothr_homo][0] == list_mthfr_homo[prothr_homo][0] == '1.0':
            #                 # print('Vlizam-hetero2')
            #                 cnt_age1_prothr_homo_mthfr_homo_mut_aborts2 = cnt_age1_prothr_homo_mthfr_homo_mut_aborts2 + 1
            #         else:
            #             # print('Vlizam3')
            #             if list_prothr_homo[prothr_homo][0] == list_mthfr_homo[prothr_homo][0] == '1.0':
            #                 cnt_age1_prothr_homo_mthfr_homo_mut_aborts3 = cnt_age1_prothr_homo_mthfr_homo_mut_aborts3 + 1
            #
            #     elif 40 <= list_age[prothr_homo][0] <= 31:
            #         if list_abort[prothr_homo][0] == '1.0':
            #             if list_prothr_homo[prothr_homo][0] == list_mthfr_homo[prothr_homo][0] == '1.0':
            #                 cnt_age1_prothr_homo_mthfr_homo_mut_aborts1 = cnt_age1_prothr_homo_mthfr_homo_mut_aborts1 + 1
            #         elif list_abort[prothr_homo][0] == '2.0':
            #             if list_prothr_homo[prothr_homo][0] == list_mthfr_homo[prothr_homo][0] == '1.0':
            #                 cnt_age1_prothr_homo_mthfr_homo_mut_aborts2 = cnt_age1_prothr_homo_mthfr_homo_mut_aborts2 + 1
            #         else:
            #             if list_prothr_homo[prothr_homo][0] == list_mthfr_homo[prothr_homo][0] == '1.0':
            #                 cnt_age1_prothr_homo_mthfr_homo_mut_aborts3 = cnt_age1_prothr_homo_mthfr_homo_mut_aborts3 + 1
            #     elif 50 <= list_age[prothr_homo][0] <= 41:
            #         if list_abort[prothr_homo][0] == '1.0':
            #             if list_prothr_homo[prothr_homo][0] == list_mthfr_homo[prothr_homo][0] == '1.0':
            #                 cnt_age1_prothr_homo_mthfr_homo_mut_aborts1 = cnt_age1_prothr_homo_mthfr_homo_mut_aborts1 + 1
            #         elif list_abort[prothr_homo][0] == '2.0':
            #             if list_prothr_homo[prothr_homo][0] == list_mthfr_homo[prothr_homo][0] == '1.0':
            #                 cnt_age1_prothr_homo_mthfr_homo_mut_aborts2 = cnt_age1_prothr_homo_mthfr_homo_mut_aborts2 + 1
            #         else:
            #             if list_prothr_homo[prothr_homo][0] == list_mthfr_homo[prothr_homo][0] == '1.0':
            #                 cnt_age1_prothr_homo_mthfr_homo_mut_aborts3 = cnt_age1_prothr_homo_mthfr_homo_mut_aborts3 + 1
            #
            # print('AGE 12', cnt_age1_prothr_homo_mthfr_homo_mut_aborts1,
            #       cnt_age1_prothr_homo_mthfr_homo_mut_aborts2,
            #       cnt_age1_prothr_homo_mthfr_homo_mut_aborts3)

            ##############################################
            ####    PAI Homo and MTHR Hомo            ####
            ##############################################
            for pai_homo in range(len(list_pai_homo)):
                if 20 <= list_age[pai_homo][0] <= 30:
                    if list_abort[pai_homo][0] == '1.0':
                        if list_pai_homo[pai_homo][0] == list_mthfr_homo[pai_homo][0] == '1.0':
                            cnt_age1_pai_homo_mthfr_homo_mut_aborts1_2030 = cnt_age1_pai_homo_mthfr_homo_mut_aborts1_2030 + 1
                    elif list_abort[pai_homo][0] == '2.0':
                        if list_pai_homo[pai_homo][0] == list_mthfr_homo[pai_homo][0] == '1.0':
                            cnt_age1_pai_homo_mthfr_homo_mut_aborts2_2030 = cnt_age1_pai_homo_mthfr_homo_mut_aborts2_2030 + 1
                    else:
                        if list_pai_homo[pai_homo][0] == list_mthfr_homo[pai_homo][0] == '1.0':
                            cnt_age1_pai_homo_mthfr_homo_mut_aborts3_2030 = cnt_age1_pai_homo_mthfr_homo_mut_aborts3_2030 + 1
                elif 31 <= list_age[pai_homo][0] <= 40:
                    if list_abort[pai_homo][0] == '1.0':
                        if list_pai_homo[pai_homo][0] == list_mthfr_homo[pai_homo][0] == '1.0':
                            cnt_age1_pai_homo_mthfr_homo_mut_aborts1_3140 = cnt_age1_pai_homo_mthfr_homo_mut_aborts1_3140 + 1
                    elif list_abort[pai_homo][0] == '2.0':
                        if list_pai_homo[pai_homo][0] == list_mthfr_homo[pai_homo][0] == '1.0':
                            cnt_age1_pai_homo_mthfr_homo_mut_aborts2_3140 = cnt_age1_pai_homo_mthfr_homo_mut_aborts2_3140 + 1
                    else:
                        if list_pai_homo[pai_homo][0] == list_mthfr_homo[pai_homo][0] == '1.0':
                            cnt_age1_pai_homo_mthfr_homo_mut_aborts3_3140 = cnt_age1_pai_homo_mthfr_homo_mut_aborts3_3140 + 1
                elif 41 <= list_age[pai_homo][0] <= 50:
                    if list_abort[pai_homo][0] == '1.0':
                        if list_pai_homo[pai_homo][0] == list_mthfr_homo[pai_homo][0] == '1.0':
                            cnt_age1_pai_homo_mthfr_homo_mut_aborts1_4150 = cnt_age1_pai_homo_mthfr_homo_mut_aborts1_4150 + 1
                    elif list_abort[pai_homo][0] == '2.0':
                        if list_pai_homo[pai_homo][0] == list_mthfr_homo[pai_homo][0] == '1.0':
                            cnt_age1_pai_homo_mthfr_homo_mut_aborts2_4150 = cnt_age1_pai_homo_mthfr_homo_mut_aborts2_4150 + 1
                    else:
                        if list_pai_homo[pai_homo][0] == list_mthfr_homo[pai_homo][0] == '1.0':
                            cnt_age1_pai_homo_mthfr_homo_mut_aborts3_4150 = cnt_age1_pai_homo_mthfr_homo_mut_aborts3_4150 + 1

            print('AGE 11', cnt_age1_pai_homo_mthfr_homo_mut_aborts1,
                  cnt_age1_pai_homo_mthfr_homo_mut_aborts2,
                  cnt_age1_pai_homo_mthfr_homo_mut_aborts3)

            context3['cnt_age1_fvl_hetero_prothr_hetero_mut_aborts1_2030'] = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts1_2030
            context3['cnt_age1_fvl_hetero_prothr_hetero_mut_aborts2_2030'] = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts2_2030
            context3['cnt_age1_fvl_hetero_prothr_hetero_mut_aborts3_2030'] = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts3_2030
            context3['cnt_age1_fvl_hetero_prothr_hetero_mut_aborts1_3140'] = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts1_3140
            context3['cnt_age1_fvl_hetero_prothr_hetero_mut_aborts2_3140'] = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts2_3140
            context3['cnt_age1_fvl_hetero_prothr_hetero_mut_aborts3_3140'] = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts3_3140
            context3['cnt_age1_fvl_hetero_prothr_hetero_mut_aborts1_4150'] = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts1_4150
            context3['cnt_age1_fvl_hetero_prothr_hetero_mut_aborts2_4150'] = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts2_4150
            context3['cnt_age1_fvl_hetero_prothr_hetero_mut_aborts3_4150'] = cnt_age1_fvl_hetero_prothr_hetero_mut_aborts3_4150
            context3['cnt_age1_fvl_hetero_prothr_homo_mut_aborts1_2030'] = cnt_age1_fvl_hetero_prothr_homo_mut_aborts1_2030
            context3['cnt_age1_fvl_hetero_prothr_homo_mut_aborts2_2030'] = cnt_age1_fvl_hetero_prothr_homo_mut_aborts2_2030
            context3['cnt_age1_fvl_hetero_prothr_homo_mut_aborts3_2030'] = cnt_age1_fvl_hetero_prothr_homo_mut_aborts3_2030
            context3['cnt_age1_fvl_hetero_prothr_homo_mut_aborts1_3140'] = cnt_age1_fvl_hetero_prothr_homo_mut_aborts1_3140
            context3['cnt_age1_fvl_hetero_prothr_homo_mut_aborts2_3140'] = cnt_age1_fvl_hetero_prothr_homo_mut_aborts2_3140
            context3['cnt_age1_fvl_hetero_prothr_homo_mut_aborts3_3140'] = cnt_age1_fvl_hetero_prothr_homo_mut_aborts3_3140
            context3['cnt_age1_fvl_hetero_prothr_homo_mut_aborts1_4150'] = cnt_age1_fvl_hetero_prothr_homo_mut_aborts1_4150
            context3['cnt_age1_fvl_hetero_prothr_homo_mut_aborts2_4150'] = cnt_age1_fvl_hetero_prothr_homo_mut_aborts2_4150
            context3['cnt_age1_fvl_hetero_prothr_homo_mut_aborts3_4150'] = cnt_age1_fvl_hetero_prothr_homo_mut_aborts3_4150
            context3['cnt_age1_fvl_hetero_pai_homo_mut_aborts1_2030'] = cnt_age1_fvl_hetero_pai_homo_mut_aborts1_2030
            context3['cnt_age1_fvl_hetero_pai_homo_mut_aborts2_2030'] = cnt_age1_fvl_hetero_pai_homo_mut_aborts2_2030
            context3['cnt_age1_fvl_hetero_pai_homo_mut_aborts3_2030'] = cnt_age1_fvl_hetero_pai_homo_mut_aborts3_2030
            context3['cnt_age1_fvl_hetero_pai_homo_mut_aborts1_3140'] = cnt_age1_fvl_hetero_pai_homo_mut_aborts1_3140
            context3['cnt_age1_fvl_hetero_pai_homo_mut_aborts2_3140'] = cnt_age1_fvl_hetero_pai_homo_mut_aborts2_3140
            context3['cnt_age1_fvl_hetero_pai_homo_mut_aborts3_3140'] = cnt_age1_fvl_hetero_pai_homo_mut_aborts3_3140
            context3['cnt_age1_fvl_hetero_pai_homo_mut_aborts1_4150'] = cnt_age1_fvl_hetero_pai_homo_mut_aborts1_4150
            context3['cnt_age1_fvl_hetero_pai_homo_mut_aborts2_4150'] = cnt_age1_fvl_hetero_pai_homo_mut_aborts2_4150
            context3['cnt_age1_fvl_hetero_pai_homo_mut_aborts3_4150'] = cnt_age1_fvl_hetero_pai_homo_mut_aborts3_4150
            context3['cnt_age1_fvl_hetero_mthfr_homo_mut_aborts1_2030'] = cnt_age1_fvl_hetero_mthfr_homo_mut_aborts1_2030
            context3['cnt_age1_fvl_hetero_mthfr_homo_mut_aborts2_2030'] = cnt_age1_fvl_hetero_mthfr_homo_mut_aborts2_2030
            context3['cnt_age1_fvl_hetero_mthfr_homo_mut_aborts3_2030'] = cnt_age1_fvl_hetero_mthfr_homo_mut_aborts3_2030
            context3['cnt_age1_fvl_hetero_mthfr_homo_mut_aborts1_3140'] = cnt_age1_fvl_hetero_mthfr_homo_mut_aborts1_3140
            context3['cnt_age1_fvl_hetero_mthfr_homo_mut_aborts2_3140'] = cnt_age1_fvl_hetero_mthfr_homo_mut_aborts2_3140
            context3['cnt_age1_fvl_hetero_mthfr_homo_mut_aborts3_3140'] = cnt_age1_fvl_hetero_mthfr_homo_mut_aborts3_3140
            context3['cnt_age1_fvl_homo_prothr_hetero_mut_aborts1_2030'] = cnt_age1_fvl_homo_prothr_hetero_mut_aborts1_2030
            context3['cnt_age1_fvl_homo_prothr_hetero_mut_aborts2_2030'] = cnt_age1_fvl_homo_prothr_hetero_mut_aborts2_2030
            context3['cnt_age1_fvl_homo_prothr_hetero_mut_aborts3_2030'] = cnt_age1_fvl_homo_prothr_hetero_mut_aborts3_2030
            context3['cnt_age1_fvl_homo_prothr_hetero_mut_aborts1_3140'] = cnt_age1_fvl_homo_prothr_hetero_mut_aborts1_3140
            context3['cnt_age1_fvl_homo_prothr_hetero_mut_aborts2_3140'] = cnt_age1_fvl_homo_prothr_hetero_mut_aborts2_3140
            context3['cnt_age1_fvl_homo_prothr_hetero_mut_aborts3_3140'] = cnt_age1_fvl_homo_prothr_hetero_mut_aborts3_3140
            context3['cnt_age1_fvl_homo_prothr_hetero_mut_aborts1_4150'] = cnt_age1_fvl_homo_prothr_hetero_mut_aborts1_4150
            context3['cnt_age1_fvl_homo_prothr_hetero_mut_aborts2_4150'] = cnt_age1_fvl_homo_prothr_hetero_mut_aborts2_4150
            context3['cnt_age1_fvl_homo_prothr_hetero_mut_aborts3_4150'] = cnt_age1_fvl_homo_prothr_hetero_mut_aborts3_4150
            context3['cnt_age1_fvl_homo_prothr_homo_mut_aborts1_2030'] = cnt_age1_fvl_homo_prothr_homo_mut_aborts1_2030
            context3['cnt_age1_fvl_homo_prothr_homo_mut_aborts2_2030'] = cnt_age1_fvl_homo_prothr_homo_mut_aborts2_2030
            context3['cnt_age1_fvl_homo_prothr_homo_mut_aborts3_2030'] = cnt_age1_fvl_homo_prothr_homo_mut_aborts3_2030
            context3['cnt_age1_fvl_homo_prothr_homo_mut_aborts1_3140'] = cnt_age1_fvl_homo_prothr_homo_mut_aborts1_3140
            context3['cnt_age1_fvl_homo_prothr_homo_mut_aborts2_3140'] = cnt_age1_fvl_homo_prothr_homo_mut_aborts2_3140
            context3['cnt_age1_fvl_homo_prothr_homo_mut_aborts3_3140'] = cnt_age1_fvl_homo_prothr_homo_mut_aborts3_3140
            context3['cnt_age1_fvl_homo_prothr_homo_mut_aborts1_4150'] = cnt_age1_fvl_homo_prothr_homo_mut_aborts1_4150
            context3['cnt_age1_fvl_homo_prothr_homo_mut_aborts2_4150'] = cnt_age1_fvl_homo_prothr_homo_mut_aborts2_4150
            context3['cnt_age1_fvl_homo_prothr_homo_mut_aborts3_4150'] = cnt_age1_fvl_homo_prothr_homo_mut_aborts3_4150
            context3['cnt_age1_fvl_homo_pai_homo_mut_aborts1_2030'] = cnt_age1_fvl_homo_pai_homo_mut_aborts1_2030
            context3['cnt_age1_fvl_homo_pai_homo_mut_aborts2_2030'] = cnt_age1_fvl_homo_pai_homo_mut_aborts2_2030
            context3['cnt_age1_fvl_homo_pai_homo_mut_aborts3_2030'] = cnt_age1_fvl_homo_pai_homo_mut_aborts3_2030
            context3['cnt_age1_fvl_homo_pai_homo_mut_aborts1_3140'] = cnt_age1_fvl_homo_pai_homo_mut_aborts1_3140
            context3['cnt_age1_fvl_homo_pai_homo_mut_aborts2_3140'] = cnt_age1_fvl_homo_pai_homo_mut_aborts2_3140
            context3['cnt_age1_fvl_homo_pai_homo_mut_aborts3_3140'] = cnt_age1_fvl_homo_pai_homo_mut_aborts3_3140
            context3['cnt_age1_fvl_homo_pai_homo_mut_aborts1_4150'] = cnt_age1_fvl_homo_pai_homo_mut_aborts1_4150
            context3['cnt_age1_fvl_homo_pai_homo_mut_aborts2_4150'] = cnt_age1_fvl_homo_pai_homo_mut_aborts2_4150
            context3['cnt_age1_fvl_homo_pai_homo_mut_aborts3_4150'] = cnt_age1_fvl_homo_pai_homo_mut_aborts3_4150
            context3['cnt_age1_fvl_homo_mthfr_homo_mut_aborts1_2030'] = cnt_age1_fvl_homo_mthfr_homo_mut_aborts1_2030
            context3['cnt_age1_fvl_homo_mthfr_homo_mut_aborts2_2030'] = cnt_age1_fvl_homo_mthfr_homo_mut_aborts2_2030
            context3['cnt_age1_fvl_homo_mthfr_homo_mut_aborts3_2030'] = cnt_age1_fvl_homo_mthfr_homo_mut_aborts3_2030
            context3['cnt_age1_fvl_homo_mthfr_homo_mut_aborts1_3140'] = cnt_age1_fvl_homo_mthfr_homo_mut_aborts1_3140
            context3['cnt_age1_fvl_homo_mthfr_homo_mut_aborts2_3140'] = cnt_age1_fvl_homo_mthfr_homo_mut_aborts2_3140
            context3['cnt_age1_fvl_homo_mthfr_homo_mut_aborts3_3140'] = cnt_age1_fvl_homo_mthfr_homo_mut_aborts3_3140
            context3['cnt_age1_fvl_homo_mthfr_homo_mut_aborts1_4150'] = cnt_age1_fvl_homo_mthfr_homo_mut_aborts1_4150
            context3['cnt_age1_fvl_homo_mthfr_homo_mut_aborts2_4150'] = cnt_age1_fvl_homo_mthfr_homo_mut_aborts2_4150
            context3['cnt_age1_fvl_homo_mthfr_homo_mut_aborts3_4150'] = cnt_age1_fvl_homo_mthfr_homo_mut_aborts3_4150
            context3['cnt_age1_prothr_hetero_pai_homo_mut_aborts1_2030'] = cnt_age1_prothr_hetero_pai_homo_mut_aborts1_2030
            context3['cnt_age1_prothr_hetero_pai_homo_mut_aborts2_2030'] = cnt_age1_prothr_hetero_pai_homo_mut_aborts2_2030
            context3['cnt_age1_prothr_hetero_pai_homo_mut_aborts3_2030'] = cnt_age1_prothr_hetero_pai_homo_mut_aborts3_2030
            context3['cnt_age1_prothr_hetero_pai_homo_mut_aborts1_3140'] = cnt_age1_prothr_hetero_pai_homo_mut_aborts1_3140
            context3['cnt_age1_prothr_hetero_pai_homo_mut_aborts2_3140'] = cnt_age1_prothr_hetero_pai_homo_mut_aborts2_3140
            context3['cnt_age1_prothr_hetero_pai_homo_mut_aborts3_3140'] = cnt_age1_prothr_hetero_pai_homo_mut_aborts3_3140
            context3['cnt_age1_prothr_hetero_pai_homo_mut_aborts1_4150'] = cnt_age1_prothr_hetero_pai_homo_mut_aborts1_4150
            context3['cnt_age1_prothr_hetero_pai_homo_mut_aborts2_4150'] = cnt_age1_prothr_hetero_pai_homo_mut_aborts2_4150
            context3['cnt_age1_prothr_hetero_pai_homo_mut_aborts3_4150'] = cnt_age1_prothr_hetero_pai_homo_mut_aborts3_4150
            context3['cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1_2030'] = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1_2030
            context3['cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2_2030'] = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2_2030
            context3['cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3_2030'] = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3_2030
            context3['cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1_3140'] = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1_3140
            context3['cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2_3140'] = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2_3140
            context3['cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3_3140'] = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3_3140
            context3['cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1_4150'] = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts1_4150
            context3['cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2_4150'] = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts2_4150
            context3['cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3_4150'] = cnt_age1_prothr_hetero_mthfr_homo_mut_aborts3_4150
            context3['cnt_age1_pai_homo_mthfr_homo_mut_aborts1_2030'] = cnt_age1_pai_homo_mthfr_homo_mut_aborts1_2030
            context3['cnt_age1_pai_homo_mthfr_homo_mut_aborts2_2030'] = cnt_age1_pai_homo_mthfr_homo_mut_aborts2_2030
            context3['cnt_age1_pai_homo_mthfr_homo_mut_aborts3_2030'] = cnt_age1_pai_homo_mthfr_homo_mut_aborts3_2030
            context3['cnt_age1_pai_homo_mthfr_homo_mut_aborts1_3140'] = cnt_age1_pai_homo_mthfr_homo_mut_aborts1_3140
            context3['cnt_age1_pai_homo_mthfr_homo_mut_aborts2_3140'] = cnt_age1_pai_homo_mthfr_homo_mut_aborts2_3140
            context3['cnt_age1_pai_homo_mthfr_homo_mut_aborts3_3140'] = cnt_age1_pai_homo_mthfr_homo_mut_aborts3_3140
            context3['cnt_age1_pai_homo_mthfr_homo_mut_aborts1_4150'] = cnt_age1_pai_homo_mthfr_homo_mut_aborts1_4150
            context3['cnt_age1_pai_homo_mthfr_homo_mut_aborts2_4150'] = cnt_age1_pai_homo_mthfr_homo_mut_aborts2_4150
            context3['cnt_age1_pai_homo_mthfr_homo_mut_aborts3_4150'] = cnt_age1_pai_homo_mthfr_homo_mut_aborts3_4150

            ######################################################
            ### Heterozygous Factor V Leiden               #######
            ###  and Prothr Hetero Mutation                #######
            ######################################################

            cnt_fvl_hetero_prothr_hetero_mutations = 0
            cnt_fvl_hetero_prothr_hetero_mut_abort1 = 0
            cnt_fvl_hetero_prothr_hetero_mut_aborts = 0

            for fvl_hetero in range(len(list_fvl_hetero)):

                if list_fvl_hetero[fvl_hetero][0] == list_prothr_hetero[fvl_hetero][0] == '1.0':
                    cnt_fvl_hetero_prothr_hetero_mut_abort1 = cnt_fvl_hetero_prothr_hetero_mut_abort1 + 1
                    cnt_fvl_hetero_prothr_hetero_mut_aborts = cnt_fvl_hetero_prothr_hetero_mut_aborts + 1
                cnt_fvl_hetero_prothr_hetero_mutations = cnt_fvl_hetero_prothr_hetero_mutations + 1

            print('FVL Hetero and PROTHR Hetero Mutations are:', cnt_fvl_hetero_prothr_hetero_mut_abort1)
            print('FVL Hetero and PROTHR Hetero Mutations are:', cnt_fvl_hetero_prothr_hetero_mutations)
            print('FVL Hetero and PROTHR Hetero Mutations for Patients with 1 Abort are:')

            ######################################################
            ### Heterozygous Factor V Leiden            ##########
            ### and PROTHROMBIN Homo Mutation           ##########
            ######################################################

            cnt_fvl_hetero_prothr_homo_mutations = 0
            cnt_fvl_hetero_prothr_homo_mut_abort1 = 0
            cnt_fvl_hetero_prothr_homo_mut_aborts = 0

            for fvl_hetero in range(len(list_fvl_hetero)):
                if list_fvl_hetero[fvl_hetero][0] == list_prothr_homo[fvl_hetero][0] == '1.0':
                    cnt_fvl_hetero_prothr_homo_mut_abort1 = cnt_fvl_hetero_prothr_homo_mut_abort1 + 1
                    cnt_fvl_hetero_prothr_homo_mut_aborts = cnt_fvl_hetero_prothr_homo_mut_aborts + 1

                cnt_fvl_hetero_prothr_homo_mutations = cnt_fvl_hetero_prothr_homo_mutations + 1

            # print('A 2 M2_0', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_homo)[0])
            # print('A 2 M2_1', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_homo)[1])
            # print('A 2 M2_2', mutations_2_abort(list_abort, list_fvl_hetero, list_prothr_homo)[2])
            ######################################################
            ### Start Count Heterozygous Factor V       ##########
            ### Leiden and PAI I Homo Mutation          ##########
            ######################################################

            cnt_fvl_hetero_pai_homo_mutations = 0
            cnt_fvl_hetero_pai_homo_mut_abort1 = 0
            cnt_fvl_hetero_pai_homo_mut_aborts = 0

            # for fvl_hetero in range(0, 133):

            for fvl_hetero in range(len(list_fvl_hetero)):
                if list_fvl_hetero[fvl_hetero][0] == list_pai_homo[fvl_hetero][0] == '1.0':
                    cnt_fvl_hetero_pai_homo_mut_abort1 = cnt_fvl_hetero_pai_homo_mut_abort1 + 1
                    cnt_fvl_hetero_pai_homo_mut_aborts = cnt_fvl_hetero_pai_homo_mut_aborts + 1
                cnt_fvl_hetero_pai_homo_mutations = cnt_fvl_hetero_pai_homo_mutations + 1

            # print('A 2 M3_0', mutations_2_abort(list_abort, list_fvl_hetero, list_pai_homo)[0])
            # print('A 2 M3_1', mutations_2_abort(list_abort, list_fvl_hetero, list_pai_homo)[1])
            # print('A 2 M3_2', mutations_2_abort(list_abort, list_fvl_hetero, list_pai_homo)[2])

            print('FVL Hetero and PAI I Homo Mutations are:', cnt_fvl_hetero_pai_homo_mut_abort1)
            print('FVL Hetero and PAI I Homo Mutations are:', cnt_fvl_hetero_pai_homo_mut_aborts)

            ######################################################
            ### Start Count Heterozygous Factor V       ##########
            ### Leiden and MTHFR Homo Mutation        ##########
            ######################################################

            cnt_fvl_hetero_mthfr_homo_mutations = 0
            cnt_fvl_hetero_mthfr_homo_mut_abort1 = 0
            cnt_fvl_hetero_mthfr_homo_mut_aborts = 0

            for fvl_hetero in range(len(list_fvl_hetero)):
                if list_fvl_hetero[fvl_hetero][0] == list_mthfr_homo[fvl_hetero][0] == '1.0':
                    cnt_fvl_hetero_mthfr_homo_mut_abort1 = cnt_fvl_hetero_mthfr_homo_mut_abort1 + 1
                    cnt_fvl_hetero_mthfr_homo_mut_aborts = cnt_fvl_hetero_mthfr_homo_mut_aborts + 1
                cnt_fvl_hetero_mthfr_homo_mutations = cnt_fvl_hetero_mthfr_homo_mutations + 1

            # print('A 2 M4_0', mutations_2_abort(list_abort, list_fvl_hetero, list_mthfr_homo)[0])
            # print('A 2 M4_1', mutations_2_abort(list_abort, list_fvl_hetero, list_mthfr_homo)[1])
            # print('A 2 M4_2', mutations_2_abort(list_abort, list_fvl_hetero, list_mthfr_homo)[2])

            print('FVL Hetero and MTHFR Homo Mutations are:', cnt_fvl_hetero_mthfr_homo_mut_abort1)
            print('FVL Hetero and MTHFR Homo Mutations are:', cnt_fvl_hetero_mthfr_homo_mut_aborts)

            # print('FVL Hetero and MTHFR Homo Mutations for Patients with 1 Abort are:')
            # print(cnt_fvl_hetero_mthfr_homo_mut_abort1)

            ######################################################
            ### Start Count Homozygous Factor V         ##########
            ### Leiden and Prothrombin Hetero Mutation  ##########
            ######################################################

            cnt_fvl_homo_prothr_hetero_mutations = 0
            cnt_fvl_homo_prothr_hetero_mut_abort1 = 0
            cnt_fvl_homo_prothr_hetero_mut_aborts = 0

            for fvl_homo in range(len(list_fvl_homo)):
                if list_fvl_homo[fvl_homo][0] == list_prothr_hetero[fvl_homo][0] == '1.0':
                    cnt_fvl_homo_prothr_hetero_mut_abort1 = cnt_fvl_homo_prothr_hetero_mut_abort1 + 1
                    cnt_fvl_homo_prothr_hetero_mut_aborts = cnt_fvl_homo_prothr_hetero_mut_aborts + 1
                cnt_fvl_homo_prothr_hetero_mutations = cnt_fvl_homo_prothr_hetero_mutations + 1

            # print('A 2 M5_0', mutations_2_abort(list_abort, list_fvl_homo, list_prothr_hetero)[0])
            # print('A 2 M5_1', mutations_2_abort(list_abort, list_fvl_homo, list_prothr_hetero)[1])
            # print('A 2 M5_2', mutations_2_abort(list_abort, list_fvl_homo, list_prothr_hetero)[2])

            print('FVL Homo and Prothr Hetero Mutations are:', cnt_fvl_homo_prothr_hetero_mut_abort1)
            print('FVL Homo and Prothr Hetero Mutations are:', cnt_fvl_homo_prothr_hetero_mut_aborts)

            # print('FVL Homo and Prothr Hetero Mutations for Patients with 1 Abort are:')
            # print(cnt_fvl_homo_prothr_hetero_mut_abort1)

            ######################################################
            ### Start Count Homozygous Factor V         ##########
            ### Leiden and Prothrombin Homo Mutation    ##########
            ######################################################

            cnt_fvl_homo_prothr_homo_mutations = 0
            cnt_fvl_homo_prothr_homo_mut_abort1 = 0
            cnt_fvl_homo_prothr_homo_mut_aborts = 0

            for fvl_homo in range(len(list_fvl_homo)):
                if list_fvl_homo[fvl_homo][0] == list_prothr_homo[fvl_homo][0] == '1.0':
                    cnt_fvl_homo_prothr_homo_mut_abort1 = cnt_fvl_homo_prothr_homo_mut_abort1 + 1
                    cnt_fvl_homo_prothr_homo_mut_aborts = cnt_fvl_homo_prothr_homo_mut_aborts + 1
                cnt_fvl_homo_prothr_homo_mutations = cnt_fvl_homo_prothr_homo_mutations + 1

            # print('A 2 M6_0', mutations_2_abort(list_abort, list_fvl_homo, list_prothr_homo)[0])
            # print('A 2 M6_1', mutations_2_abort(list_abort, list_fvl_homo, list_prothr_homo)[1])
            # print('A 2 M6_2', mutations_2_abort(list_abort, list_fvl_homo, list_prothr_homo)[2])

            print('FVL Homo and Prothr Homo Mutations are:', cnt_fvl_homo_prothr_homo_mut_abort1)
            print('FVL Homo and Prothr Homo Mutations are:', cnt_fvl_homo_prothr_homo_mut_aborts)

            # print('FVL Homo and Prothr Homo Mutations for Patients with 1 Abort are:')
            # print(cnt_fvl_homo_prothr_homo_mut_abort1)

            ######################################################
            ### Start Count Homozygous Factor V         ##########
            ### Leiden and PAI I Homo Mutation          ##########
            ######################################################

            cnt_fvl_homo_pai_homo_mutations = 0
            cnt_fvl_homo_pai_homo_mut_abort1 = 0
            cnt_fvl_homo_pai_homo_mut_aborts = 0

            for fvl_homo in range(len(list_fvl_homo)):
                if list_fvl_homo[fvl_homo][0] == list_pai_homo[fvl_homo][0] == '1.0':
                    cnt_fvl_homo_pai_homo_mut_abort1 = cnt_fvl_homo_pai_homo_mut_abort1 + 1
                    cnt_fvl_homo_pai_homo_mut_aborts = cnt_fvl_homo_pai_homo_mut_aborts + 1
                cnt_fvl_homo_pai_homo_mutations = cnt_fvl_homo_pai_homo_mutations + 1

            # print('A 2 M7_0', mutations_2_abort(list_abort, list_fvl_homo, list_pai_homo)[0])
            # print('A 2 M7_1', mutations_2_abort(list_abort, list_fvl_homo, list_pai_homo)[1])
            # print('A 2 M7_2', mutations_2_abort(list_abort, list_fvl_homo, list_pai_homo)[2])

            print('FVL Homo and PAI I Homo Mutations are:', cnt_fvl_homo_pai_homo_mut_abort1)
            print('FVL Homo and PAI I Homo Mutations are:', cnt_fvl_homo_pai_homo_mut_aborts)

            # print('FVL Homo and PAI I Homo Mutations for Patients with 1 Abort are:')
            # print(cnt_fvl_homo_pai_homo_mut_abort1)

            ######################################################
            ### Start Count Homozygous Factor V         ##########
            ### Leiden and MTHFR Homo Mutation          ##########
            ######################################################

            cnt_fvl_homo_mthfr_homo_mutations = 0
            cnt_fvl_homo_mthfr_homo_mut_abort1 = 0
            cnt_fvl_homo_mthfr_homo_mut_aborts = 0

            for fvl_homo in range(len(list_fvl_homo)):
                if list_fvl_homo[fvl_homo][0] == list_mthfr_homo[fvl_homo][0] == '1.0':
                    cnt_fvl_homo_mthfr_homo_mut_abort1 = cnt_fvl_homo_mthfr_homo_mut_abort1 + 1
                    cnt_fvl_homo_mthfr_homo_mut_aborts = cnt_fvl_homo_mthfr_homo_mut_aborts + 1
                cnt_fvl_homo_mthfr_homo_mutations = cnt_fvl_homo_mthfr_homo_mutations + 1

            print('A 2 M8_0', mutations_2_abort(list_abort, list_fvl_homo, list_mthfr_homo)[0])
            print('A 2 M8_1', mutations_2_abort(list_abort, list_fvl_homo, list_mthfr_homo)[1])
            print('A 2 M8_2', mutations_2_abort(list_abort, list_fvl_homo, list_mthfr_homo)[2])

            print('FVL Homo and MTHFR Homo Mutations are:', cnt_fvl_homo_mthfr_homo_mut_abort1)
            print('FVL Homo and MTHFR Homo Mutations are:', cnt_fvl_homo_mthfr_homo_mut_aborts)

            # print('FVL Homo and MTHFR Homo Mutations for Patients with 1 Abort are:')
            # print(cnt_fvl_homo_mthfr_homo_mut_abort1)

            ######################################################
            ### Start Count Heterozygous Prothrombin    ##########
            ### and PAI I Homo Mutation                 ##########
            ######################################################

            cnt_prothr_hetero_pai_homo_mutations = 0
            cnt_prothr_hetero_pai_homo_mut_abort1 = 0
            cnt_prothr_hetero_pai_homo_mut_aborts = 0

            for prothr_hetero in range(len(list_prothr_hetero)):
                if list_prothr_hetero[prothr_hetero][0] == list_pai_homo[prothr_hetero][0] == '1.0':
                    cnt_prothr_hetero_pai_homo_mut_abort1 = cnt_prothr_hetero_pai_homo_mut_abort1 + 1
                    cnt_prothr_hetero_pai_homo_mut_aborts = cnt_prothr_hetero_pai_homo_mut_aborts + 1
                cnt_prothr_hetero_pai_homo_mutations = cnt_prothr_hetero_pai_homo_mutations + 1

            # print('A 2 M9_0', mutations_2_abort(list_abort, list_prothr_hetero, list_pai_homo)[0])
            # print('A 2 M9_1', mutations_2_abort(list_abort, list_prothr_hetero, list_pai_homo)[1])
            # print('A 2 M9_2', mutations_2_abort(list_abort, list_prothr_hetero, list_pai_homo)[2])

            print('Prothrombin Hetero and PAI I Hetero Mutations are:', cnt_prothr_hetero_pai_homo_mut_abort1)
            print('Prothrombin Hetero and PAI I Hetero Mutations are:', cnt_prothr_hetero_pai_homo_mut_aborts)

            # print('Prothrombin Hetero and PAI I Homo Mutations for Patients with 1 Abort are:')
            # print(cnt_prothr_hetero_pai_homo_mut_abort1)

            ######################################################
            ### Start Count Heterozygous Prothrombin    ##########
            ### and MTHFR Homo Mutation                 ##########
            ######################################################

            cnt_prothr_hetero_mthfr_homo_mutations = 0
            cnt_prothr_hetero_mthfr_homo_mut_abort1 = 0
            cnt_prothr_hetero_mthfr_homo_mut_aborts = 0

            for prothr_hetero in range(len(list_prothr_hetero)):
                if list_prothr_hetero[prothr_hetero][0] == list_mthfr_homo[prothr_hetero][0] == '1.0':
                    cnt_prothr_hetero_mthfr_homo_mut_abort1 = cnt_prothr_hetero_mthfr_homo_mut_abort1 + 1
                    cnt_prothr_hetero_mthfr_homo_mut_aborts = cnt_prothr_hetero_mthfr_homo_mut_aborts + 1
                cnt_prothr_hetero_mthfr_homo_mutations = cnt_prothr_hetero_mthfr_homo_mutations + 1

            # print('A 2 M10_0', mutations_2_abort(list_abort, list_prothr_hetero, list_mthfr_homo)[0])
            # print('A 2 M10_1', mutations_2_abort(list_abort, list_prothr_hetero, list_mthfr_homo)[1])
            # print('A 2 M10_2', mutations_2_abort(list_abort, list_prothr_hetero, list_mthfr_homo)[2])

            print('Prothrombin Hetero and MTHFR Homo Mutations are:', cnt_prothr_hetero_mthfr_homo_mut_abort1)
            print('Prothrombin Hetero and MTHFR Homo Mutations are:', cnt_prothr_hetero_mthfr_homo_mut_aborts)

            # print('Prothrombin Hetero and MTHFR Homo Mutations for Patients with 1 Abort are:')
            # print(cnt_prothr_hetero_mthfr_homo_mut_abort1)

            ######################################################
            ### Start Count Homozygous PAI I            ##########
            ### and MTHFR Homo Mutation                 ##########
            ######################################################

            cnt_pai_homo_mthfr_homo_mutations = 0
            cnt_pai_homo_mthfr_homo_mut_abort1 = 0
            cnt_pai_homo_mthfr_homo_mut_aborts = 0

            for pai_homo in range(len(list_pai_homo)):
                if list_pai_homo[pai_homo][0] == list_mthfr_homo[pai_homo][0] == '1.0':
                    cnt_pai_homo_mthfr_homo_mut_abort1 = cnt_pai_homo_mthfr_homo_mut_abort1 + 1
                    cnt_pai_homo_mthfr_homo_mut_aborts = cnt_pai_homo_mthfr_homo_mut_aborts + 1
                cnt_pai_homo_mthfr_homo_mutations = cnt_pai_homo_mthfr_homo_mutations + 1

            # print('A 2 M11_0', mutations_2_abort(list_abort, list_pai_homo, list_mthfr_homo)[0])
            # print('A 2 M11_1', mutations_2_abort(list_abort, list_pai_homo, list_mthfr_homo)[1])
            # print('A 2 M11_2', mutations_2_abort(list_abort, list_pai_homo, list_mthfr_homo)[2])

            print('PAI I Homo and MTHFR Homo Mutations are:', cnt_pai_homo_mthfr_homo_mut_abort1)
            print('PAI I Homo and MTHFR Homo Mutations are:', cnt_pai_homo_mthfr_homo_mut_aborts)

            # print('PAI I Homo and MTHFR Homo Mutations for Patients with 1 Abort are:')
            # print(cnt_pai_homo_mthfr_homo_mut_abort1)

            ######################################################
            ### Start Count Heterozygous Factor V       ##########
            ### Leiden Mutation for 1 Abort             ##########
            ######################################################
            cnt_fvl_hetero_mut_1_abort = 0

            for in_fvl_hetero_abort_1 in range(len(list_abort)):
                if ((list_abort[in_fvl_hetero_abort_1][0] == '1.0') and
                        list_fvl_hetero[in_fvl_hetero_abort_1][0] == '1.0'):
                    cnt_fvl_hetero_mut_1_abort = cnt_fvl_hetero_mut_1_abort + 1
            print('FVL Hetero Mutations for 1 abort:', cnt_fvl_hetero_mut_1_abort)

            ######################################################
            ### Start Count Homozygous Factor V         ##########
            ### Leiden Mutation for 1 Abort             ##########
            ######################################################
            cnt_fvl_homo_mut_1_abort = 0
            for in_fvl_homo_abort_1 in range(len(list_abort)):
                if ((list_abort[in_fvl_homo_abort_1][0] == '1.0') and
                        list_fvl_homo[in_fvl_homo_abort_1][0] == '1.0'):
                    cnt_fvl_homo_mut_1_abort = cnt_fvl_homo_mut_1_abort + 1
            print('FVL Homo Mutations for 1 abort:', cnt_fvl_homo_mut_1_abort)

            ######################################################
            ### Start Count Factor II(Prothrombin)            ####
            ### Heterozygous Mutation for 1 Abort             ####
            ######################################################
            cnt_prothr_hetero_mut_1_abort = 0
            for in_prothr_hetero_abort_1 in range(len(list_abort)):
                if ((list_abort[in_prothr_hetero_abort_1][0] == '1.0') and
                        list_prothr_hetero[in_prothr_hetero_abort_1][0] == '1.0'):
                    cnt_prothr_hetero_mut_1_abort = cnt_prothr_hetero_mut_1_abort + 1
            print('FVL Hetero Mutations for 1 abort:', cnt_prothr_hetero_mut_1_abort)

            ######################################################
            ### Start Count Factor II(Prothrombin)            ####
            ### Homozygous Mutation for 1 Abort               ####
            ######################################################
            cnt_prothr_homo_mut_1_abort = 0
            for in_prothr_homo_abort_1 in range(len(list_abort)):
                if ((list_abort[in_prothr_homo_abort_1][0] == '1.0') and
                        list_prothr_homo[in_prothr_homo_abort_1][0] == '1.0'):
                    cnt_prothr_homo_mut_1_abort = cnt_prothr_homo_mut_1_abort + 1
            print('PROTHR Homo Mutations for 1 abort:', cnt_prothr_homo_mut_1_abort)

            ######################################################
            ### Start Count Factor PAI I Homozigous           ####
            ### Mutation for 1 Abort                          ####
            ######################################################
            cnt_pai_homo_mut_1_abort = 0

            for in_pai_homo_abort_1 in range(len(list_abort)):
                if ((list_abort[in_pai_homo_abort_1][0] == '1.0') and
                        list_pai_homo[in_pai_homo_abort_1][0] == '1.0'):
                    cnt_pai_homo_mut_1_abort = cnt_pai_homo_mut_1_abort + 1
            print('PAI I Homo Mutations for 1 abort:', cnt_pai_homo_mut_1_abort)

            ######################################################
            ### Start Count Factor MTHFR                      ####
            ### Homozygous Mutation for 1 Abort               ####
            ######################################################
            cnt_mthfr_homo_mut_1_abort = 0
            for in_mthfr_homo_abort_1 in range(len(list_abort)):
                if ((list_abort[in_mthfr_homo_abort_1][0] == '1.0') and
                        list_mthfr_homo[in_mthfr_homo_abort_1][0] == '1.0'):
                    cnt_mthfr_homo_mut_1_abort = cnt_mthfr_homo_mut_1_abort + 1
            print('MTHFR Homo Mutations for 1 abort:', cnt_mthfr_homo_mut_1_abort)

            ######################################################
            ### Start Count Count Heterozygous Factor V ##########
            ### Leiden Mutation for 2 or 3 Aborts       ##########
            ###        1 MUTATION FOR 2 OR MORE ABORTS        ####
            ######################################################
            cnt_fvl_hetero_mut_2_3_aborts = 0
            for in_fvl_hetero_aborts_2 in range(len(list_abort)):
                if ((list_abort[in_fvl_hetero_aborts_2][0] == '2.0' or
                     list_abort[in_fvl_hetero_aborts_2][0] == '3.0' or
                     list_abort[in_fvl_hetero_aborts_2][0] == '4.0' or
                     list_abort[in_fvl_hetero_aborts_2][0] == '5.0' or
                     list_abort[in_fvl_hetero_aborts_2][0] == '6.0' or
                     list_abort[in_fvl_hetero_aborts_2][0] == '7.0' or
                     list_abort[in_fvl_hetero_aborts_2][0] == '-' or
                     list_abort[in_fvl_hetero_aborts_2][0] == ''
                ) and
                        list_fvl_hetero[in_fvl_hetero_aborts_2][0] == '1.0'):
                    cnt_fvl_hetero_mut_2_3_aborts = cnt_fvl_hetero_mut_2_3_aborts + 1
            print('FVL Hetero Mutations 2 or more are:', cnt_fvl_hetero_mut_2_3_aborts)

            ######################################################
            ### End Count Count Heterozygous Factor V   ##########
            ### Leiden Mutation for 2 or 3 Aborts       ##########
            ###        1 MUTATION FOR 2 OR MORE ABORTS        ####
            ######################################################

            ######################################################
            ### Start Count Count Homozygous Factor V   ##########
            ### Leiden Mutation for 2 or 3 Aborts       ##########
            ###        1 MUTATION FOR 2 OR MORE ABORTS        ####
            ######################################################
            cnt_fvl_homo_mut_2_3_aborts = 0
            for in_fvl_homo_aborts_2 in range(len(list_abort)):
                if ((list_abort[in_fvl_homo_aborts_2][0] == '2.0' or
                     list_abort[in_fvl_homo_aborts_2][0] == '3.0' or
                     list_abort[in_fvl_homo_aborts_2][0] == '4.0' or
                     list_abort[in_fvl_homo_aborts_2][0] == '5.0' or
                     list_abort[in_fvl_homo_aborts_2][0] == '6.0' or
                     list_abort[in_fvl_homo_aborts_2][0] == '7.0' or
                     list_abort[in_fvl_homo_aborts_2][0] == '-' or
                     list_abort[in_fvl_homo_aborts_2][0] == ''
                ) and
                        list_fvl_homo[in_fvl_homo_aborts_2][0] == '1.0'):
                    cnt_fvl_homo_mut_2_3_aborts = cnt_fvl_homo_mut_2_3_aborts + 1
            print('FVL Homo Mutations 2 or more are:', cnt_fvl_homo_mut_2_3_aborts)

            ######################################################
            ###       Start Count Factor II(Prothrombin)      ####
            ###             Heterozygous Mutation             ####
            ###        1 MUTATION FOR 2 OR MORE ABORTS        ####
            ######################################################
            cnt_prothr_hetero_mut_2_3_aborts = 0
            for in_prothr_hetero_aborts_2 in range(len(list_abort)):
                if ((list_abort[in_prothr_hetero_aborts_2][0] == '2.0' or
                     list_abort[in_prothr_hetero_aborts_2][0] == '3.0' or
                     list_abort[in_prothr_hetero_aborts_2][0] == '4.0' or
                     list_abort[in_prothr_hetero_aborts_2][0] == '5.0' or
                     list_abort[in_prothr_hetero_aborts_2][0] == '6.0' or
                     list_abort[in_prothr_hetero_aborts_2][0] == '7.0' or
                     list_abort[in_prothr_hetero_aborts_2][0] == '-' or
                     list_abort[in_prothr_hetero_aborts_2][0] == ''
                ) and
                        list_prothr_hetero[in_prothr_hetero_aborts_2][0] == '1.0'):
                    cnt_prothr_hetero_mut_2_3_aborts = cnt_prothr_hetero_mut_2_3_aborts + 1
            print('PROTHR Hetero Mutations 2 or more are:', cnt_prothr_hetero_mut_2_3_aborts)
            ######################################################
            ###       Start Count Factor II(Prothrombin)      ####
            ###             Homozygous Mutation               ####
            ###        1 MUTATION FOR 2 OR MORE ABORTS        ####
            ######################################################
            cnt_prothr_homo_mut_2_3_aborts = 0
            for in_prothr_homo_aborts_2 in range(len(list_abort)):
                if ((list_abort[in_prothr_homo_aborts_2][0] == '2.0' or
                     list_abort[in_prothr_homo_aborts_2][0] == '3.0' or
                     list_abort[in_prothr_homo_aborts_2][0] == '4.0' or
                     list_abort[in_prothr_homo_aborts_2][0] == '5.0' or
                     list_abort[in_prothr_homo_aborts_2][0] == '6.0' or
                     list_abort[in_prothr_homo_aborts_2][0] == '7.0' or
                     list_abort[in_prothr_homo_aborts_2][0] == '-' or
                     list_abort[in_prothr_homo_aborts_2][0] == ''
                ) and
                        list_prothr_homo[in_prothr_homo_aborts_2][0] == '1.0'):
                    cnt_prothr_homo_mut_2_3_aborts = cnt_prothr_homo_mut_2_3_aborts + 1
            print('PROTHR Homo Mutations 2 or more are:', cnt_prothr_homo_mut_2_3_aborts)
            ######################################################
            ### Start Count Factor PAI I Homozigous Mutation  ####
            ###        1 MUTATION FOR 2 OR MORE ABORTS        ####
            ######################################################
            cnt_pai_homo_mut_2_3_aborts = 0
            for in_pai_homo_aborts_2 in range(len(list_abort)):
                if ((list_abort[in_pai_homo_aborts_2][0] == '2.0' or
                     list_abort[in_pai_homo_aborts_2][0] == '3.0' or
                     list_abort[in_pai_homo_aborts_2][0] == '4.0' or
                     list_abort[in_pai_homo_aborts_2][0] == '5.0' or
                     list_abort[in_pai_homo_aborts_2][0] == '6.0' or
                     list_abort[in_pai_homo_aborts_2][0] == '7.0' or
                     list_abort[in_pai_homo_aborts_2][0] == '-' or
                     list_abort[in_pai_homo_aborts_2][0] == ''
                ) and
                        list_pai_homo[in_pai_homo_aborts_2][0] == '1.0'):
                    cnt_pai_homo_mut_2_3_aborts = cnt_pai_homo_mut_2_3_aborts + 1
            print('PAI Homo Mutations 2 or more are:', cnt_pai_homo_mut_2_3_aborts)
            ######################################################
            ### Start Count Factor MTHFR Homozigous Mutation  ####
            ###        1 MUTATION FOR 2 OR MORE ABORTS        ####
            ######################################################
            cnt_mthfr_homo_mut_2_3_aborts = 0
            for in_mthfr_homo_aborts_2 in range(len(list_abort)):
                if ((list_abort[in_mthfr_homo_aborts_2][0] == '2.0' or
                     list_abort[in_mthfr_homo_aborts_2][0] == '3.0' or
                     list_abort[in_mthfr_homo_aborts_2][0] == '4.0' or
                     list_abort[in_mthfr_homo_aborts_2][0] == '5.0' or
                     list_abort[in_mthfr_homo_aborts_2][0] == '6.0' or
                     list_abort[in_mthfr_homo_aborts_2][0] == '7.0' or
                     list_abort[in_mthfr_homo_aborts_2][0] == '-' or
                     list_abort[in_mthfr_homo_aborts_2][0] == ''
                ) and
                        list_mthfr_homo[in_mthfr_homo_aborts_2][0] == '1.0'):
                    cnt_mthfr_homo_mut_2_3_aborts = cnt_mthfr_homo_mut_2_3_aborts + 1
            print('MTHFR Homo Mutations 2 or more are:', cnt_mthfr_homo_mut_2_3_aborts)
            ######################################################
            ### Start Count Factor FVL Heterozigous Mutation  ####
            ###                ALL PATIENTS                   ####
            ######################################################
            cnt_fvl_hetero_mutations = 0
            for fvl_hetero_data in list_fvl_hetero:
                if fvl_hetero_data[0] == '1.0':
                    cnt_fvl_hetero_mutations = cnt_fvl_hetero_mutations + 1
            print('FVL Hetero Mutations are:', cnt_fvl_hetero_mutations)
            ######################################################
            ### Start Count Factor FVL Homozygous Mutation    ####
            ###                ALL PATIENTS                   ####
            ######################################################
            cnt_fvl_homo_mutations = 0
            for fvl_homo_data in list_fvl_homo:
                if fvl_homo_data[0] == '1.0':
                    cnt_fvl_homo_mutations = cnt_fvl_homo_mutations + 1
            print('FVL Homo Mutations are:', cnt_fvl_homo_mutations)
            ######################################################
            ###       Start Count Factor II(Prothrombin)      ####
            ###             Heterozygous Mutation             ####
            ###                ALL PATIENTS                   ####
            ######################################################
            cnt_prothr_hetero_mutations = 0
            for prothr_hetero_data in list_prothr_hetero:
                if prothr_hetero_data[0] == '1.0':
                    cnt_prothr_hetero_mutations = cnt_prothr_hetero_mutations + 1
            print('PROTHR Hetero Mutations are:', cnt_prothr_hetero_mutations)
            ######################################################
            ###       Start Count Factor II(Prothrombin)      ####
            ###             Homozygous Mutation               ####
            ###                ALL PATIENTS                   ####
            ######################################################
            cnt_prothr_homo_mutations = 0
            for prothr_homo_data in list_prothr_homo:
                if prothr_homo_data[0] == '1.0':
                    cnt_prothr_homo_mutations = cnt_prothr_homo_mutations + 1
            print('PROTHR Homo Mutations are:', cnt_prothr_homo_mutations)
            ######################################################
            ### Start Count Factor PAI I Homozygous Mutation  ####
            ###                ALL PATIENTS                   ####
            ######################################################
            cnt_pai_homo_mutations = 0
            for pai_homo_data in list_pai_homo:
                if pai_homo_data[0] == '1.0':
                    cnt_pai_homo_mutations = cnt_pai_homo_mutations + 1
            print('PAI Homo Mutations are:', cnt_pai_homo_mutations)
            ######################################################
            ### Start Count Factor MTHFR Homozygous Mutation  ####
            ###                ALL PATIENTS                   ####
            ######################################################
            cnt_mthfr_homo_mutations = 0
            for mthfr_homo_data in list_mthfr_homo:
                if mthfr_homo_data[0] == '1.0':
                    cnt_mthfr_homo_mutations = cnt_mthfr_homo_mutations + 1
            print('MTHFR Homo Mutations are:', cnt_mthfr_homo_mutations)

            context3['fvl_hetero_mut_1_abort'] = cnt_fvl_hetero_mut_1_abort
            context3['fvl_homo_mut_1_abort'] = cnt_fvl_homo_mut_1_abort
            context3['prothr_hetero_mut_1_abort'] = cnt_prothr_hetero_mut_1_abort
            context3['prothr_homo_mut_1_abort'] = cnt_prothr_homo_mut_1_abort
            context3['pai_homo_mut_1_abort'] = cnt_pai_homo_mut_1_abort
            context3['mthfr_homo_mut_1_abort'] = cnt_mthfr_homo_mut_1_abort

            context3['cnt_fvl_hetero_prothr_hetero_mutations'] = cnt_fvl_hetero_prothr_hetero_mutations
            context3['cnt_fvl_hetero_prothr_homo_mutations'] = cnt_fvl_hetero_prothr_homo_mutations
            context3['cnt_fvl_hetero_pai_homo_mutations'] = cnt_fvl_hetero_pai_homo_mutations
            context3['cnt_fvl_hetero_mthfr_homo_mutations'] = cnt_fvl_hetero_mthfr_homo_mutations
            context3['cnt_fvl_homo_prothr_hetero_mutations'] = cnt_fvl_homo_prothr_hetero_mutations
            context3['cnt_fvl_homo_prothr_homo_mutations'] = cnt_fvl_homo_prothr_homo_mutations
            context3['cnt_fvl_homo_pai_homo_mutations'] = cnt_fvl_homo_pai_homo_mutations
            context3['cnt_fvl_homo_mthfr_homo_mutations'] = cnt_fvl_homo_mthfr_homo_mutations
            context3['cnt_prothr_hetero_pai_homo_mutations'] = cnt_prothr_hetero_pai_homo_mutations
            context3['cnt_prothr_hetero_mthfr_homo_mutations'] = cnt_prothr_hetero_mthfr_homo_mutations
            context3['cnt_pai_homo_mthfr_homo_mutations'] = cnt_pai_homo_mthfr_homo_mutations

            context3['cnt_fvl_hetero_prothr_hetero_mut_abort1'] = cnt_fvl_hetero_prothr_hetero_mut_abort1
            context3['cnt_fvl_hetero_prothr_homo_mut_abort1'] = cnt_fvl_hetero_prothr_homo_mut_abort1
            context3['cnt_fvl_hetero_pai_homo_mut_abort1'] = cnt_fvl_hetero_pai_homo_mut_abort1
            context3['cnt_fvl_hetero_mthfr_homo_mut_abort1'] = cnt_fvl_hetero_mthfr_homo_mut_abort1
            context3['cnt_fvl_homo_prothr_hetero_mut_abort1'] = cnt_fvl_homo_prothr_hetero_mut_abort1
            context3['cnt_fvl_homo_prothr_homo_mut_abort1'] = cnt_fvl_homo_prothr_homo_mut_abort1
            context3['cnt_fvl_homo_pai_homo_mut_abort1'] = cnt_fvl_homo_pai_homo_mut_abort1
            context3['cnt_fvl_homo_mthfr_homo_mut_abort1'] = cnt_fvl_homo_mthfr_homo_mut_abort1
            context3['cnt_prothr_hetero_pai_homo_mut_abort1'] = cnt_prothr_hetero_pai_homo_mut_abort1
            context3['cnt_prothr_hetero_mthfr_homo_mut_abort1'] = cnt_prothr_hetero_mthfr_homo_mut_abort1
            context3['cnt_pai_homo_mthfr_homo_mut_abort1'] = cnt_pai_homo_mthfr_homo_mut_abort1

            context3['cnt_fvl_hetero_prothr_hetero_mut_aborts'] = cnt_fvl_hetero_prothr_hetero_mut_aborts
            context3['cnt_fvl_hetero_prothr_homo_mut_aborts'] = cnt_fvl_hetero_prothr_homo_mut_aborts
            context3['cnt_fvl_hetero_pai_homo_mut_aborts'] = cnt_fvl_hetero_pai_homo_mut_aborts
            context3['cnt_fvl_hetero_mthfr_homo_mut_aborts'] = cnt_fvl_hetero_mthfr_homo_mut_aborts
            context3['cnt_fvl_homo_prothr_hetero_mut_aborts'] = cnt_fvl_homo_prothr_hetero_mut_aborts
            context3['cnt_fvl_homo_prothr_homo_mut_aborts'] = cnt_fvl_homo_prothr_homo_mut_aborts
            context3['cnt_fvl_homo_pai_homo_mut_aborts'] = cnt_fvl_homo_pai_homo_mut_aborts
            context3['cnt_fvl_homo_mthfr_homo_mut_aborts'] = cnt_fvl_homo_mthfr_homo_mut_aborts
            context3['cnt_prothr_hetero_pai_homo_mut_aborts'] = cnt_prothr_hetero_pai_homo_mut_aborts
            context3['cnt_prothr_hetero_mthfr_homo_mut_aborts'] = cnt_prothr_hetero_mthfr_homo_mut_aborts
            context3['cnt_pai_homo_mthfr_homo_mut_aborts'] = cnt_pai_homo_mthfr_homo_mut_aborts

            ###        1 MUTATION FOR ALL PATIENTS           ####
            context3['mthfr_homo_mut'] = cnt_mthfr_homo_mutations
            context3['pai_homo_mut'] = cnt_pai_homo_mutations
            context3['prothr_homo_mut'] = cnt_prothr_homo_mutations
            context3['prothr_hetero_mut'] = cnt_prothr_hetero_mutations
            context3['fvl_homo_mut'] = cnt_fvl_homo_mutations
            context3['fvl_hetero_mut'] = cnt_fvl_hetero_mutations
            ###        1 MUTATION FOR 2 OR MORE ABORTS        ####
            context3['2_3_aborts_mthfr_homo_mut'] = cnt_mthfr_homo_mut_2_3_aborts
            context3['2_3_aborts_pai_homo_mut'] = cnt_pai_homo_mut_2_3_aborts
            context3['2_3_aborts_prothr_homo_mut'] = cnt_prothr_homo_mut_2_3_aborts
            context3['2_3_aborts_prothr_hetero_mut'] = cnt_prothr_hetero_mut_2_3_aborts
            context3['2_3_aborts_fvl_homo_mut'] = cnt_fvl_homo_mut_2_3_aborts
            context3['2_3_aborts_fvl_hetero_mut'] = cnt_fvl_hetero_mut_2_3_aborts
            # context3['7_abort_2_mut'] = count_abort7_mutations2
            # context3['6_abort_2_mut'] = count_abort6_mutations2
            # context3['5_abort_2_mut'] = count_abort5_mutations2
            # context3['4_abort_2_mut'] = count_abort4_mutations2
            # context3['3_abort_2_mut'] = count_abort3_mutations2
            # context3['2_abort_2_mut'] = count_abort2_mutations2
            # context3['1_abort_2_mut'] = count_abort1_mutations_2
            # context3['4_aborts_3_mut'] = count_abort4_mutations3
            # context3['3_aborts_3_mut'] = count_abort3_mutations3
            # context3['2_aborts_3_mut'] = count_abort2_mutations3
            # context3['1_abort_3_mut'] = count_abort1_mutations3
    return render(request, 'calc_patients_more_mut_p.html', context3)


def controli(request):
    context3 = {}
    prida_controli = PridaControli.objects.all()
    prida_controli_form = PridaControliForm()

    list_fvl_ng = PridaControli.objects.values_list('fvl_ng')
    list_fvl_hetero = PridaControli.objects.values_list('fvl_hetero')
    list_fvl_homo = PridaControli.objects.values_list('fvl_homo')

    list_prothr_ng = PridaControli.objects.values_list('prothr_ng')
    list_prothr_hetero = PridaControli.objects.values_list('prothr_hetero')
    list_prothr_homo = PridaControli.objects.values_list('prothr_homo')

    list_pai_ng = PridaControli.objects.values_list('pai_ng')
    list_pai_hetero = PridaControli.objects.values_list('pai_hetero')
    list_pai_homo = PridaControli.objects.values_list('pai_homo')

    list_mthfr_ng = PridaControli.objects.values_list('mthfr_ng')
    list_mthfr_hetero = PridaControli.objects.values_list('mthfr_hetero')
    list_mthfr_homo = PridaControli.objects.values_list('mthfr_homo')

    list_age_controli = PridaControli.objects.values_list('age')  ## Promenliva - spisak sas stoinostite na colona "age"
    print('LIST AGE CONTROLI', list_age_controli)
    print('Controli')
    list_abort = PridaControli.objects.values_list('abort')
    prida_age_list_controli = request.POST.getlist('age')  ## Spisak s izbrana ot usera vazrast

    prida_list_data_controli = request.POST.getlist('prida_list_data_controli')
    prida_abort_list_controli = request.POST.getlist('abort')
    end_line_controli = request.POST.get('end_line_controli')
    start_line_controli = request.POST.get('start_line_controli')


    for data in prida_abort_list_controli:
        if data == 'abort_1' or data == 'abort_2' or data == 'abort_3':
            abort = data



        if 'nbr_patients_selected_mutations' in request.POST:
            print('Calculate Mutations Aborts')

            context3['end_line_controli'] = int(end_line_controli)
            context3['start_line_controli'] = int(start_line_controli)
            context3['clients_list_controli'] = int(end_line_controli) - int(start_line_controli)
            clients_list = context3['clients_list_controli']
            sublist = slice(int(start_line_controli), int(end_line_controli))

            sublist_abort = list_abort[sublist]

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

            res_func2 = func2(
                prida_list_data_controli,
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
            # context3['count_mutations_abort1'] = res_func2[0]
            context3['count_mutations'] = res_func2[0]
            # context3['percent_mutations_abort1'] = res_func2[1]
            context3['percent_mutations'] = res_func2[1]
            context3['factor_type'] = prida_list_data_controli
    ######################
    ##  Button Submit  ###
    ######################
    if request.method == 'POST':

        if 'submit' in request.POST:

            context3['end_line_controli'] = int(end_line_controli)
            context3['start_line_controli'] = int(start_line_controli)
            context3['clients_list_controli'] = int(end_line_controli) - int(start_line_controli)
            clients_list_controli = context3['clients_list_controli']

            sublist = slice(int(start_line_controli), int(end_line_controli))

            sublist_age_controli = list_age_controli[sublist]
            print('SUBLIST AGE CONTROLI', sublist_age_controli)

            count_age1 = 0
            count_age2 = 0
            count_age3 = 0

            index_array_age1 = []
            index_array_age2 = []
            index_array_age3 = []

            count_index_array_age = 0

            # for age in sublist_age_controli:
            #     if 20 <= age[0] <= 30:
            #         count_age1 = count_age1 + 1
            #         index_array_age1.append(count_index_array_age)
            #         # print('AGE', age[0])
            #     elif 31 <= age[0] <= 40:
            #         count_age2 = count_age2 + 1
            #         index_array_age2.append(count_index_array_age)
            #         # print('AGE1', age[0])
            #     elif 41 <= age[0] <= 50:
            #         count_age3 = count_age3 + 1
            #         index_array_age3.append(count_index_array_age)
            #     count_index_array_age = count_index_array_age + 1
            # print(index_array_age1, 'OK Age1')
            # print(index_array_age2, 'OK Age2')
            # print(index_array_age3, 'OK Age3')

            sublist_fvl_hetero = list_fvl_hetero[sublist]
            sublist_fvl_homo = list_fvl_homo[sublist]
            sublist_prothr_hetero = list_prothr_hetero[sublist]
            sublist_prothr_homo = list_prothr_homo[sublist]
            sublist_pai_hetero = list_pai_hetero[sublist]
            sublist_pai_homo = list_pai_homo[sublist]
            sublist_mthfr_hetero = list_mthfr_hetero[sublist]
            sublist_mthfr_homo = list_mthfr_homo[sublist]

            count_fvl_hetero = 0
            count_fvl_homo = 0
            count_prothr_hetero = 0
            count_prothr_homo = 0
            count_pai_hetero = 0
            count_pai_homo = 0
            count_mthfr_hetero = 0
            count_mthfr_homo = 0
            ########################################################
            ### Popalvane na tablitzata s kontrolite po tip mutatzii
            ########################################################
            for age_group in prida_age_list_controli:
                if age_group == 'age1':  ### Vazrastova Grupa 1
                    # context3['index_array_age'] = index_array_age1
                    # context3['age_interval'] = age
                    for age in sublist_age_controli:
                        if 20 <= age[0] <= 30:
                            count_age1 = count_age1 + 1
                            index_array_age1.append(count_index_array_age)
                            # print('AGE', age[0], index_array_age1)
                        count_index_array_age = count_index_array_age + 1

                    for factor1 in prida_list_data_controli:
                        if factor1 == 'fvl_hetero':
                            # print('INDEX ARRAY AGE1', index_array_age1)
                            for ind1 in index_array_age1:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_fvl_hetero[ind1][0] == '1.0':
                                    count_fvl_hetero = count_fvl_hetero + 1
                            # print('COUNT FVL HETERO', count_fvl_hetero)
                        elif factor1 == 'fvl_homo':
                            for ind1 in index_array_age1:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_fvl_homo[ind1][0] == '1.0':
                                    count_fvl_homo = count_fvl_homo + 1
                        elif factor1 == 'prothr_hetero':
                            for ind1 in index_array_age1:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_prothr_hetero[ind1][0] == '1.0':
                                    count_prothr_hetero = count_prothr_hetero + 1
                        elif factor1 == 'prothr_homo':
                            for ind1 in index_array_age1:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_prothr_homo[ind1][0] == '1.0':
                                    count_prothr_homo = count_prothr_homo + 1
                        elif factor1 == 'pai_hetero':
                            for ind1 in index_array_age1:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_pai_hetero[ind1][0] == '1.0':
                                    count_pai_hetero = count_pai_hetero + 1
                        elif factor1 == 'pai_homo':
                            for ind1 in index_array_age1:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_pai_homo[ind1][0] == '1.0':
                                    count_pai_homo = count_pai_homo + 1
                        elif factor1 == 'mthfr_hetero':
                            for ind1 in index_array_age1:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_mthfr_hetero[ind1][0] == '1.0':
                                    count_mthfr_hetero = count_mthfr_hetero + 1
                        elif factor1 == 'mthfr_homo':
                            for ind1 in index_array_age1:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_mthfr_homo[ind1][0] == '1.0':
                                    count_mthfr_homo = count_mthfr_homo + 1

                elif age_group == 'age2':  ### Vazrastova Grupa 2
                    count_fvl_hetero = 0
                    count_fvl_homo = 0
                    count_prothr_hetero = 0
                    count_prothr_homo = 0
                    count_pai_hetero = 0
                    count_pai_homo = 0
                    count_mthfr_hetero = 0
                    count_mthfr_homo = 0
                    count_index_array_age = 0
                    # context3['index_array_age'] = index_array_age2
                    # context3['age_interval'] = age_group
                    for age in sublist_age_controli:
                        if 31 <= age[0] <= 40:
                            count_age2 = count_age2 + 1
                            index_array_age2.append(count_index_array_age)
                            # print('AGE2', age[0], index_array_age2)
                        count_index_array_age = count_index_array_age + 1

                    for factor1 in prida_list_data_controli:
                        if factor1 == 'fvl_hetero':
                            # print('INDEX ARRAY AGE2', index_array_age2)
                            for ind2 in index_array_age2:
                                # print('SUBL FVL HETERO2', sublist_fvl_hetero[ind2])
                                if sublist_fvl_hetero[ind2][0] == '1.0':
                                    count_fvl_hetero = count_fvl_hetero + 1
                            # print('COUNT FVL HETERO2', count_fvl_hetero)
                        elif factor1 == 'fvl_homo':
                            for ind1 in index_array_age2:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_fvl_homo[ind1][0] == '1.0':
                                    count_fvl_homo = count_fvl_homo + 1
                        elif factor1 == 'prothr_hetero':
                            for ind1 in index_array_age2:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_prothr_hetero[ind1][0] == '1.0':
                                    count_prothr_hetero = count_prothr_hetero + 1
                        elif factor1 == 'prothr_homo':
                            for ind1 in index_array_age2:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_prothr_homo[ind1][0] == '1.0':
                                    count_prothr_homo = count_prothr_homo + 1
                        elif factor1 == 'pai_hetero':
                            for ind1 in index_array_age2:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_pai_hetero[ind1][0] == '1.0':
                                    count_pai_hetero = count_pai_hetero + 1
                        elif factor1 == 'pai_homo':
                            for ind1 in index_array_age2:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_pai_homo[ind1][0] == '1.0':
                                    count_pai_homo = count_pai_homo + 1
                        elif factor1 == 'mthfr_hetero':
                            for ind1 in index_array_age2:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_mthfr_hetero[ind1][0] == '1.0':
                                    count_mthfr_hetero = count_mthfr_hetero + 1
                        elif factor1 == 'mthfr_homo':
                            for ind1 in index_array_age2:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_mthfr_homo[ind1][0] == '1.0':
                                    count_mthfr_homo = count_mthfr_homo + 1

                elif age_group == 'age3':  ### Vazrastova Grupa 3
                    # count_fvl_hetero = 0
                    # count_fvl_homo = 0
                    # count_prothr_hetero = 0
                    # count_prothr_homo = 0
                    # count_pai_hetero = 0
                    # count_pai_homo = 0
                    # count_mthfr_hetero = 0
                    # count_mthfr_homo = 0
                    # count_index_array_age = 0
                    # context3['index_array_age'] = index_array_age3
                    # context3['age_interval'] = age_group
                    for age in sublist_age_controli:
                        if 41 <= age[0] <= 50:
                            count_age3 = count_age3 + 1
                            index_array_age3.append(count_index_array_age)
                            # print('AGE3', age[0], index_array_age3)
                        count_index_array_age = count_index_array_age + 1

                    for factor1 in prida_list_data_controli:
                        if factor1 == 'fvl_hetero':
                            # print('INDEX ARRAY AGE3', index_array_age3)
                            for ind3 in index_array_age3:
                                # print('SUBL FVL HETERO3', sublist_fvl_hetero[ind3])
                                if sublist_fvl_hetero[ind3][0] == '1.0':
                                    count_fvl_hetero = count_fvl_hetero + 1
                            # print('COUNT FVL HETERO3', count_fvl_hetero)
                        elif factor1 == 'fvl_homo':
                            for ind1 in index_array_age3:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_fvl_homo[ind1][0] == '1.0':
                                    count_fvl_homo = count_fvl_homo + 1
                        elif factor1 == 'prothr_hetero':
                            for ind1 in index_array_age3:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_prothr_hetero[ind1][0] == '1.0':
                                    count_prothr_hetero = count_prothr_hetero + 1
                        elif factor1 == 'prothr_homo':
                            for ind1 in index_array_age3:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_prothr_homo[ind1][0] == '1.0':
                                    count_prothr_homo = count_prothr_homo + 1
                        elif factor1 == 'pai_hetero':
                            for ind1 in index_array_age3:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_pai_hetero[ind1][0] == '1.0':
                                    count_pai_hetero = count_pai_hetero + 1
                        elif factor1 == 'pai_homo':
                            for ind1 in index_array_age3:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_pai_homo[ind1][0] == '1.0':
                                    count_pai_homo = count_pai_homo + 1
                        elif factor1 == 'mthfr_hetero':
                            for ind1 in index_array_age3:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_mthfr_hetero[ind1][0] == '1.0':
                                    count_mthfr_hetero = count_mthfr_hetero + 1
                        elif factor1 == 'mthfr_homo':
                            for ind1 in index_array_age3:
                                # print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
                                if sublist_mthfr_homo[ind1][0] == '1.0':
                                    count_mthfr_homo = count_mthfr_homo + 1

            sublist_fvl_ng = list_fvl_ng[sublist]

            sublist_prothr_ng = list_prothr_ng[sublist]

            sublist_pai_ng = list_pai_ng[sublist]

            sublist_mthfr_ng = list_mthfr_ng[sublist]

            count_fvl_ng = 0

            count_prothr_ng = 0

            count_pai_ng = 0

            count_mthfr_ng = 0
            count_mthfr_hetero = 0
            count_mthfr_homo = 0
            # print(prida_list_data)
            # print(prida_list_data_controli, 'PRIDA LIST')
            # count_fvl_hetero1 = 0
            print('PRIDA LIST DATA CONTROL', prida_list_data_controli)
            # for factor1 in prida_list_data_controli:
            #     pass
            #     # if factor1 == 'fvl_hetero' and context3['index_array_age']==index_array_age1:
            #
            #         # print('INDEX ARRAY AGE1', index_array_age1)
            #         # for ind1 in index_array_age1:
            #         #     print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
            #         #     if sublist_fvl_hetero[ind1][0] == '1.0':
            #         #         count_fvl_hetero = count_fvl_hetero + 1
            #         # print('COUNT FVL HETERO', count_fvl_hetero)
            #         # if factor1 == 'fvl_hetero':
            #         #     print('INDEX ARRAY AGE2', index_array_age2)
            #         #     for ind1 in index_array_age2:
            #         #         print('SUBL FVL HETERO', sublist_fvl_hetero[ind1])
            #         #         if sublist_fvl_hetero[ind1][0] == '1.0':
            #         #             count_fvl_hetero = count_fvl_hetero + 1
            #         #     print('COUNT FVL HETERO', count_fvl_hetero)
            #     if factor1 == 'fvl_homo':
            #         for ind1 in index_array_age1:
            #             print('SUBL FVL HOMO', sublist_fvl_homo[ind1])
            #             if sublist_fvl_homo[ind1][0] == '1.0':
            #                 count_fvl_homo = count_fvl_homo + 1
            #         print('COUNT FVL HOMO', count_fvl_homo)
            #     if factor1 == 'prothr_hetero':
            #         for ind1 in index_array_age1:
            #             print('SUBL PROTHR HETERO', sublist_fvl_hetero[ind1])
            #             if sublist_fvl_hetero[ind1][0] == '1.0':
            #                 count_fvl_hetero = count_fvl_hetero + 1
            #         print('COUNT FVL HETERO', count_fvl_hetero)
            # for f in prida_list_data_controli:
            #     # print(f, 'OK2')
            #     if f == 'fvl_ng':
            #         for fvl_ng in context3['index_array_abort']:
            #             if sublist_fvl_ng[fvl_ng][0] == '1.0':
            #                 count_fvl_ng = count_fvl_ng + 1
            #         print(count_fvl_ng, 'fvl_ng')
            #         if count_fvl_ng > 0:
            #             mutations_age1_abort1_fvl_ng_percent = count_fvl_ng / len(context3['index_array_abort']) * 100
            #             context3['mutations_age1_abort1_fvl_ng_percent'] = mutations_age1_abort1_fvl_ng_percent
            #         else:
            #             context3['mutations_age1_abort1_fvl_ng_percent'] = 0
            #     elif f == 'fvl_hetero':
            #         # print(sublist_fvl_hetero, 'SUBLIST FVL')
            #         for fvl_hetero in range(len(sublist_fvl_hetero)):
            #             if sublist_fvl_hetero[fvl_hetero][0] == '1.0':
            #                 pass
            #                 # count_fvl_hetero = count_fvl_hetero + 1
            #         # print(count_fvl_hetero, 'fvl_hetero')
            #         if count_fvl_hetero > 0:
            #             mutations_age1_abort1_fvl_hetero_percent = count_fvl_hetero / len(
            #                 sublist_fvl_hetero) * 100
            #             context3['mutations_age1_abort1_fvl_hetero_percent'] = mutations_age1_abort1_fvl_hetero_percent
            #         else:
            #             context3['mutations_age1_abort1_fvl_hetero_percent'] = 0
            #     elif f == 'fvl_homo':
            #         for fvl_homo in range(len(sublist_fvl_homo)):
            #             if sublist_fvl_homo[fvl_homo][0] == '1.0':
            #                 count_fvl_homo = count_fvl_homo + 1
            #         # print(count_fvl_homo, 'fvl_homo')
            #         if count_fvl_homo > 0:
            #             mutations_age1_abort1_fvl_homo_percent = count_fvl_homo / len(
            #                 sublist_fvl_homo) * 100
            #             context3['mutations_age1_abort1_fvl_homo_percent'] = mutations_age1_abort1_fvl_homo_percent
            #         else:
            #             context3['mutations_age1_abort1_fvl_homo_percent'] = 0
            #     elif f == 'prothr_ng':
            #         for prothr_ng in range(len(sublist_prothr_ng)):
            #             if sublist_prothr_ng[prothr_ng][0] == '1.0':
            #                 count_prothr_ng = count_prothr_ng + 1
            #         print(count_prothr_ng, 'prothr_ng')
            #         if count_prothr_ng > 0:
            #             mutations_age1_abort1_prothr_ng_percent = count_prothr_ng / len(
            #                 sublist_prothr_ng) * 100
            #             context3['mutations_age1_abort1_prothr_ng_percent'] = mutations_age1_abort1_prothr_ng_percent
            #         else:
            #             context3['mutations_age1_abort1_prothr_ng_percent'] = 0
            #     elif f == 'prothr_hetero':
            #         for prothr_hetero in range(len(sublist_prothr_hetero)):
            #             if sublist_prothr_hetero[prothr_hetero][0] == '1.0':
            #                 count_prothr_hetero = count_prothr_hetero + 1
            #         print(count_prothr_hetero, 'prothr_hetero')
            #         if count_prothr_hetero > 0:
            #             mutations_age1_abort1_prothr_hetero_percent = count_prothr_hetero / len(
            #                 sublist_prothr_hetero) * 100
            #             context3[
            #                 'mutations_age1_abort1_prothr_hetero_percent'] = mutations_age1_abort1_prothr_hetero_percent
            #         else:
            #             context3['mutations_age1_abort1_prothr_hetero_percent'] = 0
            #     elif f == 'prothr_homo':
            #         for prothr_homo in range(len(sublist_prothr_homo)):
            #             if sublist_prothr_homo[prothr_homo][0] == '1.0':
            #                 count_prothr_homo = count_prothr_homo + 1
            #         print(count_prothr_homo, 'prothr_homo')
            #         if count_prothr_homo > 0:
            #             mutations_age1_abort1_prothr_homo_percent = count_prothr_homo / len(
            #                 sublist_prothr_homo) * 100
            #             context3[
            #                 'mutations_age1_abort1_prothr_homo_percent'] = mutations_age1_abort1_prothr_homo_percent
            #         else:
            #             context3['mutations_age1_abort1_prothr_homo_percent'] = 0
            #     elif f == 'pai_ng':
            #         for pai_ng in range(len(sublist_pai_ng)):
            #             if sublist_pai_ng[pai_ng][0] == '1.0':
            #                 count_pai_ng = count_pai_ng + 1
            #         print(count_pai_ng, 'pai_ng')
            #         if count_pai_ng > 0:
            #             mutations_age1_abort1_pai_ng_percent = count_pai_ng / len(
            #                 sublist_pai_ng) * 100
            #             context3['mutations_age1_abort1_pai_ng_percent'] = mutations_age1_abort1_pai_ng_percent
            #         else:
            #             context3['mutations_age1_abort1_pai_ng_percent'] = 0
            #
            #     elif f == 'pai_hetero':
            #         for pai_hetero in range(len(sublist_pai_hetero)):
            #             if sublist_pai_hetero[pai_hetero][0] == '1.0':
            #                 count_pai_hetero = count_pai_hetero + 1
            #         print(count_pai_hetero, 'pai_hetero')
            #         if count_pai_hetero > 0:
            #             mutations_age1_abort1_pai_hetero_percent = count_pai_hetero / len(
            #                 sublist_pai_hetero) * 100
            #             context3['mutations_age1_abort1_pai_hetero_percent'] = mutations_age1_abort1_pai_hetero_percent
            #         else:
            #             context3['mutations_age1_abort1_pai_hetero_percent'] = 0
            #     elif f == 'pai_homo':
            #         for pai_homo in range(len(sublist_pai_homo)):
            #             if sublist_pai_homo[pai_homo][0] == '1.0':
            #                 count_pai_homo = count_pai_homo + 1
            #         print(count_pai_homo, 'pai_homo')
            #         if count_pai_homo > 0:
            #             mutations_age1_abort1_pai_homo_percent = count_pai_homo / len(
            #                 sublist_pai_homo) * 100
            #             context3['mutations_age1_abort1_pai_homo_percent'] = mutations_age1_abort1_pai_homo_percent
            #         else:
            #             context3['mutations_age1_abort1_pai_homo_percent'] = 0
            #     elif f == 'mthfr_ng':
            #         for mthfr_ng in range(len(sublist_mthfr_ng)):
            #             if sublist_mthfr_ng[mthfr_ng][0] == '1.0':
            #                 count_mthfr_ng = count_mthfr_ng + 1
            #         print(count_mthfr_ng, 'mthfr_ng')
            #         if count_mthfr_ng > 0:
            #             mutations_age1_abort1_mthfr_ng_percent = count_mthfr_ng / len(
            #                 sublist_mthfr_ng) * 100
            #             context3['mutations_age1_abort1_mthfr_ng_percent'] = mutations_age1_abort1_mthfr_ng_percent
            #         else:
            #             context3['mutations_age1_abort1_mthfr_ng_percent'] = 0
            #     elif f == 'mthfr_hetero':
            #         for mthfr_hetero in range(len(sublist_mthfr_hetero)):
            #             if sublist_mthfr_hetero[mthfr_hetero][0] == '1.0':
            #                 count_mthfr_hetero = count_mthfr_hetero + 1
            #         print(count_mthfr_hetero, 'mthfr_hetero')
            #         if count_mthfr_hetero > 0:
            #             mutations_age1_abort1_mthfr_hetero_percent = count_mthfr_hetero / len(
            #                 sublist_mthfr_hetero) * 100
            #             context3[
            #                 'mutations_age1_abort1_mthfr_hetero_percent'] = mutations_age1_abort1_mthfr_hetero_percent
            #         else:
            #             context3['mutations_age1_abort1_mthfr_hetero_percent'] = 0
            #     elif f == 'mthfr_homo':
            #         for mthfr_homo in range(len(sublist_mthfr_homo)):
            #             if sublist_mthfr_homo[mthfr_homo][0] == '1.0':
            #                 count_mthfr_homo = count_mthfr_homo + 1
            #         print(count_mthfr_homo, 'mthfr_homo')
            #         if count_mthfr_homo > 0:
            #             mutations_age1_abort1_mthfr_homo_percent = count_mthfr_homo / len(
            #                 sublist_mthfr_homo) * 100
            #             context3['mutations_age1_abort1_mthfr_homo_percent'] = mutations_age1_abort1_mthfr_homo_percent
            #         else:
            #             context3['mutations_age1_abort1_mthfr_homo_percent'] = 0

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

            # print(context3['age_interval'], 'New')
            # print(context3['index_array_age'], 'New', sublist_age)
            # print(prida_list_data_controli, 'Prida List Data')

            # print(sublist_fvl_hetero)
            # context3['sublist_abort'] = sublist_abort

            index_data_array_age1_abort1 = []

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

                # print(sublist_fvl_ng[index_age1_abort1], 'Bravo 1')

            # print(count_fvl_ng_age1_abort1)

            # context3['count_age1'] = count_age1
            # print(sublist_age)
            sublist_fvl_ng = list_fvl_ng[sublist]
            # sublist_age = list_age[sublist]
            # context3['sublist_age'] = sublist_age
            # print(sublist_age)
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

            f_fvl_ng = factor(sublist_fvl_ng)

            context3['count_fvl_ng'] = f_fvl_ng[0]
            context3['count_fvl_ng_0'] = f_fvl_ng[1]
            context3['fvl_1_ng_percent'] = f_fvl_ng[2]
            context3['count_all_fvl_ng_data'] = f_fvl_ng[3]

            f_fvl_hetero = factor(sublist_fvl_hetero)

            context3['count_fvl_hetero'] = f_fvl_hetero[0]
            context3['count_fvl_hetero_0'] = f_fvl_hetero[1]
            context3['fvl_1_hetero_percent'] = f_fvl_hetero[2]
            context3['count_all_fvl_hetero_data'] = f_fvl_hetero[3]

            f_fvl_homo = factor(sublist_fvl_homo)

            context3['count_fvl_homo'] = f_fvl_homo[0]
            context3['count_fvl_homo_0'] = f_fvl_homo[1]
            context3['fvl_1_homo_percent'] = f_fvl_homo[2]
            context3['count_all_fvl_homo_data'] = f_fvl_homo[3]

            f_prothr_ng = factor(sublist_prothr_ng)

            context3['count_prothr_ng'] = f_prothr_ng[0]
            context3['count_prothr_ng_0'] = f_prothr_ng[1]
            context3['prothr_1_ng_percent'] = f_prothr_ng[2]
            context3['count_all_prothr_ng_data'] = f_prothr_ng[3]

            f_prothr_hetero = factor(sublist_prothr_hetero)

            context3['count_prothr_hetero'] = f_prothr_hetero[0]
            context3['count_prothr_hetero_0'] = f_prothr_hetero[1]
            context3['prothr_1_hetero_percent'] = f_prothr_hetero[2]
            context3['count_all_prothr_hetero_data'] = f_prothr_hetero[3]

            f_prothr_homo = factor(sublist_prothr_homo)

            context3['count_prothr_homo'] = f_prothr_homo[0]
            context3['count_prothr_homo_0'] = f_prothr_homo[1]
            context3['prothr_1_homo_percent'] = f_prothr_homo[2]
            context3['count_all_prothr_homo_data'] = f_prothr_homo[3]

            f_pai_ng = factor(sublist_pai_ng)

            context3['count_pai_ng'] = f_pai_ng[0]
            context3['count_pai_ng_0'] = f_pai_ng[1]
            context3['pai_1_ng_percent'] = f_pai_ng[2]
            context3['count_all_pai_ng_data'] = f_pai_ng[3]

            f_pai_hetero = factor(sublist_pai_hetero)

            context3['count_pai_hetero'] = f_pai_hetero[0]
            context3['count_pai_hetero_0'] = f_pai_hetero[1]
            context3['pai_1_hetero_percent'] = f_pai_hetero[2]
            context3['count_all_pai_hetero_data'] = f_pai_hetero[3]

            f_pai_homo = factor(sublist_pai_homo)

            context3['count_pai_homo'] = f_pai_homo[0]
            context3['count_pai_homo_0'] = f_pai_homo[1]
            context3['pai_1_homo_percent'] = f_pai_homo[2]
            context3['count_all_pai_homo_data'] = f_pai_homo[3]

            f_mthfr_ng = factor(sublist_mthfr_ng)

            context3['count_mthfr_ng'] = f_mthfr_ng[0]
            context3['count_mthfr_ng_0'] = f_mthfr_ng[1]
            context3['mthfr_1_ng_percent'] = f_mthfr_ng[2]
            context3['count_all_mthfr_ng_data'] = f_mthfr_ng[3]

            f_mthfr_hetero = factor(sublist_mthfr_hetero)

            context3['count_mthfr_hetero'] = f_mthfr_hetero[0]
            context3['count_mthfr_hetero_0'] = f_mthfr_hetero[1]
            context3['mthfr_1_hetero_percent'] = f_mthfr_hetero[2]
            context3['count_all_mthfr_hetero_data'] = f_mthfr_hetero[3]

            f_mthfr_homo = factor(sublist_mthfr_homo)

            context3['count_mthfr_homo'] = f_mthfr_homo[0]
            context3['count_mthfr_homo_0'] = f_mthfr_homo[1]
            context3['mthfr_1_homo_percent'] = f_mthfr_homo[2]
            context3['count_all_mthfr_homo_data'] = f_mthfr_homo[3]
    #########################
    ##  End Button Submit  ##
    #########################

    if request.method == 'POST':
        if 'btn_patients_more_mutations' in request.POST:
            print('Controli')

            count_pai_homo_mutations = 0
            for pai_homo_data in list_pai_homo:
                if pai_homo_data[0] == '1.0':
                    count_pai_homo_mutations = count_pai_homo_mutations + 1
            # print('PAI Homo Mutations are:', count_pai_homo_mutations)

            count_mthfr_homo_mutations = 0
            for mthfr_homo_data in list_mthfr_homo:
                if mthfr_homo_data[0] == '1.0':
                    count_mthfr_homo_mutations = count_mthfr_homo_mutations + 1
            # print('MTHFR Homo Mutations are:', count_mthfr_homo_mutations)
            #
            # print('######################################')
            # print('\n')

            # print('More Mutations!@!!', prida_list_data_controli, len(prida_list_data_controli))
            factor_1 = []
            # list_factors = []

            for prida_list in prida_list_data_controli:
                if prida_list == 'fvl_hetero':
                    factor_1.append(list_fvl_hetero)
                elif prida_list == 'fvl_homo':
                    factor_1.append(list_fvl_homo)
                elif prida_list == 'prothr_hetero':
                    factor_1.append(list_prothr_hetero)
                elif prida_list == 'prothr_homo':
                    factor_1.append(list_prothr_homo)
                elif prida_list == 'pai_hetero':
                    factor_1.append(list_pai_hetero)
                elif prida_list == 'pai_homo':
                    factor_1.append(list_pai_homo)
                elif prida_list == 'mthfr_hetero':
                    factor_1.append(list_mthfr_hetero)
                elif prida_list == 'mthfr_homo':
                    factor_1.append(list_mthfr_homo)
                # list_factors.append(factor_1)

            # print('List Factor_1')
            # print(factor_1, len(factor_1), len(list_fvl_ng))
            rows_number = len(list_fvl_ng)

            count_factor_mutations = 0
            count_rows_num = 0
            list_index_mutations = []
            dict_patients_data_mutations = {}
            list_age_mutations = []
            list_aborts_mutations = []

            if len(prida_list_data_controli) == 2:
                for i in range(rows_number):
                    if factor_1[0][i][0] == factor_1[1][i][0] == '1.0':
                        list_index_mutations.append(count_rows_num)
                        # list_age_mutations.append(list_age[count_rows_num][0])
                        list_aborts_mutations.append(list_abort[count_rows_num][0])
                        count_factor_mutations = count_factor_mutations + 1
                    count_rows_num = count_rows_num + 1

            elif len(prida_list_data_controli) == 3:
                for i in range(rows_number):
                    if factor_1[0][i][0] == factor_1[1][i][0] == factor_1[2][i][0] == '1.0':
                        list_index_mutations.append(count_rows_num)
                        # list_age_mutations.append(list_age[count_rows_num][0])
                        list_aborts_mutations.append(list_abort[count_rows_num][0])
                        count_factor_mutations = count_factor_mutations + 1
                    count_rows_num = count_rows_num + 1

            elif len(prida_list_data_controli) == 4:
                for i in range(rows_number):
                    if factor_1[0][i][0] == factor_1[1][i][0] == factor_1[2][i][0] == factor_1[3][i][0] == '1.0':
                        list_index_mutations.append(count_rows_num)
                        # list_age_mutations.append(list_age[count_rows_num][0])
                        list_aborts_mutations.append(list_abort[count_rows_num][0])
                        count_factor_mutations = count_factor_mutations + 1
                    count_rows_num = count_rows_num + 1

            dict_patients_data_mutations['mutations_number'] = len(prida_list_data_controli)
            dict_patients_data_mutations['age'] = list_age_mutations
            dict_patients_data_mutations['aborts'] = list_aborts_mutations
            # print('List of Mutations')
            print(list_index_mutations, count_factor_mutations, count_rows_num)
            # print('List Patients with Mutations')
            print(dict_patients_data_mutations)

            print('OHO', factor_1)
            print(list_prothr_ng)
            data_fvl_hetero = []
            data_index_fvl_hetero = []

            count_fvl_hetero = 0
            index_fvl_hetero = 0
            for fvl_hetero in list_fvl_hetero:

                if fvl_hetero[0] == '1.0':
                    data_fvl_hetero.append(fvl_hetero)
                    data_index_fvl_hetero.append(index_fvl_hetero)

                    count_fvl_hetero = count_fvl_hetero + 1
                index_fvl_hetero = index_fvl_hetero + 1

            index_mutation = []
            for mutation in data_index_fvl_hetero:
                if list_pai_hetero[mutation][0] == '1.0':
                    index_mutation.append(mutation)
            # print(index_mutation, len(index_mutation))

    ##  Vizualization of the data ###
    if request.method == "POST":
        if 'save_controli' in request.POST:
            pk = request.POST.get('save')
            if not pk:
                prida_controli_form = PridaControliForm(request.POST)
            else:
                p_controli = PridaControli.objects.get(id=pk)
                prida_controli_form = PridaControliForm(request.POST, instance=p_controli)

            prida_controli_form.save()
            prida_controli_form = PridaControliForm()

        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            p_controli = PridaControli.objects.get(id=pk)
            p_controli.delete()
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            p_controli = PridaControli.objects.get(id=pk)
            prida_controli_form = PridaControliForm(instance=p_controli)
            print('Hello')
    # print(prida_list_data_controli, len(prida_list_data_controli))
    for select_factor in prida_list_data_controli:
        if select_factor == 'fvl_ng':
            context3['factor_fvl_ng'] = select_factor
        elif select_factor == 'fvl_hetero':
            context3['factor_fvl_hetero'] = select_factor
        print(select_factor)

    if prida_list_data_controli:
        print(prida_list_data_controli[0])

        context3['prida_list_data_controli'] = prida_list_data_controli
        # print(context3['prida_list_data_controli'])

    # context3['prida_list_data'] = prida_list_data
    context3['prida_controli'] = prida_controli
    context3['prida_controli_form'] = prida_controli_form
    context3['st_line'] = start_line_controli

    return render(request, 'controli.html', context3)


## Function Patients ##
def proba1(request):
    context3 = {}

    prida_mutations = PridaMutations.objects.all()  ## Zarejda model PridaMutations ot models.py

    prida_mutations_form = PridaMutationsForm()  ## Zarejda form PridaMutationsForm ot forms.py

    list_age = PridaMutations.objects.values_list('age')  ## Promenliva - spisak sas stoinostite na colona "age"

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

    prida_list_data = request.POST.getlist('prida_list_data')  ## Spisak s izbrani ot usera checkboxes s factori
    prida_age_list = request.POST.getlist('age')  ## Spisak s izbrana ot usera vazrast
    prida_abort_list = request.POST.getlist('abort')  ## Spisak s izbrani ot usera aborti

    start_line = request.POST.get('start_line')
    end_line = request.POST.get('end_line')  ## Promenliva, poluchava vavedenata stoinost ot proba1.html

    print('START LINE', start_line)

    age = ''
    for data in prida_age_list:
        if data == 'age1' or data == 'age2' or data == 'age3':
            age = data  ## Priema stoinost na izbran checkbox v colona AGE
    print(age, 'AGE')
    abort = ''
    for data in prida_abort_list:
        if data == 'abort_1' or data == 'abort_2' or data == 'abort_3':
            abort = data  ## Priema stoinost na izbran checkbox v colona ABORTS
    print(abort, 'ABORT')

    # Control Button "Calculate Aborts Mutations"

    if request.method == 'POST':
        if 'calculate_mutations_aborts' in request.POST:
            # print('Calculate Mutations Aborts')
            # print(prida_list_data, 'OK111')
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

            context3['index_array_age'] = create_array_age_and_age_interval_access_html(prida_age_list,
                                                                                        index_array_age1,
                                                                                        index_array_age2,
                                                                                        index_array_age3)[
                'index_array_age']

            context3['age_interval_aborts'] = create_array_age_and_age_interval_access_html(prida_age_list,
                                                                                            index_array_age1,
                                                                                            index_array_age2,
                                                                                            index_array_age3)[
                'age_interval']
            index_array_age_data = context3['index_array_age']

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

            print(prida_list_data)

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
            context3['factor_type'] = prida_list_data

            # context3['factor_type'] = res_func1[6]

            print(context3['count_mutations_abort1'],
                  context3['percent_mutations_abort1'],
                  context3['count_mutations_abort2'],
                  context3['percent_mutations_abort2'],
                  context3['count_mutations_abort3'],
                  context3['percent_mutations_abort3'])

            print(context3['index_array_age'], 'New', sublist_age)
            print(prida_list_data[0], 'Prida List Data')

        # if request.method == 'POST':
        elif 'btn_excel_extract' in request.POST:
            print('Extract Data to Excel')
            wb = Workbook()
            ws = wb.active
            ws.title = "Product"

            headers = ['id', 'code', 'age', 'fvl_ng', 'fvl_hetero', 'fvl_homo',
                       'prothr_ng', 'prothr_hetero', 'prothr_homo',
                       'pai_ng', 'pai_hetero', 'pai_homo',
                       'mthfr_ng', 'mthfr_hetero', 'mthfr_homo']
            ws.append(headers)

            for data in prida_mutations:
                ws.append([data.id, data.code, data.age, data.fvl_ng, data.fvl_hetero, data.fvl_homo,
                           data.prothr_ng, data.prothr_hetero, data.prothr_homo,
                           data.pai_ng, data.pai_hetero, data.pai_homo,
                           data.mthfr_ng, data.mthfr_hetero, data.mthfr_homo])

            wb.save('prida_mutations_excel.xlsx')
            print('Extract Data to Excel 2')

    # Control Button "Results: Mutations"
    if request.method == 'POST':
        print("Control Button Results: Mutations")


        if 'btn_patients_more_mutations' in request.POST:
            print("Control Button Results: Mutations")

            ######################################################
            ### Heterozygous Factor V Leiden               #######
            ###  and Prothr Hetero Mutation                #######
            ######################################################

            c_cnt_fvl_hetero_prothr_hetero_mutations = 0
            c_cnt_fvl_hetero_prothr_hetero_mut = 0
            c_cnt_fvl_hetero_prothr_hetero_mut_aborts = 0

            for fvl_hetero in range(len(list_fvl_hetero)):

                if list_fvl_hetero[fvl_hetero][0] == list_prothr_hetero[fvl_hetero][0] == '1.0':
                    c_cnt_fvl_hetero_prothr_hetero_mut = c_cnt_fvl_hetero_prothr_hetero_mut + 1
                    # c_cnt_fvl_hetero_prothr_hetero_mut_aborts = c_cnt_fvl_hetero_prothr_hetero_mut_aborts + 1
                c_cnt_fvl_hetero_prothr_hetero_mutations = c_cnt_fvl_hetero_prothr_hetero_mutations + 1

            context3['c_cnt_fvl_hetero_prothr_hetero_mut'] = c_cnt_fvl_hetero_prothr_hetero_mut
            print('FVL Hetero', c_cnt_fvl_hetero_prothr_hetero_mut)

            #####################################################
            ### Start 1 Abort 3 Mutations #######################
            #####################################################
            count_abort1_mutations3 = 0
            for in_abort in range(len(list_abort)):
                if ((list_abort[in_abort][0] == '1.0')
                        and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][
                            0] == '1.0'
                             or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                             or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] ==
                             list_pai_homo[in_abort][0] == '1.0'
                             or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] ==
                             list_pai_homo[in_abort][0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][
                                 0] == '1.0'
                             or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] ==
                             list_mthfr_homo[in_abort][0] == '1.0'
                        )
                ):
                    count_abort1_mutations3 = count_abort1_mutations3 + 1
            # print('1 Abort and 3 mutations: ', count_abort1_mutations3)

            #####################################################
            ### End 1 Abort 3 Mutations #########################
            #####################################################

            #####################################################
            ### Start 2 Aborts 3 Mutations ######################
            #####################################################
            # count_abort2_mutations3 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '2.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][
            #                  0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] ==
            #                  list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] ==
            #                  list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] ==
            #                  list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] ==
            #                  list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] ==
            #                  list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][
            #                      0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] ==
            #                  list_mthfr_homo[in_abort][0] == '1.0'
            #             )
            #     ):
            #         count_abort2_mutations3 = count_abort2_mutations3 + 1
            # print('2 Aborts and 3 mutations: ', count_abort2_mutations3)

            #####################################################
            ### End 2 Aborts 3 Mutations ########################
            #####################################################

            #####################################################
            ### Start 3 Aborts 3 Mutations ######################
            #####################################################
            # count_abort3_mutations3 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '3.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][
            #                 0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] ==
            #                  list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] ==
            #                  list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] ==
            #                  list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] ==
            #                  list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] ==
            #                  list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][
            #                      0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] ==
            #                  list_mthfr_homo[in_abort][0] == '1.0'
            #             )
            #     ):
            #         count_abort3_mutations3 = count_abort3_mutations3 + 1
            # print('3 Aborts and 3 mutations: ', count_abort3_mutations3)

            #####################################################
            ### End 2 Aborts 3 Mutations ########################
            #####################################################

            #####################################################
            ### Start 4 Aborts 3 Mutations ######################
            #####################################################
            # count_abort4_mutations3 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '4.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][
            #                 0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] ==
            #                  list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] ==
            #                  list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] ==
            #                  list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] ==
            #                  list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] ==
            #                  list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][
            #                      0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] ==
            #                  list_mthfr_homo[in_abort][0] == '1.0'
            #             )
            #     ):
            #         count_abort4_mutations3 = count_abort4_mutations3 + 1
            # print('4 Aborts and 3 mutations: ', count_abort4_mutations3)
            # print('\n')

            #####################################################
            ### End 4 Aborts 3 Mutations ########################
            #####################################################

            # count_mutations_2 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '1.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_pai_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0')
            #     ):
            #         count_mutations_2 = count_mutations_2 + 1
            # print('1 Abort and 2 mutations: ', count_mutations_2)

            ######################################################
            ### Start 2 Aborts and 2 mutations ###################
            ######################################################
            # count_mutations_abort_2 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '2.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_pai_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0')
            #     ):
            #         count_mutations_abort_2 = count_mutations_abort_2 + 1
            # print('2 Aborts and 2 mutations: ', count_mutations_abort_2)

            ######################################################
            ### End ##############################################
            ######################################################

            ######################################################
            ### Start 3 Aborts and 2 mutations ###################
            ######################################################
            # count_mutations_abort_3 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '3.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_pai_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0')
            #     ):
            #         count_mutations_abort_3 = count_mutations_abort_3 + 1
            # print('3 Aborts and 2 mutations: ', count_mutations_abort_3)

            ######################################################
            ### End ##############################################
            ######################################################

            ######################################################
            ### Start 4 Aborts and 2 mutations ###################
            ######################################################
            # count_mutations_abort_4 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '4.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_pai_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0')
            #     ):
            #         count_mutations_abort_4 = count_mutations_abort_4 + 1
            # print('4 Aborts and 2 mutations: ', count_mutations_abort_4)

            ######################################################
            ### End ##############################################
            ######################################################

            ######################################################
            ### Start 5 Aborts and 2 mutations ###################
            ######################################################
            # count_mutations_abort_5 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '5.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_pai_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0')
            #     ):
            #         count_mutations_abort_5 = count_mutations_abort_5 + 1
            # print('5 Aborts and 2 mutations: ', count_mutations_abort_5)

            ######################################################
            ### End ##############################################
            ######################################################

            ######################################################
            ### Start 6 Aborts and 2 mutations ###################
            ######################################################
            # count_mutations_abort_6 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '6.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_pai_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0')
            #     ):
            #         count_mutations_abort_6 = count_mutations_abort_6 + 1
            # print('6 Aborts and 2 mutations: ', count_mutations_abort_6)

            ######################################################
            ### End ##############################################
            ######################################################

            ######################################################
            ### Start 7 Aborts and 2 mutations ###################
            ######################################################
            # count_mutations_abort_7 = 0
            # for in_abort in range(len(list_abort)):
            #     if ((list_abort[in_abort][0] == '7.0')
            #             and (list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_prothr_hetero[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_fvl_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_hetero[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_pai_homo[in_abort][0] == '1.0'
            #                  or list_prothr_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0'
            #                  or list_pai_homo[in_abort][0] == list_mthfr_homo[in_abort][0] == '1.0')
            #     ):
            #         count_mutations_abort_7 = count_mutations_abort_7 + 1
            # print('7 Aborts and 2 mutations: ', count_mutations_abort_7)
            # print('\n')
            ######################################################
            ### End ##############################################
            ######################################################

            # count_fvl_hetero_2_mutations = 0
            # for in_fvl_hetero_aborts_2 in range(len(list_abort)):
            #     if ((list_abort[in_fvl_hetero_aborts_2][0] == '2.0' or
            #          list_abort[in_fvl_hetero_aborts_2][0] == '3.0') and
            #             list_fvl_hetero[in_fvl_hetero_aborts_2][0] == '1.0'):
            #         count_fvl_hetero_2_mutations = count_fvl_hetero_2_mutations + 1
            # print('FVL Hetero Mutations 2 or more are:', count_fvl_hetero_2_mutations)

            # count_fvl_homo_2_mutations = 0
            # for in_fvl_homo_aborts_2 in range(len(list_abort)):
            #     if ((list_abort[in_fvl_homo_aborts_2][0] != '1.0' or
            #          list_abort[in_fvl_homo_aborts_2][0] != '') and
            #             list_fvl_homo[in_fvl_homo_aborts_2][0] == '1.0'):
            #         count_fvl_homo_2_mutations = count_fvl_homo_2_mutations + 1
            # print('FVL Homo Mutations 2 or more are:', count_fvl_homo_2_mutations)

            # count_prothr_hetero_2_mutations = 0
            # for in_prothr_hetero_aborts_2 in range(len(list_abort)):
            #     if ((list_abort[in_prothr_hetero_aborts_2][0] != '1.0' or
            #          list_abort[in_prothr_hetero_aborts_2][0] != '') and
            #             list_prothr_hetero[in_prothr_hetero_aborts_2][0] == '1.0'):
            #         count_prothr_hetero_2_mutations = count_prothr_hetero_2_mutations + 1
            # print('PROTHR Hetero Mutations 2 or more are:', count_prothr_hetero_2_mutations)

            # count_prothr_homo_2_mutations = 0
            # for in_prothr_homo_aborts_2 in range(len(list_abort)):
            #     if ((list_abort[in_prothr_homo_aborts_2][0] != '1.0' or
            #          list_abort[in_prothr_homo_aborts_2][0] != '') and
            #             list_prothr_homo[in_prothr_homo_aborts_2][0] == '1.0'):
            #         count_prothr_homo_2_mutations = count_prothr_homo_2_mutations + 1
            # print('PROTHR Homo Mutations 2 or more are:', count_prothr_homo_2_mutations)

            # count_pai_homo_2_mutations = 0
            # for in_pai_homo_aborts_2 in range(len(list_abort)):
            #     if ((list_abort[in_pai_homo_aborts_2][0] != '1.0' or
            #          list_abort[in_pai_homo_aborts_2][0] != '') and
            #             list_pai_homo[in_pai_homo_aborts_2][0] == '1.0'):
            #         count_pai_homo_2_mutations = count_pai_homo_2_mutations + 1
            # print('PAI Homo Mutations 2 or more are:', count_pai_homo_2_mutations)

            # count_mthfr_homo_2_mutations = 0
            # for in_mthfr_homo_aborts_2 in range(len(list_abort)):
            #     if ((list_abort[in_mthfr_homo_aborts_2][0] != '1.0' or
            #          list_abort[in_mthfr_homo_aborts_2][0] != '') and
            #             list_mthfr_homo[in_mthfr_homo_aborts_2][0] == '1.0'):
            #         count_mthfr_homo_2_mutations = count_mthfr_homo_2_mutations + 1
            # print('MTHFR Homo Mutations 2 or more are:', count_mthfr_homo_2_mutations)

            # print('\n')
            # print('######################################')
            # count_fvl_hetero_mutations = 0
            # for fvl_hetero_data in list_fvl_hetero:
            #     if fvl_hetero_data[0] == '1.0':
            #         count_fvl_hetero_mutations = count_fvl_hetero_mutations + 1
            # print('FVL Hetero Mutations are:', count_fvl_hetero_mutations)

            # count_fvl_homo_mutations = 0
            # for fvl_homo_data in list_fvl_homo:
            #     if fvl_homo_data[0] == '1.0':
            #         count_fvl_homo_mutations = count_fvl_homo_mutations + 1
            # print('FVL Homo Mutations are:', count_fvl_homo_mutations)

            # count_prothr_hetero_mutations = 0
            # for prothr_hetero_data in list_prothr_hetero:
            #     if prothr_hetero_data[0] == '1.0':
            #         count_prothr_hetero_mutations = count_prothr_hetero_mutations + 1
            # print('PROTHR Hetero Mutations are:', count_prothr_hetero_mutations)

            # count_prothr_homo_mutations = 0
            # for prothr_homo_data in list_prothr_homo:
            #     if prothr_homo_data[0] == '1.0':
            #         count_prothr_homo_mutations = count_prothr_homo_mutations + 1
            # print('PROTHR Homo Mutations are:', count_prothr_homo_mutations)

            count_pai_homo_mutations = 0
            for pai_homo_data in list_pai_homo:
                if pai_homo_data[0] == '1.0':
                    count_pai_homo_mutations = count_pai_homo_mutations + 1
            print('PAI Homo Mutations are:', count_pai_homo_mutations)

            count_mthfr_homo_mutations = 0
            for mthfr_homo_data in list_mthfr_homo:
                if mthfr_homo_data[0] == '1.0':
                    count_mthfr_homo_mutations = count_mthfr_homo_mutations + 1
            print('MTHFR Homo Mutations are:', count_mthfr_homo_mutations)

            print('######################################')
            print('\n')

            print('More Mutations!@!!', prida_list_data, len(prida_list_data))
            factor_1 = []
            # list_factors = []

            for prida_list in prida_list_data:
                if prida_list == 'fvl_hetero':
                    factor_1.append(list_fvl_hetero)
                elif prida_list == 'fvl_homo':
                    factor_1.append(list_fvl_homo)
                elif prida_list == 'prothr_hetero':
                    factor_1.append(list_prothr_hetero)
                elif prida_list == 'prothr_homo':
                    factor_1.append(list_prothr_homo)
                elif prida_list == 'pai_hetero':
                    factor_1.append(list_pai_hetero)
                elif prida_list == 'pai_homo':
                    factor_1.append(list_pai_homo)
                elif prida_list == 'mthfr_hetero':
                    factor_1.append(list_mthfr_hetero)
                elif prida_list == 'mthfr_homo':
                    factor_1.append(list_mthfr_homo)
                # list_factors.append(factor_1)

            print('List Factor_1')
            print(factor_1, len(factor_1), len(list_fvl_ng))
            rows_number = len(list_fvl_ng)
            # print('Factor 1: ', factor_1[0][0][0])
            # print('List of All Factors')
            # print(list_factors)
            # print(len(list_factors))

            count_factor_mutations = 0
            count_rows_num = 0
            list_index_mutations = []
            dict_patients_data_mutations = {}
            list_age_mutations = []
            list_aborts_mutations = []

            if len(prida_list_data) == 2:
                for i in range(rows_number):
                    if factor_1[0][i][0] == factor_1[1][i][0] == '1.0':
                        list_index_mutations.append(count_rows_num)
                        list_age_mutations.append(list_age[count_rows_num][0])
                        list_aborts_mutations.append(list_abort[count_rows_num][0])
                        count_factor_mutations = count_factor_mutations + 1
                    count_rows_num = count_rows_num + 1

            elif len(prida_list_data) == 3:
                for i in range(rows_number):
                    if factor_1[0][i][0] == factor_1[1][i][0] == factor_1[2][i][0] == '1.0':
                        list_index_mutations.append(count_rows_num)
                        list_age_mutations.append(list_age[count_rows_num][0])
                        list_aborts_mutations.append(list_abort[count_rows_num][0])
                        count_factor_mutations = count_factor_mutations + 1
                    count_rows_num = count_rows_num + 1

            elif len(prida_list_data) == 4:
                for i in range(rows_number):
                    if factor_1[0][i][0] == factor_1[1][i][0] == factor_1[2][i][0] == factor_1[3][i][0] == '1.0':
                        list_index_mutations.append(count_rows_num)
                        list_age_mutations.append(list_age[count_rows_num][0])
                        list_aborts_mutations.append(list_abort[count_rows_num][0])
                        count_factor_mutations = count_factor_mutations + 1
                    count_rows_num = count_rows_num + 1

            dict_patients_data_mutations['mutations_number'] = len(prida_list_data)
            dict_patients_data_mutations['age'] = list_age_mutations
            dict_patients_data_mutations['aborts'] = list_aborts_mutations
            print('List of Mutations')
            print(list_index_mutations, count_factor_mutations, count_rows_num)
            print('List Patients with Mutations')
            print(dict_patients_data_mutations)

            # print('List of Factor 0')
            # print(factor_1[0])
            # print(len(factor_1[0]))
            # print('List of Factor 1')
            # print(factor_1[1])
            # print(len(factor_1[1]))
            # for factor0_mutations in factor_1[0][0]:
            #     if factor0_mutations[0] == '1.0':
            #         list_index_mutations.append(count_factor_mutations)
            #     count_factor_mutations = count_factor_mutations + 1
            #
            #
            #
            # list_index_mutations1 = []
            # count_f_m = 0
            # print(len(factor_1[1]))
            # for factor_mutations in list_index_mutations:
            #     if factor_1[1][factor_mutations][0] == '1.0':
            #         list_index_mutations1.append(factor_mutations)
            #         count_f_m = count_f_m + 1
            # print('List of All Mutations')
            # print(list_index_mutations1)
            # print(count_f_m)

            print('OHO', factor_1)
            print(list_prothr_ng)
            data_fvl_hetero = []
            data_index_fvl_hetero = []
            data_fvl_homo = []

            count_fvl_homo = 0
            count_fvl_hetero = 0
            index_fvl_hetero = 0
            for fvl_hetero in list_fvl_hetero:

                if fvl_hetero[0] == '1.0':
                    data_fvl_hetero.append(fvl_hetero)
                    data_index_fvl_hetero.append(index_fvl_hetero)

                    # data_fvl_homo.append(fvl_homo)
                    count_fvl_hetero = count_fvl_hetero + 1
                    # count_fvl_homo = count_fvl_homo + 1
                index_fvl_hetero = index_fvl_hetero + 1
            # print(data_fvl_hetero)
            print(data_index_fvl_hetero)
            print(list_fvl_hetero[9], list_fvl_hetero[10], list_fvl_hetero[22])
            print(count_fvl_hetero)

            index_mutation = []
            for mutation in data_index_fvl_hetero:
                # print(list_pai_hetero[mutation])
                if list_pai_hetero[mutation][0] == '1.0':
                    index_mutation.append(mutation)
            print(index_mutation, len(index_mutation))

    if request.method == 'POST':
        if 'submit' in request.POST:
            # print(type(int(p)), 'OK')
            # print(int(p))
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
                elif sublist_abort[abort][0] != '?' or sublist_abort[abort][0] != '2.0' or sublist_abort[abort][
                    0] != '1.0':
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
                        mutations_age1_abort1_fvl_hetero_percent = count_fvl_hetero / len(
                            context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_fvl_hetero_percent'] = mutations_age1_abort1_fvl_hetero_percent
                    else:
                        context3['mutations_age1_abort1_fvl_hetero_percent'] = 0
                elif f == 'fvl_homo':
                    for fvl_homo in context3['index_array_abort']:
                        if sublist_fvl_homo[fvl_homo][0] == '1.0':
                            count_fvl_homo = count_fvl_homo + 1
                    print(count_fvl_homo, 'fvl_homo')
                    if count_fvl_homo > 0:
                        mutations_age1_abort1_fvl_homo_percent = count_fvl_homo / len(
                            context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_fvl_homo_percent'] = mutations_age1_abort1_fvl_homo_percent
                    else:
                        context3['mutations_age1_abort1_fvl_homo_percent'] = 0
                elif f == 'prothr_ng':
                    for prothr_ng in context3['index_array_abort']:
                        if sublist_prothr_ng[prothr_ng][0] == '1.0':
                            count_prothr_ng = count_prothr_ng + 1
                    print(count_prothr_ng, 'prothr_ng')
                    if count_prothr_ng > 0:
                        mutations_age1_abort1_prothr_ng_percent = count_prothr_ng / len(
                            context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_prothr_ng_percent'] = mutations_age1_abort1_prothr_ng_percent
                    else:
                        context3['mutations_age1_abort1_prothr_ng_percent'] = 0
                elif f == 'prothr_hetero':
                    for prothr_hetero in context3['index_array_abort']:
                        if sublist_prothr_hetero[prothr_hetero][0] == '1.0':
                            count_prothr_hetero = count_prothr_hetero + 1
                    print(count_prothr_hetero, 'prothr_hetero')
                    if count_prothr_hetero > 0:
                        mutations_age1_abort1_prothr_hetero_percent = count_prothr_hetero / len(
                            context3['index_array_abort']) * 100
                        context3[
                            'mutations_age1_abort1_prothr_hetero_percent'] = mutations_age1_abort1_prothr_hetero_percent
                    else:
                        context3['mutations_age1_abort1_prothr_hetero_percent'] = 0
                elif f == 'prothr_homo':
                    for prothr_homo in context3['index_array_abort']:
                        if sublist_prothr_homo[prothr_homo][0] == '1.0':
                            count_prothr_homo = count_prothr_homo + 1
                    print(count_prothr_homo, 'prothr_homo')
                    if count_prothr_homo > 0:
                        mutations_age1_abort1_prothr_homo_percent = count_prothr_homo / len(
                            context3['index_array_abort']) * 100
                        context3[
                            'mutations_age1_abort1_prothr_homo_percent'] = mutations_age1_abort1_prothr_homo_percent
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
                        mutations_age1_abort1_pai_hetero_percent = count_pai_hetero / len(
                            context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_pai_hetero_percent'] = mutations_age1_abort1_pai_hetero_percent
                    else:
                        context3['mutations_age1_abort1_pai_hetero_percent'] = 0
                elif f == 'pai_homo':
                    for pai_homo in context3['index_array_abort']:
                        if sublist_pai_homo[pai_homo][0] == '1.0':
                            count_pai_homo = count_pai_homo + 1
                    print(count_pai_homo, 'pai_homo')
                    if count_pai_homo > 0:
                        mutations_age1_abort1_pai_homo_percent = count_pai_homo / len(
                            context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_pai_homo_percent'] = mutations_age1_abort1_pai_homo_percent
                    else:
                        context3['mutations_age1_abort1_pai_homo_percent'] = 0
                elif f == 'mthfr_ng':
                    for mthfr_ng in context3['index_array_abort']:
                        if sublist_mthfr_ng[mthfr_ng][0] == '1.0':
                            count_mthfr_ng = count_mthfr_ng + 1
                    print(count_mthfr_ng, 'mthfr_ng')
                    if count_mthfr_ng > 0:
                        mutations_age1_abort1_mthfr_ng_percent = count_mthfr_ng / len(
                            context3['index_array_abort']) * 100
                        context3['mutations_age1_abort1_mthfr_ng_percent'] = mutations_age1_abort1_mthfr_ng_percent
                    else:
                        context3['mutations_age1_abort1_mthfr_ng_percent'] = 0
                elif f == 'mthfr_hetero':
                    for mthfr_hetero in context3['index_array_abort']:
                        if sublist_mthfr_hetero[mthfr_hetero][0] == '1.0':
                            count_mthfr_hetero = count_mthfr_hetero + 1
                    print(count_mthfr_hetero, 'mthfr_hetero')
                    if count_mthfr_hetero > 0:
                        mutations_age1_abort1_mthfr_hetero_percent = count_mthfr_hetero / len(
                            context3['index_array_abort']) * 100
                        context3[
                            'mutations_age1_abort1_mthfr_hetero_percent'] = mutations_age1_abort1_mthfr_hetero_percent
                    else:
                        context3['mutations_age1_abort1_mthfr_hetero_percent'] = 0
                elif f == 'mthfr_homo':
                    for mthfr_homo in context3['index_array_abort']:
                        if sublist_mthfr_homo[mthfr_homo][0] == '1.0':
                            count_mthfr_homo = count_mthfr_homo + 1
                    print(count_mthfr_homo, 'mthfr_homo')
                    if count_mthfr_homo > 0:
                        mutations_age1_abort1_mthfr_homo_percent = count_mthfr_homo / len(
                            context3['index_array_abort']) * 100
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
    print(in_array_d, 'INDEX A D')
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
        res_count_mutations_abort3, percent_mutations_abort3, factor_type


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
def func2(
        in_array_d,
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
    count_mutations = 0
    count_mutations_abort2 = 0

    count_mutations_abort1 = 0
    count_mutations_abort3 = 0

    factor_type = in_array_d[0]
    print('FACTOR TYPE', in_array_d[0])
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
    print(in_array_d, 'IN ARRAY D')
    for factor_index in in_array_d:
        print(sublist_factor, 'Sublist FVL NG')
        print(sublist_factor[1][0], 'Result')
        count_mutations = 0
        # count_mutations = count_mutations + 1
        count_mutations_abort1 = count_mutations_abort1 + 1
        count_mutations_abort2 = count_mutations_abort2 + 1
        count_mutations_abort3 = count_mutations_abort3 + 1

        for f_in in range(len(sublist_factor)):
            print(sublist_factor[f_in][0])
            if sublist_factor[f_in][0] == '1.0':
                count_mutations = count_mutations + 1

        # if sublist_factor[factor_index][0] == '1.0':
        #     count_mutations = count_mutations + 1
        #     # print('OKK')
        #     if subl_abort[factor_index][0] == '0.0':
        #         count_mutations_abort1 = count_mutations_abort1 + 1
        #         print(count_mutations_abort1)
        #     elif subl_abort[factor_index][0] == '2.0':
        #         count_mutations_abort2 = count_mutations_abort2 + 1
        #         print(count_mutations_abort2)
        #     else:
        #         count_mutations_abort3 = count_mutations_abort3 + 1
        #         print(count_mutations_abort3)
    res_count_mutations = count_mutations
    # res_count_mutations_abort1 = count_mutations_abort1
    # print('Start')
    # print(res_count_mutations_abort1)
    percent_mutations = round(res_count_mutations * 100 / cli_list, 2)

    print(res_count_mutations, percent_mutations, 'C MUT and % MUT')

    # percent_mutations_abort1 = round(res_count_mutations_abort1 * 100 / cli_list, 2)

    # print(percent_mutations_abort1)
    # res_count_mutations_abort2 = count_mutations_abort2
    # print(res_count_mutations_abort2)
    # percent_mutations_abort2 = round(res_count_mutations_abort2 * 100 / cli_list, 2)
    # print(percent_mutations_abort2)

    # res_count_mutations_abort3 = count_mutations_abort3
    # print(res_count_mutations_abort3)
    # percent_mutations_abort3 = round(res_count_mutations_abort3 * 100 / cli_list, 2)
    # print(percent_mutations_abort3)
    # print('Stop')
    # return res_count_mutations_abort1, percent_mutations_abort1, \
    #     res_count_mutations_abort2, percent_mutations_abort2, \
    #     res_count_mutations_abort3, percent_mutations_abort3, factor_type

    return res_count_mutations, percent_mutations, factor_type


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
