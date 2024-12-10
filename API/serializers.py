from rest_framework import serializers
from bookfault.models import bookfaultmodel

class FaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = bookfaultmodel
        fields = '__all__'
