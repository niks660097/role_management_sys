from django.db import models


class RoleManager(models.Manager):
    def get_resources(self, role_list):
        resources = RolePermissionMap.objects.filter(role__in=role_list)
        return [(i.role.pk, i.get_permission_display()) for i in resources]

class Role(models.Model):
    name = models.CharField(max_length=15, null=False, blank=False)

    objects = RoleManager()

    @property
    def resources(self):#returns queryset
        return self.rolepermissionmap_set.all()

    def __str__(self):
        return self.name

class RolePermissionMap(models.Model):
    PERMISSIONS = ((1, 'READ',),
                   (2, 'WRITE',),
                   (3, 'DELETE'))

    permission = models.PositiveIntegerField(choices=PERMISSIONS, default=1)
    role = models.ForeignKey('role.Role')
    resource = models.ForeignKey('resource.Resource')#assuming all resources have a unique id, and in database

    def __str__(self):
        return '%s:%s' %(self.role.name,self.get_permission_display())

class UserRole(models.Model):
    user = models.ForeignKey('auth.User')
    role = models.ForeignKey('role.Role')

    def __str__(self):
        return '%s,%s' % (self.user.username, str(self.role))

