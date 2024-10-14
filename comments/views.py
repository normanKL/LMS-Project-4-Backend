from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from .models import Comment
from .serializers.common import CommentSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class CommentListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, _request):
        comments = Comment.objects.all()
        serialized_comments = CommentSerializer(comments, many=True)
        return Response(serialized_comments.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        request.data["owner"] = request.user.id
        comment_to_add = CommentSerializer(data=request.data)
        try:
            comment_to_add.is_valid()
            comment_to_add.save()
            return Response(comment_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error")
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class CommentDetailView(APIView):
    permission_classes = (IsAuthenticated, )
    def get_comment(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound(detail="Comment not found")

    def get(self, _request, pk):
        try:
            comment = self.get_comment(pk=pk)
            serialized_comment = CommentSerializer(comment)
            return Response(serialized_comment.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            raise NotFound(detail="Comment not found")
        
    def put(self, request, pk):
        comment_to_update = self.get_comment(pk=pk)
        updated_comment = CommentSerializer(comment_to_update, data=request.data, partial=True)
        if updated_comment.is_valid():
            updated_comment.save()
            return Response(updated_comment.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(updated_comment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def delete(self, request, pk):
        comment_to_delete = self.get_comment(pk=pk)
        if comment_to_delete.owner != request.user:
         return Response({"detail": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

        comment_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
