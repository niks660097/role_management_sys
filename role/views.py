import json
from django.db.transaction import atomic
from rest_framework.views import APIView
from rest_framework.response import Response
from role.role_helper import RoleHelper
from role.models import Role
from role.serializers import RoleSerializer


class UserRolesEndpoint(APIView):

    role_helper = RoleHelper()

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        roles = self.role_helper.get_roles(user_id)
        return Response(data=RoleSerializer(roles, many=True).data)

    @atomic()
    def delete(self, request, *args, **kwargs):
        '''
        eg. request json = {"user_id":<int>, "role_id"<int>}
        '''
        raw_data = request.read().decode('utf-8')
        json_data = json.loads(raw_data)
        self.role_helper.remove_role(json_data['user_id'], json_data['role_id'])
        return Response(data={'result': 'deleted'})

    @atomic()
    def put(self, request, *args, **kwargs):
        '''
        eg. request json = {"user_id":<int>, "role_id"<int>}
        '''
        raw_data = request.read().decode('utf-8')
        json_data = json.loads(str(raw_data))
        self.role_helper.assign_role(json_data['user_id'], json_data['role_id'])
        return Response(data={'result':'added'})

    @atomic()
    def post(self, request, *args, **kwargs):
        '''
        eg. request json = {"role_name":<str>, "resource_list":[[id, permission],......]}
        '''
        raw_data = request.read().decode('utf-8')
        json_data = json.loads(raw_data)
        role = self.role_helper.create_role(role_name=json_data['role_name'], resource_list=json_data['resource_list'])
        return Response(data={'role_id': role.pk})

class UserAccessEndpoint(APIView):

    role_helper = RoleHelper()

    def get(self, request, *args, **kwargs):
        user_id, resource_id, permission = request.GET.get('user_id'), request.GET.get('resource_id'), request.GET.get('permission')
        return Response(data={'accessible': self.role_helper.check_access(user_id, resource_id, permission)})