from rest_framework import serializers

class MonthDataSerializer(serializers.Serializer):
    y = serializers.IntegerField()
    m = serializers.IntegerField()