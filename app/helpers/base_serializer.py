from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    iid = serializers.CharField(read_only=True)
