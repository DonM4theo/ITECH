from django import forms

# It's a dictionaries space:

type_dict = (
    ("KTL", "KTL"),
    ("PRO", "FSF+PRO"),
)
KtlPMC_dict = (
    (None, '--brak--'),
    (1, 1),
    (2, 2),
    (3, 3),
    (6, 6),
)
KtlPMCPRO_dict = (
    (None, '--brak--'),
    (4, 4),
)
KtlPMCFULL_dict = (
    (None, '--brak--'),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (6, 6),
)
SzerTraw_dict = (
    (None, '--brak--'),
    (300, 300),
    (600, 600),
    (1200, 1200),
)
Gmp_dict = (
    (None, '--brak--'),
    (0, 0),
    (1, 1),
    (2, 2),
)
CzyMask_dict = (
    (None, '--brak--'),
    (0, 0),
    (1, 1),
)
StRozZad_dict = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
)


class PostFormSelector(forms.Form):
    TypProgramu = forms.ChoiceField(label='Program type', choices=type_dict)


class PostForm_KTL(forms.Form):
    NrPRM = forms.IntegerField(label='NrPRM', min_value=0)
    NazwaProgramu = forms.CharField(label='NazwaProgramu', max_length=50)
    CzyProgPrior = forms.BooleanField(label='CzyProgPrior', initial=False, required=False)
    CzyNiepWsad = forms.BooleanField(label='CzyNiepWsad', initial=False, required=False)
    CzyUltraM05 = forms.BooleanField(label='CzyUltraM05', initial=False, required=False)
    CzyPolewaczka = forms.BooleanField(label='CzyPolewaczka', initial=False, required=False)
    KtlPMC = forms.ChoiceField(choices=KtlPMC_dict, label='KtlPMC')
    SzerTraw = forms.ChoiceField(choices=SzerTraw_dict, label='SzerTraw')
    Pow = forms.IntegerField(label='Pow', max_value=10000, min_value=0)
    CzyOdmuch = forms.IntegerField(label='CzasOdmuch[s]', initial=60, max_value=200, min_value=0)
    KtlNapPW = forms.IntegerField(label='KtlNapPW', max_value=500, min_value=0)
    KtlCzasNN = forms.IntegerField(label='KtlCzasNN[s]', initial=30, max_value=300, min_value=0)
    KtlPRK = forms.IntegerField(label='KtlPRK', initial=0, max_value=99, min_value=0)
    KtlCzasWygrz = forms.IntegerField(label='KtlCzasWygrz[min]', initial=30, max_value=60, min_value=0)
    FsfCzasSusz = forms.IntegerField(label='FsfCzasSusz[min]', required=False, max_value=30, min_value=0)
    Gmp = forms.ChoiceField(choices=Gmp_dict, label='Gmp')
    CzyMask = forms.ChoiceField(choices=CzyMask_dict, label='CzyMask', required=False)
    ProPMZad = forms.IntegerField(label='ProPMZad', required=False, max_value=99, min_value=0)
    ProKolor = forms.CharField(label='ProKolor', max_length=50, required=False)
    ProCzyOtrzep = forms.BooleanField(label='ProCzyOtrzep', required=False, initial=False)
    ProCzasWygrz = forms.IntegerField(label='ProCzasWygrz[min]', required=False, max_value=80, min_value=0)
    StRozZad = forms.ChoiceField(choices=StRozZad_dict, label='StRozZad', initial=0)
    CzyAktywny = forms.BooleanField(label='CzyAktywny', required=False, initial=1)
    Czas_zal = forms.IntegerField(label='Czas_zal[s]', initial=150, max_value=999, min_value=0)
    Czas_roz = forms.IntegerField(label='Czas_roz[s]', initial=150, max_value=999, min_value=0)


class PostForm_PRO(forms.Form):
    NrPRM = forms.IntegerField(label='NrPRM', min_value=0)
    NazwaProgramu = forms.CharField(label='NazwaProgramu', max_length=50)
    CzyProgPrior = forms.BooleanField(label='CzyProgPrior', initial=False, required=False)
    CzyNiepWsad = forms.BooleanField(label='CzyNiepWsad', initial=False, required=False)
    CzyUltraM05 = forms.BooleanField(label='CzyUltraM05', initial=False, required=False)
    CzyPolewaczka = forms.BooleanField(label='CzyPolewaczka', initial=False, required=False)
    KtlPMC = forms.ChoiceField(choices=KtlPMCPRO_dict, label='KtlPMC')
    SzerTraw = forms.ChoiceField(choices=SzerTraw_dict, label='SzerTraw')
    Pow = forms.IntegerField(label='Pow', max_value=10000, min_value=0)
    CzyOdmuch = forms.IntegerField(label='CzasOdmuch[s]', initial=60, max_value=200, min_value=0)
    KtlNapPW = forms.IntegerField(label='KtlNapPW', max_value=500, required=False, disabled=True, min_value=0)
    KtlCzasNN = forms.IntegerField(label='KtlCzasNN', initial=30, max_value=60, required=False, disabled=True, min_value=0)
    KtlPRK = forms.IntegerField(label='KtlPRK', initial=0, max_value=99, required=False, disabled=True, min_value=0)
    KtlCzasWygrz = forms.IntegerField(label='KtlCzasWygrz[min]', initial=30, max_value=60, required=False, disabled=True,
                                      min_value=0)
    FsfCzasSusz = forms.IntegerField(label='FsfCzasSusz[min]', max_value=30, initial=20, min_value=0)
    Gmp = forms.ChoiceField(choices=Gmp_dict, label='Gmp')
    CzyMask = forms.ChoiceField(choices=CzyMask_dict, label='CzyMask')
    ProPMZad = forms.IntegerField(label='ProPMZad', required=False, max_value=99, min_value=0)
    ProKolor = forms.CharField(label='ProKolor', max_length=50, required=False)
    ProCzyOtrzep = forms.BooleanField(label='ProCzyOtrzep', required=False, initial=False)
    ProCzasWygrz = forms.IntegerField(label='ProCzasWygrz[min]', max_value=80, min_value=0)
    StRozZad = forms.ChoiceField(choices=StRozZad_dict, label='StRozZad', initial=1)
    CzyAktywny = forms.BooleanField(label='CzyAktywny', required=False, initial=1)
    Czas_zal = forms.IntegerField(label='Czas_zal[s]', max_value=999, initial=150, min_value=0)
    Czas_roz = forms.IntegerField(label='Czas_roz[s]', max_value=999, initial=150, min_value=0)


class EditForm(forms.Form):
    NrPRM = forms.IntegerField(label='NrPRM', required=False, disabled=True, min_value=0)
    NazwaProgramu = forms.CharField(label='NazwaProgramu', max_length=50)
    KodProgramu = forms.CharField(label='KodProgramu', required=False, disabled=True)
    CzyProgPrior = forms.BooleanField(label='CzyProgPrior', required=False)
    CzyNiepWsad = forms.BooleanField(label='CzyNiepWsad', required=False)
    CzyUltraM05 = forms.BooleanField(label='CzyUltraM05', required=False)
    CzyPolewaczka = forms.BooleanField(label='CzyPolewaczka', required=False)
    KtlPMC = forms.ChoiceField(choices=KtlPMCFULL_dict, label='KtlPMC')
    SzerTraw = forms.ChoiceField(choices=SzerTraw_dict, label='SzerTraw')
    Pow = forms.IntegerField(label='Pow', max_value=10000, min_value=0)
    CzyOdmuch = forms.IntegerField(label='CzasOdmuch[s]', max_value=200, min_value=0)
    KtlNapPW = forms.IntegerField(label='KtlNapPW', max_value=500, required=False, min_value=0)
    KtlCzasNN = forms.IntegerField(label='KtlCzasNN', max_value=300, required=False, min_value=0)
    KtlPRK = forms.IntegerField(label='KtlPRK', max_value=99, required=False, min_value=0)
    KtlCzasWygrz = forms.IntegerField(label='KtlCzasWygrz', max_value=60, required=False, min_value=0)
    FsfCzasSusz = forms.IntegerField(label='FsfCzasSusz', required=False, max_value=30, min_value=0)
    Gmp = forms.ChoiceField(choices=Gmp_dict, label='Gmp', required=False)
    CzyMask = forms.ChoiceField(choices=CzyMask_dict, label='CzyMask', required=False)
    ProPMZad = forms.IntegerField(label='ProPMZad', required=False, max_value=99, min_value=0)
    ProKolor = forms.CharField(label='ProKolor', max_length=50, required=False)
    ProCzyOtrzep = forms.BooleanField(label='ProCzyOtrzep', required=False)
    ProCzasWygrz = forms.IntegerField(label='ProCzasWygrz', required=False, max_value=80, min_value=0)
    StRozZad = forms.ChoiceField(choices=StRozZad_dict, label='StRozZad')
    CzyAktywny = forms.BooleanField(label='CzyAktywny', required=False)
    Czas_zal = forms.IntegerField(label='Czas_zal[s]', max_value=999, min_value=0)
    Czas_roz = forms.IntegerField(label='Czas_roz[s]', max_value=999, min_value=0)


sort_dict = (
    ("desc", "od najnowszych"),
    ("asc", "od najstarszych"),
)


class FilterForm(forms.Form):
    NrPRM = forms.IntegerField(label='NrPRM', required=False, min_value=0)
    Author = forms.CharField(label='Author', max_length=8, required=False)


Shift_dict = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
)

class FilterForm_activity(forms.Form):
    Date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    Shift = forms.ChoiceField(choices=Shift_dict, label='Shift')
    NrPRM = forms.IntegerField(label='NrPRM', required=False, min_value=0)
    DeltaTime = forms.IntegerField(label='DeltaTime', required=False)


class PackDetails(forms.Form):
    NrPRM = forms.IntegerField(label='NrPRM', min_value=0)
    NazwaProgramu = forms.CharField(label='NazwaProgramu', required=False, disabled=True)
    IleDetaliBelka = forms.IntegerField(label='NrPRM', min_value=1)
    IleDetaliPojemnik = forms.IntegerField(label='IleDetaliPojemnik', min_value=1)
    IleZawieszekBelka = forms.IntegerField(label='IleZawieszekBelka', min_value=1)
