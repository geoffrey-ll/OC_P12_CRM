from django.contrib.admin.apps import AdminConfig


class WebMasterAdminConfig(AdminConfig):

    default_site = "CRM_EPIC_Events.admin.WebMasterAdminSite"


class ManagerAdminConfig(AdminConfig):

    default_site = "CRM_EPIC_Events.admin.ManagerAdminSite"
