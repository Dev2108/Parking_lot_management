from rest_framework import serializers
from user_dash.models import Vehicle

class EntrySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(min_value=1, required = True)
    class Meta:
        model = Vehicle
        fields = ('number', 'user_id')
        extra_kwargs = {'number': {'required': True}}
