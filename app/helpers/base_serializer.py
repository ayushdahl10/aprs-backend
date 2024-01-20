from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    iid = serializers.CharField(read_only=True)


class BaseSerializer(serializers.Serializer):
    iid = serializers.CharField(read_only=True)
