from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Company, CustomUser
from .serializers import CompanySerializer, UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.utils.timezone import now
from django.contrib.auth import authenticate
# Create your views here.
# region Company

class CompanyViewSet(ModelViewSet):
  queryset = Company.objects.all()
  serializer_class = CompanySerializer

  def get_permissions(self):
    if self.action in ['list', 'retrieve']:
      return [IsAdminUser()]
    return super().get_permissions()

  def get_queryset(self):
    user = self.request.user
    if user.is_superuser:
      return Company.objects.all()
    return Company.objects.filter(id=user.company.id)
  
# endregion

# region CustomUser
class CustomUserViewSet(ModelViewSet):
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated]

  def get_permissions(self):
    if self.action in ['list', 'retrieve']:
      return [IsAdminUser()]
    return super().get_permissions()

  def get_queryset(self):
    user = self.request.user
    if user.is_superuser:
      return CustomUser.objects.all()
    return CustomUser.objects.filter(company=user.company)
# endregion


# region auth

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Extract credentials
        username = request.data.get('username')
        password = request.data.get('password')
        client_ip = self.get_client_ip(request)

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user:
            if not user.is_active:
                return Response({"error": "Account is inactive."}, status=403)

            # Update user-specific fields
            user.last_login_ip = client_ip
            user.failed_login_attempts = 0  # Reset failed login attempts
            user.last_login = now()
            user.save()

            # Get or create a token for the user
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
                "role": user.role,
                "company": user.company.name if user.company else None,
            })

        # Handle failed authentication
        try:
            failed_user = CustomUser.objects.get(username=username)
            failed_user.failed_login_attempts += 1
            failed_user.last_failed_login = now()
            failed_user.save()
        except CustomUser.DoesNotExist:
            pass  # Ignore if user doesn't exist to prevent enumeration attacks

        return Response({"error": "Invalid credentials."}, status=401)

    def get_client_ip(self, request):
        """
        Helper method to extract client IP address from the request.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


