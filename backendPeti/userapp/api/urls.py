from django.conf.urls import url, include
from .views import (
    UserApiView, 
    UserNotesSpecific, 
    UserViewId, 
    UserRole, 
    UserDivisionView,
    UserProfile,
    UserBerkasAPIView,
    UserBankAPIView,
    UserCertificateAPIView,
    UserContractAPIView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employees', UserViewId, basename='employees'),
router.register('employees-roles', UserRole, basename='employees-roles'),
router.register('employees-division', UserDivisionView, basename='employees-division'),

urlpatterns = [
    url('users', UserApiView.as_view()),
    url('profile', UserProfile.as_view()),
    url('notes', UserNotesSpecific.as_view()),
    url('berkas', UserBerkasAPIView.as_view()),
    url('bank', UserBankAPIView.as_view()),
    url('pendidikan', UserCertificateAPIView.as_view()),
    url('annual-contract', UserContractAPIView.as_view()),
    url('', include(router.urls)),
]