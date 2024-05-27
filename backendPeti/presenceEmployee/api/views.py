from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from presenceEmployee.utils.utils import last_digit, parseHour, parseMinute, parseToHour, median, formula_sum_actual, fix_hour
from calendarDash.models import CalendarDashHRD
from presenceEmployee.models import PresenceEmployee
from userapp.utils.modelfunction import create_log
from .serializers import PresenceEmployeeSerializers, PresenceEmployeeAnalisisSerializers
from django.db.models import Count, Q, Sum, F, Avg
from userapp.models import User
from rest_framework.pagination import LimitOffsetPagination
from django.db.models.functions import TruncMonth
from datetime import timedelta, datetime
import calendar
from collections import Counter

class PresenceAPIView(APIView):
    serializer_class = PresenceEmployeeSerializers
 
    def get_queryset(self):
        presens = PresenceEmployee.objects.all().order_by('-id')
        return presens

class PresenceAPIViewID(viewsets.ModelViewSet):
    serializer_class = PresenceEmployeeSerializers
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        users = self.request.user
        if(users.roles == "hrd"):
            querySet = PresenceEmployee.objects.all().order_by('-id')
        else:
            querySet = PresenceEmployee.objects.all().filter(employee=users.pk).order_by('-id')
        employee = self.request.query_params.get('employee', None)
        working_date = self.request.query_params.get('working_date', None)
        months = self.request.query_params.get('months', None)
        years = self.request.query_params.get('years', None)

        if employee:
            querySet=querySet.filter(employee__name__icontains=employee)
        if years:
            querySet=querySet.filter(years=years)
        if months:
            querySet=querySet.filter(months=months)
        if working_date:
            querySet=querySet.filter(working_date=working_date)

        # serializer = PresenceEmployeeSerializers(querySet)

        # return serializer.data
        return querySet
    
    def get_id(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
                presences = PresenceEmployee.objects(id=ids)
                serializer = PresenceEmployeeSerializers(presences)
        else:
            pett = self.get_queryset()
            serr = PresenceEmployeeSerializers(pett, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        presen = request.data
        wrkdt = presen.get("working_date")
        strfrom = presen.get("start_from")
        lmbrstr = presen.get("lembur_start")
        employee = User.objects.get(id=presen["employee"])
        date = datetime.strptime(wrkdt, '%Y-%m-%d').date()

        if PresenceEmployee.objects.filter(Q(employee=employee) & Q(working_date=wrkdt)).exists():
            res = Response({"message" : "Sudah ada data absensi yang sama"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if(wrkdt != None):
                if(strfrom and lmbrstr != None):
                    new_presen = PresenceEmployee.objects.create(employee=User.objects.get(id=presen["employee"]), working_date=date,
                                                                end_from=int(presen["end_from"]), start_from=int(presen["start_from"]), lembur_start=int(presen["lembur_start"]), 
                                                                lembur_end=int(presen["lembur_end"]),  ket=presen["ket"]
                                                                )
                    create_log(action="create", message=f"Presensi {employee.name} tanggal {date} dibuat oleh {request.user.name}")
                    serializer = PresenceEmployeeSerializers(new_presen)
                    response_message={"message" : "Berhasil membuat data",
                                        "data": serializer.data
                        }
                    new_presen.save()
                    res = Response(response_message)
                elif(strfrom != None):
                    new_presen = PresenceEmployee.objects.create(employee=User.objects.get(id=presen["employee"]), working_date=date,
                                                                end_from=int(presen["end_from"]), start_from=int(presen["start_from"]),  ket=presen["ket"]
                                                                )
                    create_log(action="create", message=f"Presensi {employee.name} tanggal {date} dibuat oleh {request.user.name}")
                    serializer = PresenceEmployeeSerializers(new_presen)
                    response_message={"message" : "Berhasil membuat data",
                                        "data": serializer.data
                        }
                    new_presen.save()
                    res = Response(response_message)
                elif(lmbrstr != None):
                    new_presen = PresenceEmployee.objects.create(employee=User.objects.get(id=presen["employee"]), working_date=date,
                                                                lembur_start=int(presen["lembur_start"]), lembur_end=int(presen["lembur_end"]),  ket=presen["ket"]
                                                                )
                    create_log(action="create", message=f"Presensi {employee.name} tanggal {date} dibuat oleh {request.user.name}")
                    serializer = PresenceEmployeeSerializers(new_presen)
                    response_message={"message" : "Berhasil membuat data",
                                        "data": serializer.data
                        }
                    new_presen.save()
                    res = Response(response_message)
                else:
                    res = Response({"message" : "Isi Semua data"}, status=status.HTTP_400_BAD_REQUEST)
        return res
    
    def update(self, request, *args, **kwargs):
        logged_in = request.user.roles
        if(logged_in == 'hrd'):
            data = request.data
            if data:
                presence_obj = self.get_object()
                date = datetime.strptime(data['working_date'], '%Y-%m-%d').date()

                employee = User.objects.get(id=data["employee"])

                presence_obj.employee = employee
                presence_obj.working_date = date

                if 'start_from' in data:
                    presence_obj.start_from = int(data.get('start_from'))
                    presence_obj.end_from = int(data.get('end_from'))

                if 'lembur_start' in data:
                    presence_obj.lembur_start = int(data.get('lembur_start'))
                    presence_obj.lembur_end = int(data.get('lembur_end'))
                    print(presence_obj.lembur_start)

                if 'ket' in data:
                    presence_obj.ket = data.get('ket')
                    
                if presence_obj.is_lock == False:
                    presence_obj.save()
                    create_log(action="create", message=f"Presensi {employee.name} pada tanggal {date} diubah oleh {request.user.name}")
                    res = Response({'message' : 'Data berhasil disimpan'}, status=status.HTTP_200_OK)
                else:
                    res = Response({'message' : 'Data tidak dapat diubah, karena sudah dikunci oleh hrd'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                res = Response({'message' : 'Isikan data yang di perlukan'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            res = Response({'message' : 'Anda bukan HR, untuk mengeditnya silahkan ke HR terlebih dahulu'}, status=status.HTTP_401_UNAUTHORIZED)

        return res

class PresenceSearch(APIView):
    serializer_class = PresenceEmployeeSerializers
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        presence_emp = PresenceEmployee.objects.all().order_by('-id')
        return presence_emp

    def get(self, request, *args, **kwargs):
        querySet = PresenceEmployee.objects.all().order_by('-id')
        employee = self.request.query_params.get('employee', None)
        working_date = self.request.query_params.get('working_date', None)
        months = self.request.query_params.get('months', None)
        years = self.request.query_params.get('years', None)

        if employee:
            querySet=querySet.filter(employee__name__contains=employee)
        if years:
            querySet=querySet.filter(years=years)
        if months:
            querySet=querySet.filter(months=months)
        if working_date:
            querySet=querySet.filter(working_date=working_date)

        serializer = PresenceEmployeeSerializers(querySet, many=True)

        return Response(serializer.data) 

class PresenceAPICompare(APIView):
    serializer_class = PresenceEmployeeSerializers
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        petitions = PresenceEmployee.objects.all().order_by('working_date')
        return petitions

    def get(self, request, *args, **kwargs):
        querySet = PresenceEmployee.objects.all().order_by('working_date')

        employee = self.request.query_params.get('employee', None)
        working_date = self.request.query_params.get('working_date', None)
        months = self.request.query_params.get('months', None)
        years = self.request.query_params.get('years', None)
        work_date = self.request.query_params.get('work_date', None)
        end_work_date = self.request.query_params.get('end_work_date', None)
        
        if work_date and end_work_date:
            querySet=querySet.filter(working_date__gte=work_date, working_date__lte=end_work_date)
        if employee:
            querySet=querySet.filter(employee__pk=employee)
        if years:
            querySet=querySet.filter(years=years)
        if months:
            querySet=querySet.filter(months=months)
        if working_date:
            querySet=querySet.filter(working_date=working_date)

        serializer = PresenceEmployeeSerializers(querySet, many=True)

        return Response(serializer.data) 

class PresenceAPIAnalisis(APIView):
    serializer_class = PresenceEmployeeSerializers

    def get_queryset(self):
        petitions = PresenceEmployee.objects.all().order_by('working_date')
        return petitions

    def get(self, request, *args, **kwargs):
        users = request.user
        if(users.roles == "hrd"):
            querySet = PresenceEmployee.objects.all().order_by('working_date')
        else:
            querySet = PresenceEmployee.objects.all().filter(employee=users.pk).order_by('working_date')

        employee = self.request.query_params.get('employee', None)
        working_date = self.request.query_params.get('working_date', None)
        months = self.request.query_params.get('months', None)
        years = self.request.query_params.get('years', None)

        if employee:
            querySet=querySet.filter(employee__pk=employee)
        if years:
            querySet=querySet.filter(years=years)
        if months:
            querySet=querySet.filter(months=months)
        if working_date:
            querySet=querySet.filter(working_date=working_date)

        serializer = PresenceEmployeeSerializers(querySet, many=True)

        return Response(serializer.data) 

class TopPresenceAPIView(APIView):
    serializer_class = PresenceEmployeeSerializers

    def get(self, request):
        querySet = PresenceEmployee.objects.values('working_hour').annotate(employee__pk=Count('working_hour')).order_by('-employee__pk')[:5]
        months = self.request.query_params.get('months', None)
        year = self.request.query_params.get('year', None)
        
        querySet = PresenceEmployee.objects.all()
        employee = self.request.query_params.get('employee', None)
        if employee:
            querySet=querySet.filter(employee__pk=employee)
        if months:
            querySet=querySet.filter(months=months)
        if year:
            querySet=querySet.filter(years=year)
        
        total_karyawan_all = querySet.count()
        total_karyawan = querySet.aggregate(
            employee_masuk=Count("employee__pk", filter=Q(lembur_hour = None)),
            employee_lembur=Count("employee__pk", filter=Q(working_hour = None)),
            employee_masuks=Count("employee__pk", filter=Q(lembur_hour= None) | Q(working_hour = None)),
        )

        return Response({ 
                         "data" : total_karyawan,
                         "cth" : total_karyawan_all,
                         })

class PresenceStatistikUser(APIView):
    def get(self, request, month, year, *args, **kwargs):
        user_attendance = (
            PresenceEmployee.objects
            .filter(working_date__year=year, working_date__month=month, working_hour__isnull=False)
            .values('employee__name')
            .annotate(total_attendance=Count('id'))
            .order_by('total_attendance')
        )
        
        result = [
            {item['employee__name']: item['total_attendance']}
            for item in user_attendance
        ]
        
        return Response(result)

class StatistikPresenceInMonth(APIView):
    def get(self, request, year):
        log_user = self.request.user
        if log_user.roles == 'hrd':
            presence_data = PresenceEmployee.objects.annotate(
                month=TruncMonth('working_date')
            ).filter(working_hour__isnull=False, working_date__year=year).values('month').annotate(
                count=Count('id')
            ).order_by('month')
        else:
            presence_data = PresenceEmployee.objects.annotate(
                month=TruncMonth('working_date')
            ).filter(employee=log_user.pk, working_hour__isnull=False, working_date__year=year).values('month').annotate(
                count=Count('id')
            ).order_by('month')
        
        result = [
            {item['month'].strftime('%b'): item['count']} for item in presence_data
        ]
        
        return Response(result)


class StatistikSubmissionEmployeeInMonth(APIView):
    def get(self, request, year):
        user_log = self.request.user
        bulan = request.data.get('month', None)
        if user_log.roles == 'hrd':
            presence_data = PresenceEmployee.objects.all().filter(working_date__year=year)
        else:
            presence_data = PresenceEmployee.objects.all().filter(working_date__year=year, employee=user_log.pk)

        if bulan:
            presence_data.filter(months=bulan)
    
        result = {
            month_abbr: {
                "tidak masuk": 0,
                "sakit": 0,
                "izin": 0,
                "cuti": 0,
                "wfh": 0,
                # "presence": 0 
            } for month_abbr in calendar.month_abbr[1:]
        }
        
        for presence in presence_data:
            month = calendar.month_abbr[presence.working_date.month]  
            ket = presence.ket
            
            if ket in result[month]:
                result[month][ket] += 1

            # if presence.ket is None and presence.start_from:
            #     result[month]['presence'] += 1

        create_log(action="get", message=f"logged {user_log.name}")
        if user_log.roles == 'hrd':
            valid_years = set(PresenceEmployee.objects.all().values_list('years', flat=True))
        else:
            valid_years = set(PresenceEmployee.objects.filter(employee=user_log.pk).values_list('years', flat=True))

        list_years = list(valid_years)

        res = {
            'list_year': list_years,
            'data' : result
        }
        return Response(result)
    
class StatistikEmployeeperMonth(APIView):
    def get(self, request, year):
        user_log = self.request.user
        bulan = request.data.get('month', None)
        if user_log.roles == 'hrd':
            presence_data = PresenceEmployee.objects.all().filter(working_date__year=year)
        else:
            presence_data = PresenceEmployee.objects.all().filter(working_date__year=year, employee=user_log.pk)

        if bulan:
            presence_data.filter(months=bulan)
    
        result = {
            month_abbr: {
                "tidak masuk": 0,
                "sakit": 0,
                "izin": 0,
                "cuti": 0,
                "wfh": 0,
                "presence": 0 
            } for month_abbr in calendar.month_abbr[1:]
        }
        
        for presence in presence_data:
            month = calendar.month_abbr[presence.working_date.month]  
            ket = presence.ket
            
            if ket in result[month]:
                result[month][ket] += 1

            if presence.ket is None and presence.start_from:
                result[month]['presence'] += 1

        create_log(action="get", message=f"logged {user_log.name}")
        if user_log.roles == 'hrd':
            valid_years = set(PresenceEmployee.objects.all().values_list('years', flat=True))
        else:
            valid_years = set(PresenceEmployee.objects.filter(employee=user_log.pk).values_list('years', flat=True))

        list_years = list(valid_years)

        res = {
            'list_year': list_years,
            'data' : result
        }
        return Response(res)
    
class PresenceWFHGenerate(APIView):
    def post(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        user_id = request.data.get('user_id')
        user = self.request.user
        employee = User.objects.get(id=user_id)

        # Validasi bahwa start_date dan end_date tidak boleh kosong
        if not start_date or not end_date:
            return Response({'message': 'Start date dan end date harus diisi'}, status=status.HTTP_400_BAD_REQUEST)

        if user.roles == 'hrd':
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return Response({'message': 'Format tanggal tidak valid. Gunakan format YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

            current_date = start_date
            while current_date <= end_date:
                if not CalendarDashHRD.objects.filter(date=current_date.date()).exists():
                    if not PresenceEmployee.objects.filter(
                        employee_id=user_id,
                        working_date=current_date.date(),
                    ).exists():
                        if current_date.weekday() < 5: 
                            PresenceEmployee.objects.create(
                                employee_id=user_id,
                                ket='wfh',
                                working_date=current_date.date()
                            )
                            create_log(action="create", message=f"Presensi {employee.name} wfh tanggal {current_date.date()} ubah oleh {request.user.name}")
                    else:
                        current_date += timedelta(days=1)
                else:
                    current_date += timedelta(days=1)
            results = Response({'message': 'Presensi berhasil di-generate'}, status=status.HTTP_201_CREATED)
        else:
            results = Response({'message': 'Anda tidak memiliki hak akses untuk generate presensi'}, status=status.HTTP_403_FORBIDDEN)

        return results

class PresenceLocked(APIView):
    def post(self, request):
        user = self.request.user
        data = request.data
        employee = data.get('employee')
        month = data.get('month')
        locked = int(data.get('locked'))
        if user.roles == 'hrd':
            presence = PresenceEmployee.objects.filter(employee=User.objects.get(id=employee), working_date__month=int(month))
            if locked == 1:
                for data in presence:
                    data.is_lock = True
                    data.save()
                return Response({'message': 'Presensi Berhasil di lock'}, status=status.HTTP_201_CREATED)
            elif locked == 0:
                for data in presence:
                    data.is_lock = False
                    data.save()
                return Response({'message': 'Presensi Berhasil di unlock'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Masukan data yang benar pada value lock'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Anda tidak memiliki hak akses untuk mengunci atau membuka kunci presensi'}, status=status.HTTP_403_FORBIDDEN)

from calendar import month_name

class PresenceAnalysisEmployee(APIView):
    def get(self, request):
        year = datetime.now().year
        model = PresenceEmployee.objects

        user = request.query_params.get('employee', None)
        from_date = request.query_params.get('from_date', None)
        end_date = request.query_params.get('end_date', None)
        fm_range = datetime.strptime(from_date, '%Y-%m-%d').month
        em_range =  datetime.strptime(end_date, '%Y-%m-%d').month
        months = range(fm_range, em_range+1)

        print(from_date, end_date)

        monthly_totals = []
        summary_presence = []
        av_start_from = []
        av_end_from = []
        av_lembur = 0

        summary_presence.append({
            "sakit": 0,
            "cuti": 0,
            "izin": 0,
            "average_pre_in" : 0,
            "average_pre_out" : 0,
            "average_lembur" : 0
        })

        for y in model.filter(working_date__gte=from_date, working_date__lte=end_date, employee__id=user):
            if y.ket == "sakit":
                summary_presence[0]['sakit'] += 1
            elif y.ket == "cuti":
                summary_presence[0]['cuti'] += 1
            elif y.ket == "izin":
                summary_presence[0]['izin'] += 1

        calendar = CalendarDashHRD.objects.all().filter(date__year=datetime.strptime(from_date, '%Y-%m-%d').year)
        calendar_data = []
        for cal in calendar:
            calendar_data.append(cal.title_day)
        
        for month in months:
            presences = model.filter(
                working_date__month=month,
                employee__id=user,
            ).exclude(ket__in=['sakit', 'cuti', 'izin', 'wfh']).exclude(ket__in=calendar_data)
            j_wk = 0
            m_wk = 0
           
            j_lembur = 0
            m_lembur = 0

            jam_lembur = 0
            menit_lembur = 0

            jam = 0
            menit = 0
           
            for pres in presences:
                jam = parseHour(pres.working_hour if pres.working_hour else 0)
                menit = parseMinute(pres.working_hour if pres.working_hour else 0)
                jam_lembur = parseHour(pres.lembur_hour if pres.lembur_hour else 0)
                menit_lembur = parseMinute(pres.lembur_hour if pres.lembur_hour else 0)
                j_wk += int(jam)
                m_wk += int(menit)
                j_lembur += int(jam_lembur)
                m_lembur += int(menit_lembur)

                if pres.start_from:
                    av_start_from.append(pres.start_from)
                    av_end_from.append(pres.end_from)
                else:
                    pass
            print(f"jam : {j_wk}, menit : {m_wk}, lembur : {j_lembur}, menlembur : {m_lembur}")
            menit_kerja = fix_hour(m_wk)
            menit_lembur = fix_hour(m_lembur)
            
            if len(str(menit_kerja)) > 2:
                sub_mk = parseHour(menit_kerja)
                sub_mk2 = parseMinute(menit_kerja)
                if len(str(sub_mk2)) < 2:
                    sub_mk2 = f"0{sub_mk2}"
                j_wk+=sub_mk
                menit_kerja = sub_mk2

            if len(str(menit_lembur)) > 2:
                sub_ml = parseHour(menit_lembur)
                sub_ml2 = parseMinute(menit_lembur)
                if len(str(sub_ml2)) < 2:
                    sub_ml2 = f"0{sub_ml2}"
                j_wk+=sub_ml
                menit_lembur = sub_ml2
            
            if menit_kerja == 0:
                menit_kerja = f"{parseMinute(menit_kerja)}0"
            if menit_lembur == 0:
                menit_lembur = f"{parseMinute(menit_lembur)}0"

            # print(f"jam : {j_wk}{menit_kerja}")
            # print(f"jam : {j_lembur}{menit_lembur}")
            jam_aktual = int(f"{j_wk}{menit_kerja}")
            jam_aktual_lembur = int(f"{j_lembur}{menit_lembur}")
        
            t_working_hour = fix_hour(jam_aktual)
            t_lembur_hour = fix_hour(jam_aktual_lembur)

            av_lembur+=int(t_lembur_hour)

            total_working_hour = int(t_working_hour)
            efektif_hour = 800
            if user == 6:
                efektif_hour = 900
            jk_efektif = presences.filter(start_from__isnull=False).count() * efektif_hour
            
            kurleb = 0
            if presences.count() != 0 and total_working_hour != 0 and jk_efektif != 0:
                kurleb = formula_sum_actual(total_working_hour,jk_efektif)

            month = month_name[month]
            formatted_result = {
                "bulan": month,
                "hari_kerja": presences.filter(start_from__isnull=False).count(),
                "jk_aktual": total_working_hour,
                "jk_efektif": jk_efektif,
                "kurleb": kurleb,
            }
            monthly_totals.append(formatted_result)
            
        total_days = model.filter(working_date__gte=from_date, working_date__lte=end_date, employee__id=user, start_from__isnull=False).count()

        summary_presence[0]['average_pre_in'] = int(median(av_start_from if av_start_from else [0]))
        summary_presence[0]['average_pre_out'] = int(median(av_end_from if av_end_from else [0]))
        summary_presence[0]['average_lembur'] = parseToHour(av_lembur/total_days if total_days else 1)
        return Response({"data": monthly_totals, "summary": summary_presence})

class PresenceAnalysisOn(APIView):
    def get(self, request, year, month):
        users = self.request.user
        presence = PresenceEmployee.objects.filter(years=year, months=month)
        if users.roles == 'karyawan' or users.roles == 'atasan':
            presence = presence.filter(employee=User.objects.get(id=users.id))
        
        employee = request.query_params.get('employee', None)
        if employee and users.roles == 'hrd':
            presence = presence.filter(employee=employee)

        srz = PresenceEmployeeAnalisisSerializers(presence, many=True)

        total_hour_working = 0
        total_hour_lembur = 0

        keterangan = {
            'cuti' : 0,
            'izin' : 0,
            'sakit' : 0
        }


        for x in presence:
            if x.working_hour is not None:
                value = total_hour_working + x.working_hour
                total_dua_bel = last_digit(x.working_hour) + last_digit(total_hour_working)
                if total_dua_bel > 59:
                    value += 40
                total_hour_working = value

            if x.lembur_hour is not None:
                lembur_value = total_hour_lembur + x.lembur_hour
                total_dua_bel_lembur = last_digit(x.lembur_hour) + last_digit(total_hour_lembur)
                if total_dua_bel_lembur > 59:
                    lembur_value += 40
                total_hour_lembur = lembur_value
            
            if x.ket:
                if x.ket == 'cuti':
                    keterangan['cuti']+=1
                elif x.ket == 'sakit':
                    keterangan['sakit']+=1
                elif x.ket == 'izin':
                    keterangan['izin']+=1
        count_day = presence.filter(start_from__isnull=False).exclude(cat="").count()
        jam_efektif = count_day*800
        if employee == 6 or users.id == 6:
            jam_efektif = count_day*900
        
        summary_hour = formula_sum_actual(total_hour_working, jam_efektif)

        context = {
            'data' : srz.data,
            'total_hour' : total_hour_working,
            'total_hour_lembur' : total_hour_lembur,
            'keterangan' : keterangan,
            'working_day' :count_day,
            'efektif_hour' : jam_efektif,
            'summary_hour' : summary_hour
        }
        return Response(context)