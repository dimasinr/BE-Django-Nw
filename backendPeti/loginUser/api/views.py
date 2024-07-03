from datetime import datetime
from django.shortcuts import render
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import login, authenticate


class Login(APIView):
    def post(self, request):
        User = get_user_model()
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Please fill all fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "Username tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        user = authenticate(username=username, password=password)
        status_cuti = False

        if user is not None:
            login(request, user)
            now = datetime.now().date()  
            if (now - user.employee_joined).days >= 365:  
                status_cuti = True
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'user_id': user.pk,
                'token': token.key,
                'username': user.username,
                'name': f"{user.first_name} {user.last_name}",
                'roles': user.roles,
                'status_cuti': status_cuti
            }
            return Response({"success": "Successfully logged in", "data": data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)