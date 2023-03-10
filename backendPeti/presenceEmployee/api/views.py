from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from presenceEmployee.models import PresenceEmployee
from .serializers import PresenceEmployeeSerializers
from django.db.models import Count, Sum, Q
from userapp.models import User

class PresenceAPIView(APIView):
    serializer_class = PresenceEmployeeSerializers

    def get_queryset(self):
        presens = PresenceEmployee.objects.all().order_by('-id')
        return presens

class PresenceAPIViewID(viewsets.ModelViewSet):
    serializer_class = PresenceEmployeeSerializers

    def get_queryset(self):
        presences = PresenceEmployee.objects.all().order_by('-id')
        return presences
    
    def get_ids(self, request, *args, **kwargs):
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
        if(wrkdt != None):
            if(strfrom and lmbrstr != None):
                new_presen = PresenceEmployee.objects.create(employee=User.objects.get(id=presen["employee"]), working_date=presen["working_date"],
                                                            end_from=int(presen["end_from"]), start_from=int(presen["start_from"]), lembur_start=int(presen["lembur_start"]), 
                                                            lembur_end=int(presen["lembur_end"]),  ket=presen["ket"]
                                                            )
                serializer = PresenceEmployeeSerializers(new_presen)
                response_message={"message" : "Berhasil membuat data",
                                    "data": serializer.data
                    }
                new_presen.save()
                res = Response(response_message)
            elif(strfrom != None):
                new_presen = PresenceEmployee.objects.create(employee=User.objects.get(id=presen["employee"]), working_date=presen["working_date"],
                                                            end_from=int(presen["end_from"]), start_from=int(presen["start_from"]),  ket=presen["ket"]
                                                            )
                serializer = PresenceEmployeeSerializers(new_presen)
                response_message={"message" : "Berhasil membuat data",
                                    "data": serializer.data
                    }
                new_presen.save()
                res = Response(response_message)
            elif(lmbrstr != None):
                new_presen = PresenceEmployee.objects.create(employee=User.objects.get(id=presen["employee"]), working_date=presen["working_date"],
                                                             lembur_start=int(presen["lembur_start"]), lembur_end=int(presen["lembur_end"]),  ket=presen["ket"]
                                                            )
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
        presence_obj = self.get_object()
        data = request.data

        employee = User.objects.get(id=data["employee"])

        presence_obj.employee = employee
        presence_obj.working_date = data['working_date']
        # presence_obj.working_date = datetime.strptime(data['working_date'], '%Y-%m-%d')
        if(presence_obj.start_from):
            presence_obj.start_from = int(data['start_from'])
            presence_obj.end_from = int(data['end_from'])
        if(presence_obj.lembur_start != None):
            presence_obj.lembur_start = data['lembur_start']
            presence_obj.lembur_end = data['lembur_end']
        if(presence_obj.ket != None):
            presence_obj.ket = data['ket']

        presence_obj.save()

        serializers = PresenceEmployeeSerializers(presence_obj)

        return Response(serializers.data)

class PresenceSearch(APIView):
    serializer_class = PresenceEmployeeSerializers

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

    def get_queryset(self):
        petitions = PresenceEmployee.objects.all().order_by('working_date')
        return petitions

    def get(self, request, *args, **kwargs):
        querySet = PresenceEmployee.objects.all().order_by('working_date')

        employee_name = self.request.query_params.get('employee_name', None)
        working_date = self.request.query_params.get('working_date', None)
        months = self.request.query_params.get('months', None)
        years = self.request.query_params.get('years', None)
        work_date = self.request.query_params.get('work_date', None)
        end_work_date = self.request.query_params.get('end_work_date', None)
        
        if work_date and end_work_date:
            querySet=querySet.filter(working_date__gte=work_date, working_date__lte=end_work_date)
        if employee_name:
            querySet=querySet.filter(employee__name__contains=employee_name)
        if years:
            querySet=querySet.filter(years=years)
        if months:
            querySet=querySet.filter(months=months)
        if working_date:
            querySet=querySet.filter(working_date=working_date)

        serializer = PresenceEmployeeSerializers(querySet, many=True)

        return Response(serializer.data) 