from rest_framework import serializers
from ..models import Course

class CourseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk') 
    class Meta:
        model = Course
        fields = '__all__'

