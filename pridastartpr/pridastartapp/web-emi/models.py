from django.db import models

class Patient(models.Model):

    name = models.CharField(max_length=100)
    maternal_age = models.IntegerField()
    systolic_blood_pressure = models.DecimalField(max_digits=5, decimal_places=2)
    diastolic_blood_pressure = models.DecimalField(max_digits=5, decimal_places=2)
    gestational_week = models.DecimalField(max_digits=4, decimal_places=1)
    newborn_weight = models.IntegerField()
    eai1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    nea1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    eai2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    nea2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    erythrocytes = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    hemoglobin = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    hematocrit = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    mcv = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    mch = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    mchc = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rdw = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    prothrombin_time_sec = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    prothrombin_time_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    prothrombin_time_inr = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    platelets = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    mpv = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pdw = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    creatinine = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    total_protein = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    albumin = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fibrinogen = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    crp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    proteinuria = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    asat = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    alat = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    factor_v_leiden = models.CharField(max_length=50, blank=True, null=True)
    factor_ii_mutation = models.CharField(max_length=50, blank=True, null=True)
    pai = models.CharField(max_length=50, blank=True, null=True)
    mthfr = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
    

#Pregnant Controls
class Control(models.Model):

   
    name = models.CharField(max_length=100)
    maternal_age = models.IntegerField()
    systolic_blood_pressure = models.DecimalField(max_digits=5, decimal_places=2)
    diastolic_blood_pressure = models.DecimalField(max_digits=5, decimal_places=2)
    gestational_week = models.DecimalField(max_digits=4, decimal_places=1)
    newborn_weight = models.IntegerField()
    eai1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    nea1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    eai2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    nea2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    erythrocytes = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    hemoglobin = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    hematocrit = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    mcv = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    mch = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    mchc = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rdw = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    prothrombin_time_sec = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    prothrombin_time_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    prothrombin_time_inr = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    platelets = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    mpv = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pdw = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    creatinine = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    total_protein = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    albumin = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fibrinogen = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    crp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    proteinuria = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    asat = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    alat = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    factor_v_leiden = models.CharField(max_length=50, blank=True, null=True)
    factor_ii_mutation = models.CharField(max_length=50, blank=True, null=True)
    pai = models.CharField(max_length=50, blank=True, null=True)
    mthfr = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

#spontanetous abortion


class Abortion(models.Model):
    no = models.CharField(max_length=50, verbose_name="No", blank=True, null=True)
    code = models.CharField(max_length=50, verbose_name="Код")
    year = models.PositiveIntegerField(verbose_name="Година")
    number = models.PositiveIntegerField(verbose_name="Номер")
    age = models.PositiveIntegerField(verbose_name="Възраст")
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Мъж'), ('Female', 'Жена')],
        verbose_name="Пол"
    )

    # Other fields redefined with 0, 1, or empty
    factor_v_normal = models.IntegerField(
        choices=[
            (0, '0'),
            (1, '1'),
        ],
        blank=True,
        null=True,
        verbose_name="Factor V Leiden Normal Genotype"
    )
    factor_v_heterozygous = models.IntegerField(
        choices=[
            (0, '0'),
            (1, '1'),
        ],
        blank=True,
        null=True,
        verbose_name="Heterozygous Factor V Leiden Mutation"
    )
    factor_v_homozygous = models.IntegerField(
        choices=[
            (0, '0'),
            (1, '1'),
        ],
        blank=True,
        null=True,
        verbose_name="Homozygous Factor V Leiden Mutation"
    )
    factor_ii_normal = models.IntegerField(
        choices=[
            (0, '0'),
            (1, '1'),
        ],
        blank=True,
        null=True,
        verbose_name="Factor II (Prothrombin) - Normal Genotype"
    )
    factor_ii_heterozygous = models.IntegerField(
        choices=[
            (0, '0'),
            (1, '1'),
        ],
        blank=True,
        null=True,
        verbose_name="Factor II (Prothrombin) - Heterozygous Mutation"
    )
    factor_ii_homozygous = models.IntegerField(
        choices=[
            (0, '0'),
            (1, '1'),
        ],
        blank=True,
        null=True,
        verbose_name="Factor II (Prothrombin) - Homozygous Mutation"
    )
    pai1_normal = models.IntegerField(
        choices=[
            (0, '0'),
            (1, '1'),
        ],
        blank=True,
        null=True,
        verbose_name="PAI-1 Normal Genotype"
    )
    pai1_heterozygous = models.IntegerField(
        choices=[
            (0, '0'),
            (1, '1'),
        ],
        blank=True,
        null=True,
        verbose_name="PAI-1 Heterozygous Mutation"
    )
    pai1_homozygous = models.IntegerField(
        choices=[
            (0, '0'),
            (1, '1'),
        ],
        blank=True,
        null=True,
        verbose_name="PAI-1 Homozygous Mutation"
    )
    mthfr_normal = models.IntegerField(
        choices=[
            (0, '0'),
            (1, '1'),
        ],
        blank=True,
        null=True,
        verbose_name="MTHFR Normal Genotype"
    )
    mthfr_heterozygous = models.IntegerField(
        choices=[
            (0, '0'),
            (1, '1'),
        ],
        blank=True,
        null=True,
        verbose_name="MTHFR Heterozygous Mutation"
    )
    mthfr_homozygous = models.IntegerField(
        choices=[
            (0, '0'),
            (1, '1'),
        ],
        blank=True,
        null=True,
        verbose_name="MTHFR Homozygous Mutation"
    )

    def __str__(self):
        return f"{self.no} - {self.code} - {self.year}"
