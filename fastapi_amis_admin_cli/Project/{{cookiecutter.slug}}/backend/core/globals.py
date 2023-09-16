from sqlalchemy_database import AsyncDatabase, Database

from core.settings import settings

# 创建异步数据库引擎
async_db = AsyncDatabase.create(
    url=settings.database_url_async,
    session_options={
        "expire_on_commit": False,
    },
)
# 创建同步数据库引擎
sync_db = Database.create(
    url=settings.database_url,
    session_options={
        "expire_on_commit": False,
    },
)

{% if cookiecutter.use_user_auth=="True" %}
from fastapi_user_auth.site import AuthAdminSite

site = AuthAdminSite(settings, engine=async_db)
auth = site.auth
{% else %}
from fastapi_amis_admin.admin import AdminSite

site = AdminSite(settings, engine=async_db)
{% endif %}

{% if cookiecutter.use_scheduler=="True" %}
from fastapi_scheduler import SchedulerAdmin

scheduler = SchedulerAdmin.bind(site)
{% endif %}
