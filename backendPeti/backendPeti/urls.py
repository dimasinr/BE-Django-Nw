from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from noteHR.api.views import get_cuti
from userapp.api import views
from attendanceEmployee.api.views import (
    AttendanceAPISearch, 
    TopAttendanceAPIView, 
    AttendanceAPICompare, 
    AttendanceAPIAnalisis
)
from userapp.api.views import (
     EmployeeBirth, 
     UserSearch, 
     UserSearchView, 
     UserPasswordReset, 
     ResetPassword, 
     UserSearchContract, 
     UserWorkHourAPIView, 
     EmployeeContractEnd, 
     ChangePasswordAPIView, 
     CertificatePieChartAPIView
)
from calendarDash.api.views import WeekTotals, post_delete_calendar
from presenceEmployee.api.views import (
    PresenceAPIAnalisis, 
    PresenceAPICompare, 
    PresenceSearch, 
    TopPresenceAPIView, 
    PresenceStatistikUser, 
    StatistikPresenceInMonth, 
    StatistikSubmissionEmployeeInMonth, 
    PresenceWFHGenerate, PresenceLocked
)
from submisssion.api.views import (
    CalendarSubmissionView, 
    SubmissionIzin, 
    send_notification_api
)
from noteHR.api.views import post_delete_notes

urlpatterns = (
    [
    path(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),
    # path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/reset-password/', UserPasswordReset.as_view(), name='reset-password'),
    path('api/send-notification/', send_notification_api, name='send_notification'),

]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

)