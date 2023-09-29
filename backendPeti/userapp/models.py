import uuid
from django import utils
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from datetime import date, datetime
from django.db.models import Sum
from backendPeti.helper.commons import TrackableDateModel
from bank.models import Bank
from backendPeti.helper.file import RandomFileName

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_active, is_staff, is_superuser, **extrafields):
        now = timezone.now()
        if not username:
            raise ValueError("the given username is not valid")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_active=is_active, 
                            is_staff=is_staff, is_superuser=is_superuser, date_joined=now, **extrafields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password, **extrafields):
        return self._create_user(username, email, password, is_active=True, is_staff=False, is_superuser=False, **extrafields)

    def create_superuser(self, username, email, password, **extrafields):
        user = self._create_user(username, email, password, is_active=True, is_staff=True, 
                                is_superuser=True, **extrafields)
        user.save(using=self._db)

        return user     

class User(AbstractBaseUser, PermissionsMixin):
        username= models.CharField(max_length=120, unique=True)
        email = models.EmailField(max_length=250, unique=True)
        first_name = models.CharField(max_length=30, blank=True, null=True)
        last_name = models.CharField(max_length=30, blank=True, null=True)
        name = models.CharField(max_length=255, blank=True, null=True)
        foto = models.ImageField(upload_to=RandomFileName('user/foto/'), null=True, blank=True)
        division = models.CharField(max_length=255, blank=True, null=True)
        status_employee = models.CharField(max_length=255, blank=True, null=True)
        is_active = models.BooleanField(default=True) #karyawan aktif
        is_staff = models.BooleanField(default=False)
        is_superuser = models.BooleanField(default=False)
        employee_joined = models.DateField(null=True, blank=True)
        employee_ended = models.DateField(null=True, blank=True)
        date_joined = models.DateTimeField(default=timezone.now) #karyawan mulai bekerja
        receive_newsletter = models.BooleanField(default=False)
        sisa_cuti = models.IntegerField( blank=True, null=True)
        birth_date = models.DateField(blank=True, null=True)
        address = models.CharField(max_length=300, blank=True, null=True)
        roles = models.CharField(max_length=30, blank=True, null=True)
        gender = models.CharField(max_length=30, blank=True, null=True)
        religion = models.CharField(max_length=30, blank=True, null=True)
        employee_code = models.CharField(max_length=250, blank=True, null=True, default="EmpId")
        contract_start = models.DateField(blank=True, null=True)
        contract_end = models.DateField(blank=True, null=True)
        contract_time = models.CharField(max_length=250, blank=True, null=True)
        alamat = models.TextField(null=True, blank=True, default='')
        status_kawin = models.CharField(max_length=250, null=True, blank=True, default='belum menikah') 
        no_hp = models.CharField(max_length=250, null=True, blank=True) 

        objects = UserManager()

        def save(self, *args, **kwargs):
            if(self.first_name != None and self.last_name != None):
                self.name = (self.first_name + ' ' + self.last_name)
                super(User, self).save(*args, **kwargs)
            else:
                super(User, self).save(*args, **kwargs)

            if(self.contract_start != None and self.contract_end != None):
                # x = date(2020, 5, 17)
                # y = date(2020, 8, 4)
                vas = self.contract_end - self.contract_start
                years = vas.days // 365
                months = (vas.days - years *365) // 30
                days = (vas.days - years * 365 - months*30)
                tah = str(years)
                bul = str(months)
                har = str(days)
                contract_times = tah + ' Tahun ' + bul + ' Bulan ' + har + ' Hari'
                # print(contract_times)
                # print(tah)
                self.contract_time = contract_times
                super(User, self).save(*args, **kwargs)

        def get_total_work_hour(self):
            total_hour = self.working_hours.aggregate(total_work_hour=Sum('working_hour'))['total_work_hour']
            return total_hour if total_hour is not None else 0
            
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS =  [ 'email', ]

class UserRoles(models.Model):
    roles = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.roles

class UserDivision(models.Model):
    division = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.division

    
class UserBank(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    nomor = models.CharField(max_length=255, null=True, blank=True)
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.nomor

class UserCertificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    institute_name = models.CharField(max_length=255, null=True, blank=True)
    study_program = models.CharField(max_length=255, null=True, blank=True)
    certificate_level = models.CharField(max_length=255, null=True, blank=True, default='SMA/SMK')
    foto = models.ImageField(upload_to=RandomFileName('certificate/'), null=True, blank=True)
    transkrip = models.ImageField(upload_to=RandomFileName('certificate/transkrip/'), null=True, blank=True)

    def __str__(self):
        return self.institute_name
    
class UserBerkas(TrackableDateModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    nik = models.CharField(max_length=255, null=True, blank=True)
    berkas_ktp = models.FileField(upload_to=RandomFileName('ktp/'), null=True, blank=True)
    no_npwp = models.CharField(max_length=255, null=True, blank=True)
    berkas_npwp = models.FileField(upload_to='npwp/', null=True, blank=True)
    no_bpjs = models.CharField(max_length=255, null=True, blank=True)
    berkas_bpjs = models.FileField(upload_to=RandomFileName('bpjs/'), null=True, blank=True)
    
    def __str__(self):
        return self.nik

class UserContract(TrackableDateModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    contract_start = models.DateField(blank=True, null=True)
    contract_end = models.DateField(blank=True, null=True)
    contract_time = models.CharField(max_length=250, blank=True, null=True)

    def save(self, *args, **kwargs):
        contract_start_date = datetime.strptime(str(self.contract_start), '%Y-%m-%d')
        contract_end_date = datetime.strptime(str(self.contract_end), '%Y-%m-%d')
        vas =  contract_end_date - contract_start_date
        years = vas.days // 365
        months = (vas.days - years *365) // 30
        days = (vas.days - years * 365 - months*30)
        tah = str(years)
        bul = str(months)
        har = str(days)
        contract_times = tah + ' Tahun ' + bul + ' Bulan ' + har + ' Hari'
        # print(contract_times)
        # print(tah)
        self.contract_time = contract_times
        super(UserContract, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.employee.name

class Certificate(TrackableDateModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=255, null=False, blank=False)
    berkas = models.FileField(upload_to=RandomFileName('sertifikat/'), null=True, blank=True)

    def __str__(self):
        return self.nama

class UserAdditionalData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    cv = models.FileField(upload_to=RandomFileName('cv/'), null=True, blank=True)
    sertifikat = models.ManyToManyField(Certificate)

    def __str__(self):
        return self.id

class Log(models.Model):
    message = models.TextField()
    action = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.message + ' - '+ str(self.timestamp)

class UserNotes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    notes = models.TextField(null=True, blank=True, default='')
    created_at = models.DateTimeField(default=utils.timezone.now)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.employee.name