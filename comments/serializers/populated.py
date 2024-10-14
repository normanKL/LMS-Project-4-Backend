from .common import CommentSerializer
from jwt_auth.serializers import UserSerializer

class PopulatedCommentSerializer(CommentSerializer):
    owner = UserSerializer()