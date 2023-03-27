from .models import LogFile, Operation, TraceBack
from rest_framework import serializers

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = [
            'id',
            'level',
            'message',
            'created_at',
            'source_name'
        ]

class TraceBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraceBack
        fields = [
            'id',
            'level',
            'message',
            'created_at',
            'is_corrected',
            'corrected_at',
            'source_name'
        ]


class LogFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogFile
        fields = [
            'file',
            'type',
            'source_name',
            'created_at'
        ]