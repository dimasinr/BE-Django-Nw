from rest_framework import serializers
from allauth.account.adapter import get_adapter
from backendPeti import settings
from .models import Log, User, UserBank, UserBerkas, UserCertificate, UserContract, UserNotes, UserRoles, UserDivision
from allauth.account.utils import setup_user_email
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=settings.ACCOUNT_EMAIL_REQUIRED)
    first_name = serializers.CharField(required=False, write_only=True)
    last_name = serializers.CharField(required=False, write_only=True)
    name = serializers.CharField(required=False, write_only=True)
    sisa_cuti = serializers.CharField(required=False, write_only=True)
    roles = serializers.CharField(required=False, write_only=True)

    password1 = serializers.CharField(required=False, write_only=True)
    password2 = serializers.CharField(required=False, write_only=True)

    def validate_password1(self, password):
        return get_adapter().clean_password(password)
    
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                ("The two password fields didn't match.")
            )
        return data
    
    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'first_name' : self.validated_data.get('first_name', ''),
            'last_name' : self.validated_data.get('last_name', ''),
            'name' : self.validated_data.get('name', ''),
            'division' : self.validated_data.get('division', ''),
            'sisa_cuti' : self.validated_data.get('sisa_cuti', ''),
            'roles' : self.validated_data.get('roles', ''),
            'address' : self.validated_data.get('address', ''),
            'user_type' : self.validated_data.get('user_type', ''),
            'password1' : self.validated_data.get('password1', ''),
            'email' : self.validated_data.get('email', ''),
            'gender' : self.validated_data.get('gender', ''),
            'religion' : self.validated_data.get('religion', ''),
            'contract_start' : self.validated_data.get('contract_start', ''),
            'contract_end' : self.validated_data.get('contract_end', ''),
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user 

        user.save()
        return user

class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User Model w/o password
    """
    class Meta:
        model = User
        fields = ('pk', 'employee_code', 'username', 'email', 'first_name', 'last_name', 'is_active','alamat', 'status_kawin', 'no_hp', 'name', 'division', 'employee_joined', 'employee_ended', 'birth_date',
                    'sisa_cuti', 'roles', 'foto', 'gender', 'religion', 'status_employee', 'contract_start', 'contract_end', 'contract_time')
        # read_only_fields = ('email', )

class UserSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'employee_code', 'username', 'name', 'division')
        # read_only_fields = ('email', )

class UserContractSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk','employee_code', 'name', 'foto', 'division', 'employee_joined', 'employee_ended', 'contract_start', 'contract_end', 'contract_time', 'is_active' )

class UserBirthdaySerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk','employee_code', 'name', 'division', 'birth_date' )

class UserRolesSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = '__all__' 
        
class UserTotalDataIOSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'is_active')
        # fields = '__all__' 

class UserDivisionSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserDivision
        fields = '__all__' 

class UserNotesSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserNotes
        exclude = ['employee']

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'

class UserBerkasSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBerkas
        fields = '__all__'

class UserBankSerializer(serializers.ModelSerializer):
    employee = UserSubSerializer(read_only=True)
    class Meta:
        model = UserBank
        fields = '__all__'
        depth = 1

class UserCertificateSerializer(serializers.ModelSerializer):
    employee = UserSubSerializer(read_only=True)
    class Meta:
        model = UserCertificate
        fields = '__all__'
        depth = 1

class UserCertificatePieChartSerializer(serializers.Serializer):
    certificate_level = serializers.CharField()
    count = serializers.IntegerField()
    
class UserContractListSerializer(serializers.ModelSerializer):
    employee = UserSubSerializer(read_only=True)
    class Meta:
        model = UserContract
        fields = '__all__'
        depth = 1

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        # model = User
        fields = ("email")

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        min_length=4,
    )
    class Meta:
        # model = User
        fields = ("password")

    def validate(self, data):
        password = data.get("password")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing Data")
        
        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")

        user.set_password(password)
        user.save()
        return data