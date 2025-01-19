"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users.views import UsersView, SignUpView, LogInView, LogOutView, ResetPasswordView, ConfirmPasswordView
from properties.views import PropertyViewSet, FavoriteViewSet, EnquiryViewSet

# Swagger UI
schema_view = get_schema_view(
   openapi.Info(
      title="ELBIS Homes API",
      default_version='v1',
      description="ELBIS Homes API is a Django-based server-side application that handles user authentication, property data management, and integration with a MySQL database. It is built using Python, Django Rest Framework, and JWT authentication, providing a robust and scalable foundation for real estate platforms.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(name="Peter Oyelegbin", url="https://peteroyelegbin.com.ng", email="info@peteroyelegbin.com.ng"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter(trailing_slash=False)
router.register(r'users/manage', UsersView, basename="manage_user")
router.register(r'users/signup', SignUpView, basename="signup")
router.register(r'users/login', LogInView, basename="login")
router.register(r'users/logout', LogOutView, basename="logout")
router.register(r'users/password/reset', ResetPasswordView, basename="password_reset")
router.register(r'users/password/confirm', ConfirmPasswordView, basename="password_confirm")
router.register(r'properties', PropertyViewSet, basename="manage_property")
router.register(r'favorites', FavoriteViewSet, basename="manage_favorites")
router.register(r'enquiry', EnquiryViewSet, basename="make_enquiry")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/api/', include(router.urls)),
    # API DOCS URL
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
