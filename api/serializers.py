from rest_framework import serializers
from .models import test_case, test_part, variable

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = test_case
        fields = ["id", "test_part", "output"]

class TestPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = test_part
        fields = ["id", "name", "description"]