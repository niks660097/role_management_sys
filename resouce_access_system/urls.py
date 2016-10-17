"""resouce_access_system URL Configuration
"""
from django.conf.urls import url
from django.contrib import admin
from role.views import UserRolesEndpoint, UserAccessEndpoint

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^role/', UserRolesEndpoint.as_view()),
    url(r'^user/access/', UserAccessEndpoint.as_view()),
]