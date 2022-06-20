from django.contrib.auth.models import User
from core.models import Paste, ExpiryLog, Language
from rest_framework import serializers
from core.validators import validate_future_datetime


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_staff']
        read_only_fields = ['id', 'username', 'is_staff']


class PasteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Paste
        fields = [
            'id',
            'title',
            'body',
            'timestamp',
            'expiry',
            'freeze_hits',
            'hits',
            'size',
            'author',
            'language',
        ]
        read_only_fields = ['id', 'freeze_hits', 'hits']

    def validate_expiry(self, value):
        if value is not None:  # JSON null means no expiry.
            validate_future_datetime(value)
        return value


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name']
        read_only_fields = ['id']


class ExpiryLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExpiryLog
        fields = [
            'id',
            'expired_ids',
            'timestamp',
            'count',
            'reclaimed_space',
            'completed',
        ]
        read_only_fields = ['id']
