from rest_framework import serializers
from role.models import Role, RolePermissionMap

class RoleSerializer(serializers.ModelSerializer):
    resource_ids = serializers.SerializerMethodField()
    class Meta:
        model = Role
        fields = ('id', 'resource_ids')

    def get_resource_ids(self, obj):
        return Role.objects.get_resources([obj.pk])