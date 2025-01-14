from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from datetime import timedelta
from threading import Thread
from utils import CustomJWTAuthentication, send_async_email, cache, general_logger
from .serializers import SignUpSerializer, LogInSerializer, ResetPasswordSerializer, ConfirmPasswordSerializer
from .models import UserModel, CustomPasswordResetToken

# Create your views here.
class SignUpView(viewsets.ViewSet):
    """
    User Signup Endpoint

    Register as a new user. 
    """
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=SignUpSerializer, responses={201: 'CREATED', 400: 'BAD REQUEST', 401: 'UNAUTHORIZED'})
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                access_token = AccessToken.for_user(user)
                response_data = {
                    'success': True,
                    'status': 200,
                    'message': 'Signup successful',
                    'first_name': serializer.data['first_name'],
                    'last_name': serializer.data['last_name'],
                    'access_token': str(access_token)
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    'success': False,
                    'status': 401,
                    'message': 'Invalid credentials',
                }
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            general_logger.error("An error occurred: %s", e)
            response_data = {
                "success": False,
                "status": 400,
                "message": "Validation error: Invalid input from user or empty fields",
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
                    'first_name': str(user.first_name),
                    'last_name': str(user.last_name),
                    'access_token': str(access_token)
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
            general_logger.error("An error occurred: %s", e)
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
            general_logger.error("An error occurred: %s", e)
            response_data = {
                'success': False,
                'status': 400,
                'message': "Validation error occured",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        

class ResetPasswordView(viewsets.ViewSet):
    """
        Password Reset Endpoint

        Initiate a password reset as a register user. 
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=ResetPasswordSerializer, responses={200: 'OK', 404: 'NOT FOUND', 500:'SERVER ERROR'})
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('email')
            user = UserModel.objects.get(email=email)
            token, _ = CustomPasswordResetToken.objects.get_or_create(user=user)
            email_subject = 'ELBIS Homes: Password Reset Request'
            email_body = f"""Dear {user},\n\nYou have requested a password reset. Use the following token to reset your password within the next 10 minutes before expiration:\n\nToken: {token.key}\n\nPS: Please ignore if you did not initiate this process.\n\nRegards,\nELBIS Homes"""
            recipient = [user.email]
            # Asynchronously handle send mail
            Thread(target=send_async_email, args=(email_subject, email_body, recipient)).start()
            response_data = {
                'success': True,
                'status': 200,
                'message': 'Password reset token has been sent to your mail.',
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except UserModel.DoesNotExist:
            response_data = {
                'success': False,
                'status': 404,
                'message': 'User does not exist!',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            general_logger.error("Exception error occurred: %s", e)
            response_data = {
                'success': False,
                'status': 500,
                'message': 'An error occurred, kindly contact support!',
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ConfirmPasswordView(viewsets.ViewSet):
    """
        Password Confirmation Endpoint

        Confirm the new password as a register user. 
    """
    serializer_class = ConfirmPasswordSerializer
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=ConfirmPasswordSerializer, responses={200: 'OK', 400: 'BAD REQUEST', 406: 'NOT ACCEPTABLE', 500:'SERVER ERROR'})
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            otp_token = serializer.validated_data.get('token')
            password = serializer.validated_data.get('password')
            token = CustomPasswordResetToken.objects.select_related('user').get(key=otp_token)
            if token.is_expired():
                token.delete()
                response_data = {
                    'success': False,
                    'status': 406,
                    'message': 'Token has expired!',
                }
                return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE)
            user = token.user
            user.set_password(password)
            user.save()
            token.delete()
            response_data = {
                'success': True,
                'status': 200,
                'message': 'Password has been reset successfully.',
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except CustomPasswordResetToken.DoesNotExist as e:
            general_logger.error("Token error occurred: %s", e)
            response_data = {
                'success': False,
                'status': 400,
                'message': 'Invalid token!',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            general_logger.error("Exception error occurred: %s", e)
            response_data = {
                'success': False,
                'status': 500,
                'message': 'An error occurred, kindly contact support!'
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        