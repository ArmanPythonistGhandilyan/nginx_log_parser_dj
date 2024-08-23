from logs.models import NginxLog
from rest_framework import serializers


class NginxLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NginxLog
        fields = "__all__"
