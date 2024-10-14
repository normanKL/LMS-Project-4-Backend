from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from .models import Author
from .serializers.common import AuthorSerializer
from .serializers.populated import PopulatedAuthorSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from courses.models import Course
from courses.serializers.common import CourseSerializer
from courses.serializers.populated import PopulatedCourseSerializer

# Create your views here.

class AuthorListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    def get(self, _request):
        authors = Author.objects.all()
        serialized_authors = PopulatedAuthorSerializer(authors, many=True)
        return Response(serialized_authors.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        author_to_add = AuthorSerializer(data=request.data)
        try:
            author_to_add.is_valid()
            author_to_add.save()
            return Response(author_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error")
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class AuthorDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    def get_author(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise NotFound(detail="Author not found")

    def get(self, _request, pk):
        try:
            author = self.get_author(pk=pk)
            serialized_author = PopulatedAuthorSerializer(author)
            return Response(serialized_author.data, status=status.HTTP_200_OK)
        except Author.DoesNotExist:
            raise NotFound(detail="Author not found")
        
    def put(self, request, pk):
        author_to_update = self.get_author(pk=pk)
        updated_author = AuthorSerializer(author_to_update, data=request.data, partial=True)
        if updated_author.is_valid():
            updated_author.save()
            return Response(updated_author.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(updated_author.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def delete(self, _request, pk):
        author_to_delete = self.get_author(pk=pk)
        author_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AuthorCoursesView(APIView):
    def get(self, request, author_id):
        courses = Course.objects.filter(author__id=author_id).select_related('author', 'owner')
        serialized_courses = PopulatedCourseSerializer(courses, many=True)
        return Response(serialized_courses.data, status=status.HTTP_200_OK)
