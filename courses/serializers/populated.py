from authors.serializers.common import AuthorSerializer
from comments.serializers.populated import PopulatedCommentSerializer
from jwt_auth.serializers import UserSerializer
from .common import CourseSerializer

class PopulatedCourseSerializer(CourseSerializer):
    author = AuthorSerializer()
    comments = PopulatedCommentSerializer(many=True)
    owner = UserSerializer()