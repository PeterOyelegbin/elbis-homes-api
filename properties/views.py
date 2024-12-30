from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from threading import Thread
from utils import send_async_email, general_logger
from .models import Property, Favorite
from .serializers import PropertySerializer, FavoriteSerializer, EnquirySerializer

# Create your views here.
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    parser_classes = (MultiPartParser, FormParser)
    search_fields = ['bedroom', 'property_type', 'price', 'state', 'status']

    def get_permissions(self):
        """
        Return the appropriate permissions based on the action.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('search', openapi.IN_QUERY, description="Search by bedroom, property_type, price, state, or status", type=openapi.TYPE_STRING),], responses={200: 'OK', 404: 'NOT FOUND'})
    def list(self, request, *args, **kwargs):
        try:
            objects = self.filter_queryset(self.get_queryset())
            if not objects:
                raise Property.DoesNotExist
            serializer = self.get_serializer(objects, many=True)
            response_data = {
                "success": True,
                "status": 200,
                "message": "Properties listed successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Property.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "No records found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=PropertySerializer, responses={201: 'CREATED', 400: 'BAD REQUEST'})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            response_data = {
                "success": True,
                "status": 201,
                "message": "Property added successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            general_logger.error("An error occurred: %s", e)
            response_data = {
                "success": False,
                "status": 400,
                "message": "Validation error: Invalid input from user or empty fields",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: 'OK', 404: 'NOT FOUND'})
    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            instance = Property.objects.get(pk=pk)
            serializer = self.get_serializer(instance)
            response_data = {
                "success": True,
                "status": 200,
                "message": "Property retrieved successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Property.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Property does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=PropertySerializer, responses={200: 'OK', 400: 'BAD REQUEST', 404: 'NOT FOUND'})
    def update(self, request, pk=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = Property.objects.get(pk=pk)
            if 'cover_image' in request.FILES:
                if instance.cover_image:
                    instance.cover_image.delete()
            if 'bedroom_image' in request.FILES:
                if instance.bedroom_image:
                    instance.bedroom_image.delete()
            if 'bathroom_image' in request.FILES:
                if instance.bathroom_image:
                    instance.bathroom_image.delete()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = {
                "success": True,
                "status": 200,
                "message": "Property updated successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Property.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Property does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            general_logger.error("An error occurred: %s", e)
            response_data = {
                "success": False,
                "status": 400,
                "message": "Validation error: Invalid input from user or empty fields",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PropertySerializer, responses={200: 'OK', 400: 'BAD REQUEST', 404: 'NOT FOUND'})
    def partial_update(self, request, pk=None, *args, **kwargs):
        return self.update(request, pk, partial=True, *args, **kwargs)

    @swagger_auto_schema(responses={204: 'NO CONTENT', 404: 'NOT FOUND'})
    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            instance = Property.objects.get(pk=pk)
            instance.cover_image.delete()
            instance.bedroom_image.delete()
            instance.bathroom_image.delete()
            instance.delete()
            response_data = {
                "success": True,
                "status": 204,
                "message": "Property deleted successfully",
            }
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Property.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Property does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        

class FavoriteViewSet(viewsets.ViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Favorite.objects.none()
        return Favorite.objects.filter(user=self.request.user)

    @swagger_auto_schema(responses={200: 'OK', 404: 'NOT FOUND'})
    def list(self, request, *args, **kwargs):
        try:
            favorites = self.get_queryset()
            if not favorites:
                raise Favorite.DoesNotExist
            serializer = FavoriteSerializer(favorites, many=True)
            response_data = {
                "success": True,
                "status": 200,
                "message": "Favorites listed successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Favorite.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "No records found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(request_body=FavoriteSerializer, responses={201: 'CREATED', 400: 'BAD REQUEST', 404: 'NOT FOUND'})
    def create(self, request, *args, **kwargs):
        serializer = FavoriteSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            property_id = serializer.validated_data['property_id']
            property = Property.objects.get(pk=property_id)
            user = request.user
            Favorite.objects.get_or_create(user=user, property=property)
            response_data = {
                "success": True,
                "status": 201,
                "message": "Property added to favorite",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Property.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Property does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            general_logger.error("An error occurred: %s", e)
            response_data = {
                "success": False,
                "status": 400,
                "message": "Validation error: an error occured",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(responses={204: 'NO CONTENT', 404: 'NOT FOUND'})
    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            property = Property.objects.get(pk=pk)
            user = request.user
            favorite = Favorite.objects.get(user=user, property=property)
            favorite.delete()
            response_data = {
                "success": True,
                "status": 204,
                "message": "Favorite deleted successfully",
            }
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Property.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Property does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Favorite.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Favorite does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        

class EnquiryViewSet(viewsets.ViewSet):
    serializer_class = EnquirySerializer
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(request_body=EnquirySerializer, responses={200: 'OK', 400: 'BAD REQUEST', 500: 'SERVER ERROR'})
    def create(self, request, *args, **kwargs):
        serializer = EnquirySerializer(data=request.data)
        if serializer.is_valid():
            try:
                auth_user = request.user
                email_subject = f'Enquiry from {auth_user.first_name} {auth_user.last_name}'
                email_body = serializer.validated_data['message']
                email_recipient = ['test@peteroyelegbin.com.ng']
                email_header = {'Reply-To': auth_user.email}
                # Asynchronously handle send mail
                Thread(target=send_async_email, args=(email_subject, email_body, email_recipient, email_header)).start()
                response_data = {
                    "success": True,
                    "status": 200,
                    "message": "Message successfully sent",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                general_logger.error("An error occurred: %s", e)
                response_data = {
                    "success": False,
                    "status": 500,
                    "message": "An error occurred, kindly contact the support team.",
                }
                return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response_data = {
                "success": False,
                "status": 400,
                "message": "Message field is required and must be at least 10 characters",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        