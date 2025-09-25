from djoser.serializers import UserSerializer as BaseUserSerializer,UserCreateSerializer as BaseUserCreateSerialilzer

class UserCreateSerializer(BaseUserCreateSerialilzer):
    class Meta(BaseUserCreateSerialilzer.Meta):
        fields=['id','email','password','first_name','last_name','address','phone_number']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name='CustomUser'
        fields=['id','email','password','first_name','last_name','address','phone_number']