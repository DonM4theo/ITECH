from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Log(models.Model):
    idPRM = models.IntegerField(null=True)
    NrPRM = models.SmallIntegerField(null=True)
    NazwaProgramu = models.CharField(max_length=50, null=True)
    KodProgramu = models.CharField(max_length=15, null=True)
    CzyProgPrior = models.BooleanField()
    CzyNiepWsad = models.BooleanField()
    CzyUltraM05 = models.BooleanField()
    CzyPolewaczka = models.BooleanField()
    KtlPMC = models.SmallIntegerField()
    SzerTraw = models.SmallIntegerField()
    Pow = models.SmallIntegerField(null=True)
    CzyOdmuch = models.SmallIntegerField()
    KtlNapPW = models.SmallIntegerField(null=True)
    KtlCzasNN = models.SmallIntegerField(null=True)
    KtlPRK = models.SmallIntegerField()
    KtlCzasWygrz = models.SmallIntegerField(null=True)
    FsfCzasSusz = models.SmallIntegerField(null=True)
    Gmp = models.SmallIntegerField(null=True)
    CzyMask = models.SmallIntegerField(null=True)
    ProPMZad = models.SmallIntegerField(null=True)
    ProKolor = models.CharField(max_length=50, null=True)
    ProCzyOtrzep = models.BooleanField(null=True)
    ProCzasWygrz = models.SmallIntegerField(null=True)
    StRozZad = models.SmallIntegerField()
    CzyAktywny = models.BooleanField()
    Czas_zal = models.IntegerField(null=True)
    Czas_roz = models.IntegerField(null=True)
    DataMod = models.DateTimeField(null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    data_log = models.DateTimeField(null=True, auto_now_add=True)

    def publish(self):
        self.data_log = timezone.now()
        self.save()

    def __str__(self):
        return str(self.NrPRM) + " -- " + str(self.data_log) + " -- " + str(self.author)


# Model to store the list of logged in users


class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete=models.CASCADE)
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username
