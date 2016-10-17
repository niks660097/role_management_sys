from django.db.transaction import atomic
from resource.models import Resource
from role.models import Role, RolePermissionMap, UserRole

class RoleHelper:

    @atomic()
    def assign_role(self, user_id, role_id):
        user_role = UserRole.objects.filter(user_id=user_id, role_id=role_id).first()
        if not user_role:
            user_role = UserRole.objects.create(user_id=user_id, role_id=role_id)
        return user_role

    @atomic()
    def remove_role(self, user_id, role_id):
        user_role = UserRole.objects.filter(user_id=user_id, role_id=role_id)
        if user_role.first():
            user_role.delete()

    def check_access(self, user_id, resource_id, permission):
        roles = self.get_roles(user_id)
        role_permission_map = RolePermissionMap.objects.filter(role__in=roles, resource_id=resource_id,
                                                               permission=permission)
        if role_permission_map.first():
            return True
        else:
            return False

    def get_roles(self, user_id):
        role_ids = UserRole.objects.filter(user_id=user_id).values_list('role_id', flat=True)
        return Role.objects.filter(id__in=role_ids)

    @atomic()
    def create_role(self, role_name, resource_list):
        role = Role.objects.create(name=role_name)
        for i in resource_list:#(id, permission_code)
            res = Resource.objects.get(pk=i[0])
            r_r = RolePermissionMap.objects.create(resource_id=i[0], permission=i[1], role=role)
        return role

