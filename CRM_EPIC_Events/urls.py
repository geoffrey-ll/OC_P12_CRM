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
# from rest_framework_nested import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from accounts.views import AccountView
from products.views import ContractViewSet, EventViewSet


router = routers.SimpleRouter()
router.register("events", EventViewSet, basename="events")
router.register("contracts", ContractViewSet, basename="contracts")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("crm_ee/signup/", AccountView.as_view(), name="signup"),
    # path("crm_ee/logout/", include("rest_framework.urls")),
    # path("crm_ee/tokens/", TokenObtainPairView.as_view(),
    #      name="token_obtain_par"),
    # path("crm_ee/tokens/refresh/", TokenRefreshView.as_view(),
    #      name="token_refresh"),
    path("crm_ee/", include(router.urls)),
]
