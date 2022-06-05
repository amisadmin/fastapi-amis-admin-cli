from core.settings import settings

{% if cookiecutter.use_user_auth=="True" %}
from fastapi_user_auth.site import AuthAdminSite

site = AuthAdminSite(settings)
auth = site.auth
{% else %}
from fastapi_amis_admin.amis_admin import AdminSite

site = AdminSite(settings)
{% endif %}

{% if cookiecutter.use_scheduler=="True" %}
from fastapi_scheduler import SchedulerAdmin

scheduler = SchedulerAdmin.bind(site)
{% endif %}
