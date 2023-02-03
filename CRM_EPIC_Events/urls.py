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

# from accounts.admin import manager_admin_site, webmaster_admin_site
from accounts.views import AccountViewSet
from additional_data.views import CompanyViewSet, LocationViewSet
from persons.views import PersonViewSet
from products.views import ContractViewSet, EventViewSet


router = routers.SimpleRouter()
router.register("events", EventViewSet, basename="events")
router.register("contracts", ContractViewSet, basename="contracts")
router.register("clients", PersonViewSet, basename="clients")
router.register("companies", CompanyViewSet, basename="companies")
router.register("locations", LocationViewSet, basename="locations")
router.register("employees", AccountViewSet, basename="employees")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("crm_ee/", include(router.urls)),
]
