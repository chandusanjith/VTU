from rest_framework import serializers
from .models import MasterNotes


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterNotes
        fields = '__all__'
        depth = 1