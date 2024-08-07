from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from submisssion.api.serializer import SubmissionSerializer

from submisssion.models import Submission
from userapp.utils.modelfunction import create_calendar, create_log, delete_calendar

from .serializer import NotesSerializer
from noteHR.models import NotesApp
from userapp.models import User
from presenceEmployee.models import PresenceEmployee
from datetime import datetime
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view

class NotesAPIView(APIView):
    serializer_class = NotesSerializer
    # pagination_class = LimitOffsetPagination

    def get_queryset(self):
        notes = NotesApp.objects.all().order_by('-id')
        return notes
    
    def get(self, request, *args, **kwargs):
        querySet = NotesApp.objects.all().order_by('-id')
        
        employee_name = self.request.query_params.get('employee_name', None)
        employee_id = self.request.query_params.get('employee_id', None)
        notes = self.request.query_params.get('notes', None)
        date_note = self.request.query_params.get('date_note', None)
        hari = self.request.query_params.get('hari', None)
        bulan = self.request.query_params.get('bulan', None)
        tahun = self.request.query_params.get('tahun', None)

        if employee_name:
            querySet=querySet.filter(employee__name__icontains=employee_name)
        if employee_id:
            querySet=querySet.filter(employee__id__contains=employee_id)
        if date_note:
            querySet=querySet.filter(date_note=date_note)
        if notes:
            querySet=querySet.filter(notes=notes)
        if hari:
            querySet=querySet.filter(hari=hari)
        if bulan:
            querySet=querySet.filter(bulan=bulan)
        if tahun:
            querySet=querySet.filter(tahun=tahun)

        serializer = NotesSerializer(querySet, many=True)

        return Response(serializer.data) 
    

class NotesAPIVIEWID(viewsets.ModelViewSet):
    serializer_class = NotesSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        # notes = NotesApp.objects.all().order_by('-id')
        logged_user = self.request.user
        if(logged_user.roles == 'hrd'):
            querySet = NotesApp.objects.all().order_by('-id')
        
            employee_name = self.request.query_params.get('employee_name', None)
            employee_id = self.request.query_params.get('employee_id', None)
            notes = self.request.query_params.get('notes', None)
            date_note = self.request.query_params.get('date_note', None)
            hari = self.request.query_params.get('hari', None)
            bulan = self.request.query_params.get('bulan', None)
            tahun = self.request.query_params.get('tahun', None)

            if employee_name:
                querySet=querySet.filter(employee__name__icontains=employee_name)
            if employee_id:
                querySet=querySet.filter(employee__id__contains=employee_id)
            if date_note:
                querySet=querySet.filter(date_note=date_note)
            if notes:
                querySet=querySet.filter(notes=notes)
            if hari:
                querySet=querySet.filter(hari=hari)
            if bulan:
                querySet=querySet.filter(bulan=bulan)
            if tahun:
                querySet=querySet.filter(tahun=tahun)
        else:
            # querySet = NotesApp.objects.all().filter(employee=logged_user.pk, type_notes='cuti').order_by('-id')
            querySet = NotesApp.objects.filter(employee=logged_user.pk).exclude(type_notes__in=['masuk', 'catatan']).order_by('-id')

        # serializer = NotesSerializer(querySet, many=True)

        # return serializer.data
        return querySet

    def get_ids(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
                notes = NotesApp.objects(id=ids)
                serializer = NotesSerializer(notes)
        else:
            pett = self.get_queryset()
            employee_name = self.request.query_params.get('employee_name', None)
            notes = self.request.query_params.get('notes', None)
            date_note = self.request.query_params.get('date_note', None)
            if employee_name:
                querySet=querySet.filter(employee_name=employee_name)
            if date_note:
                querySet=querySet.filter(date_note=date_note)
            if notes:
                querySet=querySet.filter(notes=notes)
            serializer = NotesSerializer(pett, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        notes_data = request.data
        empl = notes_data.get("employee")
        datn = notes_data.get("date_note")
        noted = notes_data.get("notes")
        typ = notes_data.get("type_notes")

        date = datetime.strptime(datn, '%Y-%m-%d').date()

        if(empl != '' and datn != '' and noted != ''):
            new_notes = NotesApp.objects.create(employee=User.objects.get(id=notes_data['employee']), notes=notes_data['notes'], type_notes=notes_data['type_notes'],
                            date_note=notes_data['date_note'])
            new_notes.save()
            if(typ == 'masuk'):
                new_presen = PresenceEmployee.objects.create(employee=User.objects.get(id=notes_data["employee"]), working_date=date,
                                                       end_from=1700, start_from=900, ket=noted
                                                       )
                new_presen.save()
            elif(typ == 'sakit' or typ == 'tidak masuk' or typ == 'izin'):
                new_presen = PresenceEmployee.objects.create(employee=User.objects.get(id=notes_data["employee"]), working_date=date,
                                                       end_from=None, start_from=None, ket=typ
                                                       )
                new_presen.save()
            elif(typ == 'cuti'):
                new_presen = PresenceEmployee.objects.create(employee=User.objects.get(id=notes_data["employee"]), working_date=date,
                                                       end_from=None, start_from=None, ket=typ
                                                       )
                users_obj = User.objects.get(id=notes_data['employee'])
                users_obj.sisa_cuti = int(users_obj.sisa_cuti) - 1

                users_obj.save()
                new_presen.save()
            
            serializer = NotesSerializer(new_notes)
            response_message={"message" : "Catatan Berhasil dibuat",
                                "data": serializer.data
                }
            return Response(response_message)
        else:
            return Response({"error" : "Please fill all fields"}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        note_object = self.get_object()
        data = request.data

        employee = User.objects.get(id=data.get("employee"))
        print(note_object.type_notes)
        print(data.get('type_notes'))
        note_object.employee = employee
        note_object.notes = data.get('notes')
        date = datetime.strptime(data.get('date_note'), '%Y-%m-%d').date()
       
        # if note_object.type_notes != data.get('type_notes'):
        if data.get('type_notes') != 'masuk':
            presence_emp = PresenceEmployee.objects.get(employee=employee, working_date=note_object.date_note, ket=note_object.type_notes)
            if note_object.type_notes == 'masuk':
                presence_emp.delete()
                PresenceEmployee.objects.create(employee=employee, working_date=note_object.date_note, ket=note_object.type_notes)
            presence_emp = PresenceEmployee.objects.get(employee=employee, working_date=note_object.date_note, ket=note_object.type_notes)
            presence_emp.ket = data.get('type_notes')
            presence_emp.working_date = date
            if note_object.type_notes == 'cuti':
                employee.sisa_cuti += 1
                employee.save()
                create_log(message=f"cuti bertambah 1 untuk user {employee.name} karena {request.user.roles} mengubah tipe catatan menjadi {data.get('type_notes')} dari {note_object.type_notes}", action="update")
            elif data.get('type_notes') == 'cuti':
                employee.sisa_cuti -= 1
                employee.save()
                create_log(message=f"cuti berkurang 1 untuk user {employee.name} karena {request.user.roles} mengubah tipe catatan menjadi {data.get('type_notes')} dari {note_object.type_notes}", action="update")
        else:
            if note_object.type_notes == 'cuti':
                employee.sisa_cuti += 1
                employee.save()
                create_log(message=f"cuti bertambah 1 untuk user {employee.name} karena {request.user.roles} mengubah tipe catatan menjadi {data.get('type_notes')} dari {note_object.type_notes}", action="update")
            presence_emp = PresenceEmployee.objects.get(employee=employee, working_date=note_object.date_note, ket=note_object.type_notes)
            presence_emp.ket = data.get('type_notes')
            presence_emp.start_from = 900
            presence_emp.end_from = 1700
            presence_emp.working_date=date
        presence_emp.save()
        
        # if presence_emp:
        #     if data.get('type_notes') != 'cuti':
        #         presence_emp.ket = data.get('type_notes')

        #         if note_object.type_notes == 'cuti':
        #             employee.sisa_cuti += 1
        #             employee.save()
        #     else:
        #         presence_emp.ket = data.get('type_notes')
        #         employee.sisa_cuti -= 1
        #         employee.save()
      
        note_object.type_notes = data.get('type_notes')
        note_object.date_note = data.get('date_note')

        note_object.save()

        serializer = NotesSerializer(note_object)

        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        # logedin_user = request.user.roles
        # if(logedin_user == "hrd"):
        notesed = self.get_object()
        notesed.delete()
        response_message={"message" : "Notes has been deleted"}
        # else:
            # response_message={"message" : "Not Allowed"}

        return Response(response_message)


class NotesAPIID(viewsets.ModelViewSet):
    serializer_class = NotesSerializer

    def get_queryset(self):
        notes = NotesApp.objects.all().order_by('-id')
        return notes
    
    def get_ids(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
                notes = NotesApp.objects(id=ids)
                serializer = NotesSerializer(notes)
        else:
            querySet = self.get_queryset()
            employee_name = self.request.query_params.get('employee_name', None)
            notes = self.request.query_params.get('notes', None)
            date_note = self.request.query_params.get('date_note', None)
            if employee_name:
                querySet=querySet.filter(employee__pk=employee_name)
            if date_note:
                querySet=querySet.filter(date_note=date_note)
            if notes:
                querySet=querySet.filter(notes=notes)
            serializer = NotesSerializer(querySet, many=True)
        return Response(serializer.data)
    

@api_view(['GET'])
def get_cuti(request, year, emp_id):
    notes = NotesApp.objects.filter(employee=emp_id, type_notes='cuti', tahun=year)
    submission = Submission.objects.filter(employee=emp_id, permission_type='cuti', start_date__year=year)

    serializer_notes = NotesSerializer(notes, many=True)
    serializer_submiss = SubmissionSerializer(submission, many=True)

    return Response({
        "notes_cuti": serializer_notes.data,
        "submission_cuti": serializer_submiss.data,
    })

@api_view(['POST'])
def post_delete_notes(request):
    notes_data = request.data
    notes_id = notes_data.get("notes_id")
    # date_note = notes_data.get("date_note")
    # notes = notes_data.get("notes")
    # type_notes = notes_data.get("type_notes")

    notes = NotesApp.objects.filter(id=notes_id)

    user = get_object_or_404(User, id=notes.employee)

    if notes.ket != 'catatan':
        if notes.ket != 'masuk':
            presencess = PresenceEmployee.objects.get(employee=user, working_date=notes.date_note, ket=notes.ket)
            if notes.ket == 'cuti':
                user.sisa_cuti += 1
                user.save()
                create_log(action="delete", message=f"notes dengan type {notes.ket} di delete oleh {request.user.roles}, cuti user {user.name} bertambah 1")
            presencess.delete()
        else:
            presencess = PresenceEmployee.objects.get(employee=user, working_date=notes.date_note, start_from=900, end_from=1700)
            presencess.delete()

    notes.delete()
    response_message = {"message": "Notes has been deleted"}
    return Response(response_message)