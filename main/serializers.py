from rest_framework import serializers
from .models import Lab, Todo

class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ['id', 'title', 'description', 'due_date', 'completed']


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['title', 'completed']