from rest_framework import serializers

from users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    get_like_count = serializers.SerializerMethodField()  # 自定义字段: 选择题选
    def get_get_like_count(self,obj):
        return obj.get_like_count(obj)
    class Meta:
        model = User
        fields =["id", "username", "get_like_count"]

