from django.db import models


class Patients(models.Model):
    patient_id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    years = models.PositiveIntegerField(blank=True, null=True)
    probe_date = models.DateField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    arterial_pressure = models.CharField(max_length=20, blank=True, null=True)
    gw = models.IntegerField(blank=True, null=True)
    baby_weight = models.IntegerField(blank=True, null=True)
    erythrocytes = models.FloatField(blank=True, null=True)
    hemoglobin = models.FloatField(blank=True, null=True)
    #

    def __str__(self):
        return self.name


class PatientProba(models.Model):
    patient_id = models.SmallAutoField(primary_key=True)
    # name = models.CharField(max_length=255)

    name = models.CharField(max_length=20, blank=True, null=True)
    years = models.PositiveIntegerField(blank=True, null=True)
    # name = models.CharField(max_length=20)
    # years = models.PositiveIntegerField()


# Create your models here.
class Score(models.Model):
    # objects = None

    name = models.CharField(max_length=50)
    value = models.PositiveSmallIntegerField()

    # code = models.CharField(max_length=20)
    # birth_year = models.CharField(max_length=10)
    # number = models.PositiveIntegerField()
    # age = models.PositiveSmallIntegerField()
    # sex = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Prida(models.Model):
    # id = models.PositiveSmallIntegerField(default=0, primary_key=1)
    code = models.CharField(max_length=20)
    birth_year = models.CharField(max_length=10, null=True, blank=True)
    number = models.PositiveIntegerField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    sex = models.CharField(max_length=10)
    fvl = models.CharField(max_length=3, null=True)
    prothr = models.CharField(max_length=3, null=True)
    pai = models.CharField(max_length=3, null=True)
    mthfr = models.CharField(max_length=3, null=True)


class PridaMutations(models.Model):
    # id = models.PositiveSmallIntegerField(default=0, primary_key=1)
    code = models.CharField(max_length=20)
    # birth_year = models.PositiveIntegerField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    fvl_ng = models.CharField(max_length=3, null=True, blank=True)
    fvl_hetero = models.CharField(max_length=3, null=True, blank=True)
    fvl_homo = models.CharField(max_length=3, null=True, blank=True)

    prothr_ng = models.CharField(max_length=3, null=True, blank=True)
    prothr_hetero = models.CharField(max_length=3, null=True, blank=True)
    prothr_homo = models.CharField(max_length=3, null=True, blank=True)

    pai_ng = models.CharField(max_length=3, null=True, blank=True)
    pai_hetero = models.CharField(max_length=10, null=True, blank=True)
    pai_homo = models.CharField(max_length=10, null=True, blank=True)

    mthfr_ng = models.CharField(max_length=3, null=True, blank=True)
    mthfr_hetero = models.CharField(max_length=3, null=True, blank=True)
    mthfr_homo = models.CharField(max_length=3, null=True, blank=True)

    abort = models.CharField(max_length=1, null=True, blank=True)

class PridaMutations2(models.Model):
    # id = models.PositiveSmallIntegerField(default=0, primary_key=1)
    code = models.CharField(max_length=20)
    # birth_year = models.PositiveIntegerField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    # fvl_ng = models.CharField(max_length=3, null=True, blank=True)
    fvl_hetero = models.CharField(max_length=3, null=True, blank=True)
    fvl_homo = models.CharField(max_length=3, null=True, blank=True)

    # prothr_ng = models.CharField(max_length=3, null=True, blank=True)
    prothr_hetero = models.CharField(max_length=3, null=True, blank=True)
    prothr_homo = models.CharField(max_length=3, null=True, blank=True)

    # pai_ng = models.CharField(max_length=3, null=True, blank=True)
    pai_hetero = models.CharField(max_length=10, null=True, blank=True)
    pai_homo = models.CharField(max_length=10, null=True, blank=True)

    # mthfr_ng = models.CharField(max_length=3, null=True, blank=True)
    mthfr_hetero = models.CharField(max_length=3, null=True, blank=True)
    mthfr_homo = models.CharField(max_length=3, null=True, blank=True)

    abort = models.CharField(max_length=1, null=True, blank=True)

class PridaControli(models.Model):
    # id = models.PositiveSmallIntegerField(default=0, primary_key=1)
    code = models.CharField(max_length=20)
    # birth_year = models.PositiveIntegerField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    fvl_ng = models.CharField(max_length=3, null=True, blank=True)
    fvl_hetero = models.CharField(max_length=3, null=True, blank=True)
    fvl_homo = models.CharField(max_length=3, null=True, blank=True)

    prothr_ng = models.CharField(max_length=3, null=True, blank=True)
    prothr_hetero = models.CharField(max_length=3, null=True, blank=True)
    prothr_homo = models.CharField(max_length=3, null=True, blank=True)

    pai_ng = models.CharField(max_length=3, null=True, blank=True)
    pai_hetero = models.CharField(max_length=10, null=True, blank=True)
    pai_homo = models.CharField(max_length=10, null=True, blank=True)

    mthfr_ng = models.CharField(max_length=3, null=True, blank=True)
    mthfr_hetero = models.CharField(max_length=3, null=True, blank=True)
    mthfr_homo = models.CharField(max_length=3, null=True, blank=True)

    abort = models.CharField(max_length=1, null=True, blank=True)

class Person(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    location = models.CharField(max_length=50, blank=True)