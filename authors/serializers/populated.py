from .common import AuthorSerializer
from courses.serializers.common import CourseSerializer
from courses.serializers.populated import PopulatedCourseSerializer

class PopulatedAuthorSerializer(AuthorSerializer):
    courses = PopulatedCourseSerializer(many=True, read_only=True)