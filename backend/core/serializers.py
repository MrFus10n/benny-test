from django.contrib.auth.models import User
from rest_framework import serializers


class PeriodSerializer(serializers.Serializer):
    start = serializers.CharField(read_only=True)
    end = serializers.CharField(read_only=True)


class ConditionsSerializer(serializers.Serializer):
    periods = PeriodSerializer(many=True)
    amount_max = serializers.CharField(read_only=True)
    amount_min = serializers.CharField(read_only=True)


class ParserSerializer(serializers.Serializer):
    text = serializers.CharField(write_only=True)
    conditions = ConditionsSerializer(read_only=True)


class UserSerializer(serializers.ModelSerializer):
    is_authenticated = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_authenticated')

    @staticmethod
    def get_is_authenticated(obj):
        return obj.is_authenticated

    def to_representation(self, instance):
        if instance.is_anonymous:
            return {
                'id': None,
                'first_name': None,
                'last_name': None,
                'is_authenticated': False
            }
        return super().to_representation(instance)