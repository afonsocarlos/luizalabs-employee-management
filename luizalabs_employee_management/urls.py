"""luizalabs_employee_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path
from rest_framework import permissions, routers
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from api import views as api_views


router = routers.DefaultRouter()
router.register(r'employees', api_views.EmployeeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_jwt_token, name='api-token-auth'),
    path('api-token-refresh/', refresh_jwt_token, name='api-token-refresh'),
    path('api/v1/', include(router.urls)),
    path('docs/', include_docs_urls(
        title='Luizalabs Employee Management API',
        authentication_classes=[],
        permission_classes=[permissions.AllowAny])
         ),
]
