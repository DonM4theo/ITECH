from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Log
from django.contrib.auth.models import User
import pyodbc
import datetime
from .forms import PostForm_KTL, PostForm_PRO, EditForm, FilterForm, PostFormSelector, FilterForm_activity, PackDetails


# DB = "DBADAL"
# DB_SERVER = "GT166\SQLEXPRESS01"
# DB_USER = "sa"
# DB_PASSWORD = "xxxxxxx"
# DB_DRIVER = "{SQL Server Native Client 11.0}"


def get_logged(request):
    who_logged = request.session['_auth_user_id']
    who_logged = str(User.objects.get(id=who_logged))
    when_logged = request.session['_session_init_timestamp_']
    return who_logged, when_logged


def is_technolog(user):
    return user.is_superuser or user.groups.filter(name='technolog').exists()


def is_paczka_menago(user):
    return user.is_superuser or user.groups.filter(name='technolog') or user.groups.filter(name='paczka_menago').exists()


def index(request):
    return render(request, 'index.html', {"DB": DB, "DB_SERVER": DB_SERVER})


db_URL = (f"DRIVER={DB_DRIVER};"
          f"Server={DB_SERVER};"
          f"Database={DB};"
          f"UID={DB_USER};"
          f"PWD={DB_PASSWORD};"
          # "Trusted_Connection=yes;"
          )


@login_required
def select_all_program(request):
    try:
        conn = pyodbc.connect(db_URL)
        query = "select * from dbo.programy order by [NrPRM] asc"
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()

        return render(request, "select_all_program.html", {"result": result})
    except pyodbc.OperationalError:
        return HttpResponse("__Server MSSQL is not found or not accessible__")


@login_required
@user_passes_test(is_technolog)
def select_type(request):
    if request.method == "POST":
        pre_form = PostFormSelector(request.POST)
        if pre_form.is_valid():
            gc = pre_form.cleaned_data
            if gc.get('TypProgramu') == "PRO":
                return HttpResponseRedirect('/PRO_create')
            elif gc.get('TypProgramu') == "KTL":
                return HttpResponseRedirect('/KTL_create')
    else:
        form = PostFormSelector()
        return render(request, 'pre_create.html', {'form': form})


@login_required
@user_passes_test(is_technolog)
def create_KTL(request):
    if request.method == "POST":
        form = PostForm_KTL(request.POST)
        if form.is_valid():

            try:
                conn = pyodbc.connect(db_URL)
                cd = form.cleaned_data
                cursor = conn.cursor()
                try:
                    NazwaProgramu = (cd.get('NazwaProgramu')).upper()
                    ProKolor = cd.get('ProKolor')
                    if ProKolor == '':
                        ProKolor = None
                    cursor.execute("""INSERT INTO [dbo].[programy](
                    [NrPRM], [NazwaProgramu], [CzyProgPrior], [CzyNiepWsad], [CzyUltraM05], [CzyPolewaczka], [KtlPMC],
                    [SzerTraw], [Pow], [CzyOdmuch], [KtlNapPW], [KtlCzasNN], [KtlPRK], [KtlCzasWygrz], [FsfCzasSusz], [Gmp],
                    [CzyMask], [ProPMZad], [ProKolor], [ProCzyOtrzep], [ProCzasWygrz], [StRozZad], [CzyAktywny], [Czas_zal],
                    [Czas_roz])
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                   cd.get('NrPRM'), NazwaProgramu, cd.get('CzyProgPrior'), cd.get('CzyNiepWsad'),
                                   cd.get('CzyUltraM05'), cd.get('CzyPolewaczka'), cd.get('KtlPMC'), cd.get('SzerTraw'),
                                   cd.get('Pow'), cd.get('CzyOdmuch'), cd.get('KtlNapPW'), cd.get('KtlCzasNN'),
                                   cd.get('KtlPRK'), cd.get('KtlCzasWygrz'), cd.get('FsfCzasSusz'), cd.get('Gmp'),
                                   cd.get('CzyMask'), cd.get('ProPMZad'), ProKolor, cd.get('ProCzyOtrzep'),
                                   cd.get('ProCzasWygrz'), cd.get('StRozZad'), cd.get('CzyAktywny'), cd.get('Czas_zal'),
                                   cd.get('Czas_roz'))

                except pyodbc.IntegrityError:
                    return HttpResponse("__IntegrityError: duplicated record's attribute__")
                conn.commit()
                conn.close()
                print(request.user)
                user = request.user
                create_log(cd.get('NrPRM'), user)
                return HttpResponseRedirect("/")
            except pyodbc.OperationalError:
                return HttpResponse("__Server MSSQL is not found or not accessible__")
    else:
        data = {'NrPRM': last_NrPRM()}
        form = PostForm_KTL(initial=data)
    return render(request, 'KTL_create.html', {'form': form})


@login_required
@user_passes_test(is_technolog)
def create_PRO(request):
    if request.method == "POST":
        form = PostForm_PRO(request.POST)
        if form.is_valid():

            try:
                conn = pyodbc.connect(db_URL)
                cd = form.cleaned_data
                cursor = conn.cursor()
                print("LOOK AT THIS:", cd.get('Czas_zal'), cd.get('Czas_roz'))
                try:
                    NazwaProgramu = (cd.get('NazwaProgramu')).upper()
                    ProKolor = cd.get('ProKolor')
                    if ProKolor == '':
                        ProKolor = None
                    cursor.execute("""INSERT INTO [dbo].[programy](
                    [NrPRM], [NazwaProgramu], [CzyProgPrior], [CzyNiepWsad], [CzyUltraM05], [CzyPolewaczka], [KtlPMC],
                    [SzerTraw], [Pow], [CzyOdmuch], [KtlNapPW], [KtlCzasNN], [KtlPRK], [KtlCzasWygrz], [FsfCzasSusz], [Gmp],
                    [CzyMask], [ProPMZad], [ProKolor], [ProCzyOtrzep], [ProCzasWygrz], [StRozZad], [CzyAktywny], [Czas_zal],
                    [Czas_roz])
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                   cd.get('NrPRM'), NazwaProgramu, cd.get('CzyProgPrior'), cd.get('CzyNiepWsad'),
                                   cd.get('CzyUltraM05'), cd.get('CzyPolewaczka'), cd.get('KtlPMC'), cd.get('SzerTraw'),
                                   cd.get('Pow'), cd.get('CzyOdmuch'), cd.get('KtlNapPW'), cd.get('KtlCzasNN'),
                                   cd.get('KtlPRK'), cd.get('KtlCzasWygrz'), cd.get('FsfCzasSusz'), cd.get('Gmp'),
                                   cd.get('CzyMask'), cd.get('ProPMZad'), ProKolor, cd.get('ProCzyOtrzep'),
                                   cd.get('ProCzasWygrz'), cd.get('StRozZad'), cd.get('CzyAktywny'), cd.get('Czas_zal'),
                                   cd.get('Czas_roz'))

                except pyodbc.IntegrityError:
                    return HttpResponse("__IntegrityError: duplicated record's attribute__")
                conn.commit()
                conn.close()
                print(request.user)
                user = request.user
                create_log(cd.get('NrPRM'), user)
                return HttpResponseRedirect("/")
            except pyodbc.OperationalError:
                return HttpResponse("__Server MSSQL is not found or not accessible__")
    else:
        data = {'NrPRM': last_NrPRM()}
        form = PostForm_PRO(initial=data)
    return render(request, 'PRO_create.html', {'form': form})


@login_required
@user_passes_test(is_technolog)
def edit(request, idPRM):
    try:
        conn = pyodbc.connect(db_URL)
        query = f"""SELECT [idPRM], [NrPRM], [NazwaProgramu], [KodProgramu], [CzyProgPrior],
                        [CzyNiepWsad], [CzyUltraM05], [CzyPolewaczka], [KtlPMC], [SzerTraw],
                        [Pow], [CzyOdmuch], [KtlNapPW], [KtlCzasNN], [KtlPRK], [KtlCzasWygrz],
                        [FsfCzasSusz], [Gmp], [CzyMask], [ProPMZad], [ProKolor], [ProCzyOtrzep],
                        [ProCzasWygrz], [StRozZad], [CzyAktywny], [Czas_zal], [Czas_roz]
                        FROM [{DB}].[dbo].[programy] where [idPRM] = ?"""
        cursor = conn.cursor()
        cursor.execute(query, idPRM)
        result = cursor.fetchall()
        conn.close()
        data = {'ID': result[0][0], 'NrPRM': result[0][1], 'NazwaProgramu': result[0][2], 'KodProgramu': result[0][3],
                'CzyProgPrior': result[0][4], 'CzyNiepWsad': result[0][5], 'CzyUltraM05': result[0][6],
                'CzyPolewaczka': result[0][7], 'KtlPMC': result[0][8], 'SzerTraw': result[0][9], 'Pow': result[0][10],
                'CzyOdmuch': result[0][11], 'KtlNapPW': result[0][12], 'KtlCzasNN': result[0][13], 'KtlPRK': result[0][14],
                'KtlCzasWygrz': result[0][15], 'FsfCzasSusz': result[0][16], 'Gmp': result[0][17], 'CzyMask': result[0][18],
                'ProPMZad': result[0][19], 'ProKolor': result[0][20], 'ProCzyOtrzep': result[0][21],
                'ProCzasWygrz': result[0][22], 'StRozZad': result[0][23], 'CzyAktywny': result[0][24],
                'Czas_zal': result[0][25], 'Czas_roz': result[0][26]}

    except pyodbc.OperationalError:
        return HttpResponse("__Server MSSQL is not found or not accessible__")
    if request.method == "POST":
        form = EditForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            check_keys = (['NazwaProgramu', 'CzyProgPrior', 'CzyNiepWsad', 'CzyUltraM05', 'CzyPolewaczka', 'KtlPMC',
                           'SzerTraw', 'Pow', 'CzyOdmuch', 'KtlNapPW', 'KtlCzasNN', 'KtlPRK', 'KtlCzasWygrz',
                           'FsfCzasSusz', 'Gmp', 'CzyMask', 'ProPMZad', 'ProKolor', 'ProCzyOtrzep', 'ProCzasWygrz',
                           'StRozZad', 'CzyAktywny', 'Czas_zal', 'Czas_roz'])

            for key in check_keys:
                if data.get(key) != cd.get(key):
                    if cd.get(key) == '':
                        print("key:", key, "value:", cd.get(key))
                        continue
                    if key == 'NazwaProgramu':
                        cd.update({'NazwaProgramu': (cd.get(key)).upper()})
                    if isinstance(cd.get(key), str):
                        value = "'" + str(cd.get(key)) + "'"
                        query = "UPDATE [dbo].[programy] SET [" + key + "] = " + value + " WHERE [idPRM] = " + str(idPRM)
                        print("query1:", query)
                    else:
                        value = str(int(cd.get(key)))
                        query = "UPDATE [dbo].[programy] SET [" + key + "] = " + value + " WHERE [idPRM] = " + str(idPRM)
                        print("query2:", query)
                    try:
                        conn = pyodbc.connect(db_URL)
                        cursor = conn.cursor()
                        cursor.execute(query)
                        conn.commit()
                        conn.close()

                    except:
                        return HttpResponse("__Server MSSQL is not found or not accessible__")

            user = request.user
            create_log(result[0][1], user)
        return HttpResponseRedirect("/select")

    else:

        form = EditForm(initial=data)

    return render(request, "edit.html", {'form': form, 'result': result})


def last_NrPRM():
    try:
        conn = pyodbc.connect(db_URL)
        query = f"SELECT TOP (1) [NrPRM] FROM [{DB}].[dbo].[programy] order by [NrPRM] desc"
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
    except pyodbc.OperationalError:
        return HttpResponse("__Server MSSQL is not found or not accessible__")
    return str(result[0] + 1)


def create_log(NrPRM, user):
    try:
        conn = pyodbc.connect(db_URL)
        query = f"""SELECT [idPRM], [NrPRM], [NazwaProgramu], [KodProgramu], [CzyProgPrior],
                        [CzyNiepWsad], [CzyUltraM05], [CzyPolewaczka], [KtlPMC], [SzerTraw],
                        [Pow], [CzyOdmuch], [KtlNapPW], [KtlCzasNN], [KtlPRK], [KtlCzasWygrz],
                        [FsfCzasSusz], [Gmp], [CzyMask], [ProPMZad], [ProKolor], [ProCzyOtrzep],
                        [ProCzasWygrz], [StRozZad], [CzyAktywny], [Czas_zal], [Czas_roz], [DataMod]
                        FROM [{DB}].[dbo].[programy] where [NrPRM] = ?"""
        cursor = conn.cursor()
        cursor.execute(query, NrPRM)
        result = cursor.fetchall()
        conn.close()
        log = Log()

        log.idPRM = result[0][0]
        log.NrPRM = result[0][1]
        log.NazwaProgramu = result[0][2]
        log.KodProgramu = result[0][3]
        log.CzyProgPrior = result[0][4]
        log.CzyNiepWsad = result[0][5]
        log.CzyUltraM05 = result[0][6]
        log.CzyPolewaczka = result[0][7]
        log.KtlPMC = result[0][8]
        log.SzerTraw = result[0][9]
        log.Pow = result[0][10]
        log.CzyOdmuch = result[0][11]
        log.KtlNapPW = result[0][12]
        log.KtlCzasNN = result[0][13]
        log.KtlPRK = result[0][14]
        log.KtlCzasWygrz = result[0][15]
        log.FsfCzasSusz = result[0][16]
        log.Gmp = result[0][17]
        log.CzyMask = result[0][18]
        log.ProPMZad = result[0][19]
        log.ProKolor = result[0][20]
        log.ProCzyOtrzep = result[0][21]
        log.ProCzasWygrz = result[0][22]
        log.StRozZad = result[0][23]
        log.CzyAktywny = result[0][24]
        log.Czas_zal = result[0][25]
        log.Czas_roz = result[0][26]
        log.DataMod = result[0][27]
        log.author = user
        print("LOGI z inserta", log)
        log.save()

    except pyodbc.OperationalError:
        return HttpResponse("__Server MSSQL is not found or not accessible__")


@login_required
@user_passes_test(is_technolog)
def show_log(request):
    if request.method == "GET":
        form = FilterForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            # s = [log.author for log in Log.objects.all()]
            # z = Log(Log.author)
            # print("CZEJ TO:", s, z)
            if type(cd.get('NrPRM')) == int and cd.get('Author') != '':
                logs = Log.objects.filter(NrPRM=cd.get('NrPRM'),
                                          author=User.objects.get(username=cd.get('Author')).pk)
                return render(request, "logs.html", {'logs': logs, 'form': form})
            elif type(cd.get('NrPRM')) == int and cd.get('Author') == '':
                logs = Log.objects.filter(NrPRM=cd.get('NrPRM'))
                return render(request, "logs.html", {'logs': logs, 'form': form})
            elif type(cd.get('NrPRM')) != int and cd.get('Author') != '':
                logs = Log.objects.filter(author=User.objects.get(username=cd.get('Author')).pk)
                return render(request, "logs.html", {'logs': logs, 'form': form})
    else:

        form = FilterForm()
    logs = Log.objects.all()
    return render(request, "logs.html", {'logs': logs, 'form': form})


def get_production_activity(dt_in, dt_out, NrPRM=None, DeltaTime=None):
    delta = '(cast(datediff(second,CAST(CzasPrzebZad AS time),CAST(Czas_przebyw AS time)) as decimal)) as Exceeding_Time'
    delta_val = '(cast(datediff(second,CAST(CzasPrzebZad AS time),CAST(Czas_przebyw AS time)) as decimal))'
    if type(NrPRM) != int and type(DeltaTime) != int:
        query = f"""SELECT [NR_belki], [NrTrawersy], [Data_Wejscia], [Data_Wyj], [CzasPrzebZad],
                    [Czas_przebyw], {delta}, [NazwaObszaru], [KodObszaru], [NumerProgramu], [NazwaProgramu], [KtlPmc],
                    [KtlNapPW], [KtlNap]
                FROM [{DB}].[dbo].[Proc_View_01] where [Data_Wejscia] >= '{dt_in}' and [Data_Wejscia] <= '{dt_out}'"""

    elif type(NrPRM) != int and type(DeltaTime) == int:
        query = f"""SELECT [NR_belki], [NrTrawersy], [Data_Wejscia], [Data_Wyj], [CzasPrzebZad],
                    [Czas_przebyw], {delta}, [NazwaObszaru], [KodObszaru], [NumerProgramu], [NazwaProgramu], [KtlPmc],
                    [KtlNapPW], [KtlNap]
                FROM [{DB}].[dbo].[Proc_View_01] where [Data_Wejscia] >= '{dt_in}' and [Data_Wejscia] <= '{dt_out}' 
                    and {delta_val} >= {DeltaTime}"""

    elif type(NrPRM) == int and type(DeltaTime) != int:
        query = f"""SELECT [NR_belki], [NrTrawersy], [Data_Wejscia], [Data_Wyj], [CzasPrzebZad],
                    [Czas_przebyw], {delta}, [NazwaObszaru], [KodObszaru], [NumerProgramu], [NazwaProgramu], [KtlPmc],
                    [KtlNapPW], [KtlNap]
                FROM [{DB}].[dbo].[Proc_View_01] where [Data_Wejscia] >= '{dt_in}' and [Data_Wejscia] <= '{dt_out}' 
                    and [NumerProgramu] = {NrPRM}"""

    elif type(NrPRM) == int and type(DeltaTime) == int:
        query = f"""SELECT [NR_belki], [NrTrawersy], [Data_Wejscia], [Data_Wyj], [CzasPrzebZad],
                    [Czas_przebyw], {delta}, [NazwaObszaru], [KodObszaru], [NumerProgramu], [NazwaProgramu], [KtlPmc],
                    [KtlNapPW], [KtlNap]
                FROM [{DB}].[dbo].[Proc_View_01] where [Data_Wejscia] >= '{dt_in}' and [Data_Wejscia] <= '{dt_out}' 
                    and [NumerProgramu] = {NrPRM} and {delta_val} >= {DeltaTime}"""

    conn = pyodbc.connect(db_URL)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()

    return result


@login_required
def show_production_activity(request):

    today = datetime.date.today()
    now = datetime.datetime.now()
    timeH = now.strftime("%H")
    today = today.strftime('%Y-%m-%d')
    if 6 <= int(timeH) < 14:
        current_dt_in = today + ' 06:00:00'
        current_dt_out = today + ' 13:59:59'
        shift_d = 1
    elif 14 <= int(timeH) < 22:
        current_dt_in = today + ' 14:00:00'
        current_dt_out = today + ' 21:59:59'
        shift_d = 2
    else:
        current_dt_in = today + ' 22:00:00'
        current_dt_out = today + ' 05:59:59'
        shift_d = 3

    today_view = datetime.date.today().strftime('%Y-%m-%d')
    try:
        result = get_production_activity(current_dt_in, current_dt_out)

    except pyodbc.OperationalError:
        return HttpResponse("__Server MSSQL is not found or not accessible__")
    if request.method == "GET":
        form = FilterForm_activity(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            dt_view = cd.get('Date').strftime('%Y-%m-%d')
            dt_1plus = str(dt_view).split('-')
            dt_1plus = (datetime.date(int(dt_1plus[0]), int(dt_1plus[1]), int(dt_1plus[2])))
            dt = dt_1plus.strftime('%Y-%m-%d')
            dt_1plus = dt_1plus + datetime.timedelta(1)

            dt_1plus = dt_1plus.strftime('%Y-%m-%d')
            shift = int(cd.get('Shift'))
            NrPRM = cd.get('NrPRM')
            DeltaTime = cd.get('DeltaTime')
            print("exceed_time", DeltaTime)
            if shift == 1:
                dt_in = dt + ' 06:00'
                dt_out = dt + ' 13:59'
                result = get_production_activity(dt_in, dt_out, NrPRM, DeltaTime)
            elif shift == 2:
                dt_in = dt + ' 14:00'
                dt_out = dt + ' 21:59'
                result = get_production_activity(dt_in, dt_out, NrPRM, DeltaTime)
            elif shift == 3:
                dt_in = dt + ' 22:00'
                dt_out = dt_1plus + ' 05:59'
                result = get_production_activity(dt_in, dt_out, NrPRM, DeltaTime)
            data = {
                'Date': dt_view,
                'Shift': shift,
                'NrPRM': NrPRM,
                'DeltaTime': DeltaTime,
            }
            form = FilterForm_activity(initial=data)
            return render(request, 'line_activity.html', {'form': form, 'result': result})

        else:
            data = {
                'Date': today_view,
                'Shift': shift_d
            }
            form = FilterForm_activity(initial=data)
        return render(request, 'line_activity.html', {'form': form, 'result': result})


@login_required
@user_passes_test(is_paczka_menago)
def show_pack_detail(request):
    try:
        conn = pyodbc.connect(db_URL)
        query = """SELECT pd.NrPRM, pr.NazwaProgramu, pd.IleDetaliBelka, pd.IleDetaliPojemnik, pd.IleZawieszekBelka, pd.DataMod
                    FROM dbo.packdetail as pd, dbo.programy as pr WHERE pd.NrPRM = pr.NrPRM"""
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()

        return render(request, "show_pack_detail.html", {"result": result})
    except pyodbc.OperationalError:
        return HttpResponse("__Server MSSQL is not found or not accessible__")


@login_required
@user_passes_test(is_paczka_menago)
def edit_pack_detail(request, NrPRM):
    try:
        conn = pyodbc.connect(db_URL)
        query = """SELECT pd.NrPRM, pr.NazwaProgramu, pd.IleDetaliBelka, pd.IleDetaliPojemnik, pd.IleZawieszekBelka, pd.DataMod
                    FROM dbo.packdetail as pd, dbo.programy as pr WHERE pd.NrPRM = pr.NrPRM and pd.NrPRM = ?"""
        query_of_unique = """SELECT NrPRM FROM dbo.packdetail"""
        cursor = conn.cursor()
        cursor.execute(query, NrPRM)
        result = cursor.fetchall()
        cursor.execute(query_of_unique)
        list_existed_nrprm = cursor.fetchall()
        conn.close()
        data = {'NrPRM': result[0][0], 'NazwaProgramu': result[0][1], 'IleDetaliBelka': result[0][2],
                'IleDetaliPojemnik': result[0][3], 'IleZawieszekBelka': result[0][4]}
        existed_details = []
        for record in list_existed_nrprm:
            existed_details.append(record[0])

    except pyodbc.OperationalError:
        return HttpResponse("__Server MSSQL is not found or not accessible__")
    if request.method == "POST":
        form = PackDetails(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            check_keys = (['NrPRM', 'NazwaProgramu', 'IleDetaliBelka', 'IleDetaliPojemnik', 'IleZawieszekBelka'])

            for key in check_keys:
                if data.get(key) != cd.get(key):
                    if key == 'NrPRM':
                        value = cd.get(key)
                        if value in existed_details:
                            print(value, "czy istnieje w:", existed_details)
                            return HttpResponse("__Record for this NrPRM exists already__")
                        else:
                            value = str(int(cd.get(key)))
                            query = "UPDATE dbo.packdetail SET [" + key + "] = " + value + " WHERE [NrPRM] = " + str(NrPRM)
                            print("edit_query:", query)
                    try:
                        conn = pyodbc.connect(db_URL)
                        cursor = conn.cursor()
                        cursor.execute(query)
                        conn.commit()
                        conn.close()

                    except:
                        return HttpResponse("__Server MSSQL is not found or not accessible__")

        return HttpResponseRedirect("/show_pack_detail")

    else:

        form = PackDetails(initial=data)

    return render(request, "edit_pack_detail.html", {'form': form, 'result': result})


@login_required
@user_passes_test(is_paczka_menago)
def delete_pack_detail(request, NrPRM):
    query = """DELETE FROM dbo.packdetail WHERE NrPRM = ?"""
    try:
        conn = pyodbc.connect(db_URL)
        cursor = conn.cursor()
        cursor.execute(query, NrPRM)
        conn.commit()
        conn.close()

    except:
        return HttpResponse("__Server MSSQL is not found or not accessible__")

    return HttpResponseRedirect("/show_pack_detail")


existed_details = []


def check_NrPRM_in_details():
    try:
        conn = pyodbc.connect(db_URL)
        query_of_unique = """SELECT NrPRM FROM dbo.packdetail"""
        cursor = conn.cursor()
        cursor.execute(query_of_unique)
        list_existed_nrprm = cursor.fetchall()
        conn.close()

        for record in list_existed_nrprm:
            existed_details.append(int(record[0]))

    except pyodbc.OperationalError:
        return HttpResponse("__Server MSSQL is not found or not accessible__")


@login_required
@user_passes_test(is_paczka_menago)
def add_pack_detail(request):
    check_NrPRM_in_details()
    if request.method == 'POST':
        NrPRM = request.POST["NrPRM_f"]
        IleDetaliBelka = request.POST["IleDetaliBelka_f"]
        IleDetaliPojemnik = request.POST["IleDetaliPojemnik_f"]
        IleZawieszekBelka = request.POST["IleZawieszekBelka_f"]

        print("NrPRM taki:", NrPRM, "szukam w:", existed_details)
        if int(NrPRM) in existed_details:
            return HttpResponse("__Record for this NrPRM exists already__")
        else:
            try:
                conn = pyodbc.connect(db_URL)
                query = f"""INSERT INTO dbo.packdetail
                                    ([NrPRM], [IleDetaliBelka] ,[IleDetaliPojemnik], [IleZawieszekBelka]) VALUES
                                    ({NrPRM}, {IleDetaliBelka}, {IleDetaliPojemnik}, {IleZawieszekBelka})"""
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                conn.close()
            except:
                return HttpResponse("__Server MSSQL is not found or not accessible__")

    return HttpResponseRedirect("/show_pack_detail")

