"""CRM_EPIC_Events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from accounts.views import AccountViewSet
from additional_data.views import CompanyViewSet, LocationViewSet
from persons.views import PersonViewSet
from products.views import ContractViewSet, EventViewSet


router = routers.SimpleRouter()
router.register("clients", PersonViewSet, basename="clients")
router.register("companies", CompanyViewSet, basename="companies")
router.register("contracts", ContractViewSet, basename="contracts")
router.register("employees", AccountViewSet, basename="employees")
router.register("events", EventViewSet, basename="events")
router.register("locations", LocationViewSet, basename="locations")


def trigger_error(request):
    """Test d'erreur avec Sentry."""
    division_by_zero = 1 / 0
    return division_by_zero


urlpatterns = [
    path("crm_ee/", include("rest_framework.urls", namespace="rest_famework")),
    path("admin/", admin.site.urls),
    path("crm_ee/", include(router.urls)),
    path("crm_ee/tokens/", TokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("crm_ee/tokens/refresh/", TokenRefreshView.as_view(),
         name="token_refresh"),
    path("crm_ee/sentry-debug-test/", trigger_error)
]
