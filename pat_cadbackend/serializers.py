# serializers.py

from rest_framework import serializers
from .models import CurrentCall

class CurrentCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentCall
        fields = '__all__'
