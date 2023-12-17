from common.serializers.mixins import ExtendedModelSerializer
from organizations.models.organizations import Employee
from organizations.serializars.nested.dicts import PositionShortSerializer
from users.serializars.nested.users import UserShortSerializer


class EmployeeShortSerializer(ExtendedModelSerializer):
    user = UserShortSerializer()
    position = PositionShortSerializer()

    class Meta:
        fields = (
            'id',
            'user',
            'position',
        )
        model = Employee
