from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from datetime import timedelta
from .utils import CustomJWTAuthentication
from .serializers import SignUpSerializer, LogInSerializer

# Create your views here.
class SignUpView(viewsets.ViewSet):
    """
    User Signup Endpoint

    Register as a new user. 
    """
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=SignUpSerializer, responses={201: 'CREATED', 400: 'BAD REQUEST'})
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = {
                "success": True,
                "status": 201,
                "message": "User sign up successful",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            response_data = {
                "success": False,
                "status": 400,
                "message": "Validation error: Invalid or empty fields",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class LogInView(viewsets.ViewSet):
    """
    User Login Endpoint

    User log in with their email and password.
    """
    serializer_class = LogInSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LogInSerializer, responses={200: 'OK', 401: 'UNAUTHORIZED', 400: 'BAD_REQUEST'})
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                access_token = AccessToken.for_user(user)
                response_data = {
                    'success': True,
                    'status': 200,
                    'message': 'Login successful',
                    'access_token': str(access_token),
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'success': False,
                    'status': 401,
                    'message': 'Invalid credentials',
                }
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            response_data = {
                'success': False,
                'status': 400,
                'message': 'Validation error: Email or password field is invalid or empty',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class LogOutView(viewsets.ViewSet):
    """
    User Logout Endpoint

    Logs out user by blacklisting their access token.
    """
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(responses={205: 'RESET CONTENT', 400: 'BAD REQUEST'})
    def create(self, request):
        try:
            token = request.auth
            if token:
                cache_key = CustomJWTAuthentication.get_cache_key(self, str(token))
                # Set timeout as per token expiry
                timeout = timedelta(hours=3).total_seconds()
                cache.set(cache_key, 'blacklisted', timeout=timeout)
                response_data = {
                    'success': True,
                    'status': 205,
                    'message': 'Logout successful',
                }
                return Response(response_data, status=status.HTTP_205_RESET_CONTENT)
            else:
                response_data = {
                    'success': False,
                    'status': 400,
                    'message': 'Invalid token',
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                'success': False,
                'status': 400,
                'message': str(e),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
