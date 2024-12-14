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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users.views import SignUpView, LogInView, LogOutView
from properties.views import PropertyViewSet

# Swagger UI
schema_view = get_schema_view(
   openapi.Info(
      title="ELBIS Homes API",
      default_version='v1',
      description="Backend API for ELBIS Homes, a real estate platform to enhance Nigeria accommodation process.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="info@peteroyelegbin.com.ng"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'users/signup', SignUpView, basename="auth_signup")
router.register(r'users/login', LogInView, basename="auth_login")
router.register(r'users/logout', LogOutView, basename="auth_logout")
router.register(r'properties', PropertyViewSet, basename="manage-property")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/api/', include(router.urls)),
    # API DOCS URL
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
