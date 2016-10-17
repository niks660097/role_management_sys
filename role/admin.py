from django.contrib import admin

from role.models import *

admin.site.register(Role)
admin.site.register(RolePermissionMap)
admin.site.register(UserRole)

