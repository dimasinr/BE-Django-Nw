from datetime import datetime
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from calendarDash.models import DashboardHRD, CalendarDashHRD
from .serializers import DashboardHrdSerializers, CalendarDashSerializers
from django.db.models import Count, Q
from userapp.models import User
from presenceEmployee.models import PresenceEmployee
from rest_framework.decorators import api_view

class DashboardTopAPIView(viewsets.ModelViewSet):
    serializer_class = DashboardHrdSerializers

    def get_queryset(self):
        dashboards = DashboardHRD.objects.all().order_by('-id')
        return dashboards

    def get(self, request):
        id = request.query_params['id']
        if id != None:
            dash = DashboardHRD.objects(id=id)
            serializer = DashboardHrdSerializers
        else:
            dash = self.get_queryset()
            serializer = DashboardHrdSerializers(dash, many=True)

        return Response(serializer.data)

class CalendarAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CalendarDashSerializers

    def get_queryset(self):
        calendarHr = CalendarDashHRD.objects.all().order_by('date')
        return calendarHr
    
    def get_ids(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
            calendarHr = CalendarDashHRD.objects(id=ids)
            serializer = CalendarDashSerializers(calendarHr)
        else:
            pett = self.get_queryset()
            serializer = CalendarDashSerializers(pett, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        calendarData = request.data
        if calendarData:
            titleday = calendarData.get("title_day")
            typeday = calendarData.get("type_day")
            date_str = calendarData.get("date")
            date = datetime.strptime(date_str, '%Y-%m-%d').date()

            if date.weekday() >= 5:
                dayof = 'weekend'
            else:
                dayof = 'weekday'
            try:
                existing_date = CalendarDashHRD.objects.get(date=date)
                response_message = {"message": f"Sudah ada Jenis data di tanggal {existing_date.date}"}
                return Response(response_message, status=409)
            except CalendarDashHRD.DoesNotExist:
                CalendarDashHRD.objects.create(title_day=titleday, type_day=typeday, date=date, day_of=dayof)

                if dayof == 'weekday':
                    users = User.objects.all().filter(is_active=True)
                    for user in users:
                        PresenceEmployee.objects.create(employee=user, working_date=date, ket=titleday)
            response_message = Response({"message" : "Data Berhasil ditambahkan"}, status=status.HTTP_201_CREATED)  
        else:
            response_message = Response({"message" : "Tidak dapat menambahkan data dikarenakan tidak mengisi semua data"}, status=status.HTTP_400_BAD_REQUEST)  
        return response_message
    
class CalendarAPIView(APIView):
    serializer_class = DashboardHrdSerializers

    def get_queryset(self):
        petitions = CalendarDashHRD.objects.all().order_by('-id')
        return petitions

    def get(self, request, *args, **kwargs):
        querySet = CalendarDashHRD.objects.all().order_by('-id')
        
        employee_name = self.request.query_params.get('employee_name', None)
        working_date = self.request.query_params.get('working_date', None)
        months = self.request.query_params.get('months', None)
        years = self.request.query_params.get('years', None)

        if employee_name:
            querySet=querySet.filter(employee_name=employee_name)
        if years:
            querySet=querySet.filter(years=years)
        if months:
            querySet=months.filter(months=months)
        if working_date:
            querySet=querySet.filter(working_date=working_date)

        serializer = DashboardHrdSerializers(querySet, many=True)

        return Response(serializer.data) 

class WeekTotals(APIView):
    serializer_class = CalendarDashSerializers

    def get(self, request):
        week = CalendarDashHRD.objects.all()
        day_of_total = week.count()
        week_of_total = CalendarDashHRD.objects.aggregate(
            weekend=Count("day_of", filter=Q(day_of='weekend')),
            weekday=Count("day_of", filter=Q(day_of='weekday')),
        )

        case_weekend = CalendarDashHRD.objects.filter(day_of__contains='weekend')
        serializer_weekend = CalendarDashSerializers(case_weekend, many=True)

        case_weekday = CalendarDashHRD.objects.filter(day_of__contains='weekday')
        serializer_weekday = CalendarDashSerializers(case_weekday, many=True)

        case_cuti = CalendarDashHRD.objects.filter(day_of__contains='cuti')
        serializer_cuti = CalendarDashSerializers(case_cuti, many=True)

        case_izin = CalendarDashHRD.objects.filter(day_of__contains='izin')
        serializer_izin = CalendarDashSerializers(case_izin, many=True)

        case_sakit = CalendarDashHRD.objects.filter(day_of__contains='sakit')
        serializer_sakit = CalendarDashSerializers(case_sakit, many=True)

        return Response({"message" : "WeekDay and WeekEnd", 
                         "weeks" : week_of_total,
                         "day_of_total" : day_of_total,
                         "weekday" : serializer_weekday.data,
                         "weekend" : serializer_weekend.data,
                         "cuti" : serializer_cuti.data,
                         "izin" : serializer_izin.data,
                         "sakit" : serializer_sakit.data
                         })
                         
@api_view(['POST'])
def post_delete_calendar(request):
    calendarData = request.data
    if calendarData:
        calendar_id = calendarData.get("calendar_id")
        calendar = CalendarDashHRD.objects.filter(id=calendar_id).first()
        if calendar is None:
            return Response({"message" : "Tidak ada data calendar tersebut"}, status=status.HTTP_404_NOT_FOUND) 

        if calendar.date.weekday() >= 5:
            dayof = 'weekend'
        else:
            dayof = 'weekday'
        if dayof == 'weekday':
            users = User.objects.all().filter(is_active=True)
            for user in users:
                presen = PresenceEmployee.objects.filter(employee=user, working_date=calendar.date, ket=calendar.title_day)
                if presen.exists():
                    presen.delete()
                else:
                    print("tidak ada data presensi")
        calendar.delete()
        response_message = Response({"message" : "Data berhasil dihapus"}, status=status.HTTP_200_OK)  
    else:
        response_message = Response({"message" : "Tidak dapat menambahkan data dikarenakan tidak mengisi semua data"}, status=status.HTTP_400_BAD_REQUEST)  
    return response_message