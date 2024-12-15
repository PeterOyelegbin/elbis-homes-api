from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Property
from .serializers import PropertySerializer

# Create your views here.
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    parser_classes = (MultiPartParser, FormParser)
    search_fields = ['price']

    def get_permissions(self):
        """
        Return the appropriate permissions based on the action.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('search', openapi.IN_QUERY, description="Search by price", type=openapi.TYPE_STRING),], responses={200: 'OK', 404: 'NOT FOUND'})
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
            print(headers)
            response_data = {
                "success": True,
                "status": 201,
                "message": "Property added successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            response_data = {
                "success": False,
                "status": 400,
                "message": f"Validation error: {e}",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: 'OK', 404: 'NOT FOUND'})
    def retrieve(self, request, pk=None):
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
            response_data = {
                "success": False,
                "status": 400,
                "message": f"Validation error: {e}",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PropertySerializer, responses={200: 'OK', 400: 'BAD REQUEST', 404: 'NOT FOUND'})
    def partial_update(self, request, pk=None, *args, **kwargs):
        return self.update(request, pk, partial=True, *args, **kwargs)

    @swagger_auto_schema(responses={204: 'NO CONTENT', 404: 'NOT FOUND'})
    def destroy(self, request, pk=None):
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
