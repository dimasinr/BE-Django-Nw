from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.db.models import Count, Q
from bank.models import Bank
from calendarDash.models import CalendarDashHRD
from presenceEmployee.models import PresenceEmployee
from userapp.serializer import (
    UserBankSerializer,
    UserBerkasSerializer,
    UserBirthdaySerializers,
    UserCertificateSerializer,
    UserContractListSerializer, 
    UserDetailsSerializer, 
    UserNotesSerializers, 
    UserRolesSerializers, 
    UserTotalDataIOSerializers, 
    UserDivisionSerializers, 
    ResetPasswordSerializer, 
    EmailSerializer, 
    UserContractSerializers,
    UserCertificatePieChartSerializer
)
from userapp.models import User, UserBank, UserBerkas, UserCertificate, UserContract, UserNotes, UserRoles, UserDivision
from django.db.models import Sum
from attendanceEmployee.models import AttendanceEmployee
from rest_framework import generics
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from userapp.utils.utilsfunction import get_weekday_count
from django.contrib.auth.hashers import check_password, make_password

class UserApiView(APIView):
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        users = User.objects.all()
        return users
    
    def get(self, request):
        id = request.query_params['id']
        if id != None:
            userprofiles = User.objects(id=id)
            serializer = UserDetailsSerializer
        else:
            userprofiles = self.get_queryset()
            serializer = UserDetailsSerializer(userprofiles, many=True)

        return Response(serializer.data)
    
    def post(self, request):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        user_filter = User.objects.filter(username=username)
        email_filter = User.objects.filter(email=email)
        print(user_filter)

        if first_name == None or last_name == None or username == None or email == None or password == None or confirm_password == None:
            return Response({'message': 'Gagal! isi semua fields',}, status=status.HTTP_400_BAD_REQUEST) 
        if password != confirm_password:
            return Response({'message': 'Gagal! Password tidak sama',}, status=status.HTTP_400_BAD_REQUEST) 
        if len(password) < 8 and len(confirm_password) < 8:
            return Response({'message': 'Gagal! Password minimal 8 digit',}, status=status.HTTP_400_BAD_REQUEST) 
        if user_filter is None:
            return Response({'message': 'Gagal! Username Sudah digunakan',}, status=status.HTTP_400_BAD_REQUEST) 
        if email_filter is None:
            return Response({'message': 'Gagal! Email Sudah digunakan',}, status=status.HTTP_400_BAD_REQUEST) 
        print(f"{first_name} - {last_name} - {email} - {password} - {username}")

        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.password = make_password(password)
        user.username = username
        user.save()
        return Response({'message': 'Berhasil! User Sudah dibuat',}, status=status.HTTP_201_CREATED) 

class UserViewId(viewsets.ModelViewSet):
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        notes = User.objects.all()
        return notes
    
    def get_ids(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
                notes = User.objects(id=ids)
                serializer = UserDetailsSerializer(notes)
        else:
            pett = self.get_queryset()
            serializer = UserDetailsSerializer(pett, many=True)
        return Response(serializer.data)
        
    def post(self, request, *args, **kwargs):
        users = request.data
        password1 = users.get("password1")
        password2 = users.get("password2")

        if(password1 == password2 ):
            user_regist = User.objects.create(username=users['username'], first_name=users['first_name'], 
                    last_name=users['last_name'], name=users['name'],  sisa_cuti=users['sisa_cuti'], 
                    roles=users['roles'], division=users['division'])
            serializer = UserDetailsSerializer(user_regist)
            response_message={"message" : "User Berhasil dibuat",
                            "data": serializer.data
            }
            user_regist.save()
            ressPon = Response(response_message)
        else:
            ressPon = Response({"message" : "password harus sama"}, status=status.HTTP_400_BAD_REQUEST)  
        
        return ressPon

class UserRole(viewsets.ModelViewSet):
    serializer_class = UserRolesSerializers

    def get_queryset(self):
        notes = UserRoles.objects.all()
        return notes

class UserDivisionView(viewsets.ModelViewSet):
    serializer_class = UserDivisionSerializers

    def get_queryset(self):
        division = UserDivision.objects.all()
        return division

class ListDivision(APIView):
    serializer_class = UserDivisionSerializers

    def get(self, request):
        division = UserDivision.objects.all()
        srz = UserDivisionSerializers(division, many=True)
        return Response(srz.data)

class UserTotal(APIView):
    serializer_class = UserTotalDataIOSerializers

    def get(self, request, year):
        userAct = User.objects.all()
        total_karyawan_all = userAct.count()
        total_karyawan = User.objects.aggregate(
            active_employee=Count("is_active", filter=Q(is_active=True)),
            inactive_employee=Count("is_active", filter=Q(is_active=False)),
        )

        # countPresence = PresenceEmployee.objects.exclude(working_hour=None).count()
        countPresence = PresenceEmployee.objects.aggregate(
            presence=Count("working_hour", filter=~Q(working_hour=None)),
            actual_presence=Count(
                "lembur_hour",
                filter=Q(lembur_hour=None) & Q(working_hour=None) & Q(ket="libur")
            )
        )

        weekday_count = get_weekday_count(year)
        weekend_national_count = CalendarDashHRD.objects.filter(day_of='weekday').count()
        total_day = weekday_count-weekend_national_count

        return Response({
                         "working_day": total_day,
                         "employee" : total_karyawan,
                         "total_attendance" : countPresence,
                         "total_employee" : total_karyawan_all,
                         })

class UserWorkHourAPIView(APIView):
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        user_active = request.GET.get('user_active')
        
        if start_date is None:
            start_date = '1970-01-01'
        if end_date is None:
            end_date = '1970-01-01'
        if user_active is None:
            user_active = True
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        presences = PresenceEmployee.objects.filter(working_date__gte=start_date, working_date__lte=end_date, employee__is_active=user_active, working_hour__isnull=False)
        
        user_dict = {}
        for presence in presences:
            user = presence.employee
            if user not in user_dict:
                user_dict[user] = 0
            if presence.working_hour is not None:
                user_dict[user] += presence.working_hour
            else:
                user_dict[user] += 0
            # user_dict[user] += presence.working_hour
        
        asc_sorted_users = sorted(user_dict.items(), key=lambda x: x[1], reverse=True)[:5]
        desc_sorted_users = sorted(user_dict.items(), key=lambda x: x[1], reverse=False)[:5]
        
        data_asc = []
        for user, working_hour in asc_sorted_users:
            data_asc.append({
                "id" : user.pk,
                "name": user.name,
                "working_hour": working_hour
            })
        
        data_desc = []
        for user, working_hour in desc_sorted_users:
            data_desc.append({
                "id" : user.pk,
                "name": user.name,
                "working_hour": working_hour
            })
        
        return Response({
            "top_five": data_asc,
            "low_five": data_desc
        })


class UserSearch(APIView):
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        users = User.objects.all().order_by('name')
        return users
    
    def get(self, request, *args, **kwargs):
        querySet = User.objects.all().order_by('name')
        
        name = self.request.query_params.get('name', None)
        active = self.request.query_params.get('active', None)
        roles = self.request.query_params.get('roles', None)
        division = self.request.query_params.get('division', None)
        active = self.request.query_params.get('active', None)

        if name:
            querySet=querySet.filter(name__icontains=name)
        if active:
            querySet=querySet.filter(is_active=active)
        if roles:
            querySet=querySet.filter(roles__contains=roles)
        if division:
            querySet=querySet.filter(division__contains=division)
        if active:
            querySet=querySet.filter(is_active=active)

        serializer = UserDetailsSerializer(querySet, many=True)

        return Response(serializer.data)

class EmployeeBirth(APIView):
    def get(self, request, month):
        try:
            users = User.objects.filter(birth_date__month=month, is_active=True).order_by('birth_date__day')
            serializer = UserBirthdaySerializers(users, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class EmployeeContractEnd(APIView):
    def get(self, request, year):
        try:
            today = datetime.now()
            current_month = today.month
            previous_month = (current_month - 1) if current_month != 1 else 12
            next_month = (current_month + 1) if current_month != 12 else 1
            users = User.objects.filter( contract_end__month__range=(previous_month, next_month), contract_end__year=year, is_active=True)
            serializer = UserContractSerializers(users, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UserProfile(APIView):

    def get(self, request, *args, **kwargs):
        emp_id = request.user.pk
        try:
            profile = User.objects.get(pk=emp_id)
            
            serializer = UserDetailsSerializer(profile)
            
            return Response(serializer.data)
        except User.DoesNotExist:
            # Tangani jika profil pengguna tidak ditemukan
            return Response({'message': 'Profil pengguna tidak ditemukan'}, status=404)

class UserSearchContract(APIView):
    serializer_class = UserContractSerializers

    def get_queryset(self):
        users = User.objects.all().order_by('contract_end')
        return users
    
    def get(self, request, *args, **kwargs):
        querySet = User.objects.all().order_by('contract_end')
        
        name = self.request.query_params.get('name', None)
        contract_start = self.request.query_params.get('contract_start', None)
        contract_end = self.request.query_params.get('contract_end', None)
        active_user = self.request.query_params.get('active_user', None)

        if name:
            querySet=querySet.filter(name__icontains=name)
        if active_user:
            querySet=querySet.filter(is_active=active_user)
        if contract_start:
            querySet=querySet.filter(roles__contains=contract_start)
        if contract_end:
            querySet=querySet.filter(division__contains=contract_end)

        serializer = UserContractSerializers(querySet, many=True)

        return Response(serializer.data) 

class UserSearchView(APIView):
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        users = User.objects.all().order_by('username')
        return users
    
    def get(self, request, *args, **kwargs):
        querySet = User.objects.all().order_by('username')
        
        name = self.request.query_params.get('name', None)

        if name:
            querySet=querySet.filter(name__icontains=name)

        serializer = UserDetailsSerializer(querySet, many=True)

        return Response(serializer.data) 


class UserPasswordReset(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            encode_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            
            reset_url = reverse(
                "reset-password",
                kwargs={"encoded_pk":encode_pk, "token":token}
            )

            reset_url = reset_url

            return Response(
                {
                    "Message": reset_url
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "Message":
                    "User Does not exist"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"kwargs":kwargs}
        )

        serializer.is_valid(raise_exception=True)

        return Response(
            {"Message" : "Password reset complete"},
            status = status.HTTP_200_OK
        )

class ChangePasswordAPIView(APIView):
    def post(self, request):
        # Mendapatkan data permintaan
        old_password = request.data.get('old_password')
        new_password1 = request.data.get('new_password1')
        new_password2 = request.data.get('new_password2')
        
        if new_password1 != new_password2:
            return Response({'message': 'New passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        
        if not check_password(old_password, user.password):
            return Response({'message': 'Invalid old password.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.password = make_password(new_password1)
        user.save()
        
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
    
class UserNotesSpecific(APIView):

    def get(self, request, *args, **kwargs):
        employee = self.request.query_params.get('employee', None)
        user = self.request.user
        if user.roles == 'hrd':
            if employee:
                user_notes = UserNotes.objects.get_or_create(employee=User.objects.get(id=employee))
                serializer = UserNotesSerializers(user_notes, many=True)

                return Response(serializer.data)
            else: 
                return Response({'message': 'Masukan params employee.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Tidak dapat mengakses API ini.'}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        user = self.request.user
        data = request.data
        employee = data.get('employee')
        notes_employee = data.get('notes_employee')
        if user.roles == 'hrd':
            note_emp = UserNotes.objects.get(employee=User.objects.get(id=employee))
            note_emp.notes = notes_employee
            note_emp.save()
            return Response({'message': 'Berhasil mengedit notes.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Tidak dapat mengakses API ini.'}, status=status.HTTP_403_FORBIDDEN)

class UserBerkasAPIView(APIView):

    def get(self, request, *args, **kwargs):
        employee = self.request.query_params.get('employee', None)
        if employee:
            user_berkas = UserBerkas.objects.get_or_create(employee=User.objects.get(id=employee))
            serializer = UserBerkasSerializer(user_berkas, many=True)

            return Response(serializer.data[0], status=status.HTTP_200_OK)
        else: 
            return Response({'message': 'Masukan params employee.'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # user = self.request.user
        data = request.data
        employee = data.get('employee')
        nik = data.get('nik', None)
        file_ktp = data.get('file_ktp', None)
        no_npwp = data.get('no_npwp', None)
        file_npwp = data.get('file_npwp', None)
        no_bpjs = data.get('no_bpjs', None)
        file_bpjs = data.get('file_bpjs', None)
        user_berkas = UserBerkas.objects.get(employee=User.objects.get(id=employee))
        user_berkas.nik = nik
        user_berkas.berkas_ktp = file_ktp
        user_berkas.no_npwp = no_npwp
        user_berkas.berkas_npwp = file_npwp
        user_berkas.no_bpjs = no_bpjs
        user_berkas.berkas_bpjs = file_bpjs
        user_berkas.save()
        return Response({'message': 'Berhasil!',
                         }, status=status.HTTP_201_CREATED)

class UserBankAPIView(APIView):

    def get(self, request, *args, **kwargs):
        employee = self.request.query_params.get('employee', None)
        if employee:
            user_bank = UserBank.objects.get_or_create(employee=User.objects.get(id=employee))
            serializer = UserBankSerializer(user_bank, many=True)

            return Response(serializer.data[0], status=status.HTTP_200_OK)
        else: 
            return Response({'message': 'Masukan params employee.'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # user = self.request.user
        data = request.data
        employee = data.get('employee')
        nomor = data.get('nomor', None)
        bank_id = data.get('bank_id', None)
        user_bank = UserBank.objects.get(employee=User.objects.get(id=employee))
        user_bank.nomor = nomor
        user_bank.bank = Bank.objects.get(id=bank_id)
        user_bank.save()
        return Response({'message': 'Berhasil!',
                         }, status=status.HTTP_201_CREATED)
    
class CertificatePieChartAPIView(APIView):
    def get(self, request):
        data = UserCertificate.objects.values('certificate_level').annotate(count=Count('certificate_level'))

        # Menggunakan serializer untuk mengonversi data ke format yang sesuai
        serializer = UserCertificatePieChartSerializer(data, many=True)

        # Menghitung total jumlah sertifikat
        total_certificates = UserCertificate.objects.count()

        # Menghitung persentase
        for item in serializer.data:
            item['percentage'] = (item['count'] / total_certificates) * 100

        return Response(serializer.data)

class UserCertificateAPIView(APIView):

    def get(self, request, *args, **kwargs):
        employee = self.request.query_params.get('employee', None)
        if employee:
            user_study = UserCertificate.objects.get_or_create(employee=User.objects.get(id=employee))
            serializer = UserCertificateSerializer(user_study, many=True)

            return Response(serializer.data[0], status=status.HTTP_200_OK)
        else: 
            return Response({'message': 'Masukan params employee.'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # user = self.request.user
        data = request.data
        employee = data.get('employee')
        institute_name = data.get('institute_name', None)
        study_program = data.get('study_program', None)
        certificate_level = data.get('certificate_level', None)
        foto = data.get('foto', None)
        transkrip = data.get('transkrip', None)
        user_study = UserCertificate.objects.get(employee=User.objects.get(id=employee))
        user_study.institute_name = institute_name
        user_study.study_program = study_program
        user_study.certificate_level = certificate_level
        user_study.foto = foto
        user_study.transkrip = transkrip
        user_study.save()
        return Response({'message': 'Berhasil!',
                         }, status=status.HTTP_201_CREATED)

class UserContractAPIView(APIView):

    def get(self, request, *args, **kwargs):
        employee = self.request.query_params.get('employee', None)
        if employee:
            user_contract = UserContract.objects.filter(employee=User.objects.get(id=employee))
            serializer = UserContractListSerializer(user_contract, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else: 
            return Response({'message': 'Masukan params employee.'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        employee_id = data.get('employee')
        contract_start = data.get('contract_start', None)
        contract_end = data.get('contract_end', None)

        try:
            if contract_start is not None and contract_end is not None:
                contract_start = datetime.strptime(contract_start, '%d-%m-%Y').strftime('%Y-%m-%d')
                contract_end = datetime.strptime(contract_end, '%d-%m-%Y').strftime('%Y-%m-%d')

                UserContract.objects.create(
                    employee=User.objects.get(id=employee_id),
                    contract_start=contract_start, contract_end= contract_end
                )

                return Response({'message': 'Berhasil!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Gagal! Lengkapi data kontrak terlebih dahulu'}, status=status.HTTP_403_FORBIDDEN)
        except ValueError:
            return Response({'message': 'Format tanggal tidak valid. Gunakan format DD-MM-YYYY.'}, status=status.HTTP_400_BAD_REQUEST)