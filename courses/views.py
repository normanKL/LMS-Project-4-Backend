from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model

from .models import Course
from .serializers.common import CourseSerializer
from .serializers.populated import PopulatedCourseSerializer
from jwt_auth.models import Profile  

User = get_user_model()

# Create your views here.

class CourseListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        course = Course.objects.all()
        serialized_course = PopulatedCourseSerializer(course, many=True)
        return Response(serialized_course.data, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        queryset = Course.objects.all()
        title = self.request.query_params.get('title', None)
        author = self.request.query_params.get('author', None)

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__name__icontains=author)

        return queryset
    
    def post(self, request):
        request.data["owner"] = request.user.id
        course_to_add = CourseSerializer(data=request.data)
        try:
            course_to_add.is_valid()
            course_to_add.save()
            return Response(course_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error")
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class CourseDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    def get_course(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise NotFound(detail="Course not found")

    def get(self, _request, pk):
        try:
            course = self.get_course(pk=pk)
            serialized_course = PopulatedCourseSerializer(course)
            return Response(serialized_course.data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            raise NotFound(detail="Course not found")
        
    def put(self, request, pk):
        course_to_update = self.get_course(pk=pk)
        updated_course = CourseSerializer(course_to_update, data=request.data, partial=True)
        if updated_course.is_valid():
            updated_course.save()
            return Response(updated_course.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(updated_course.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def delete(self, _request, pk):
        course_to_delete = self.get_book(pk=pk)
        course_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AddCourseToProfileView(APIView):
    def post(self, request, course_id):
        user = request.user
        if not hasattr(user, 'profile'):
            return Response({"detail": "User profile does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            course = Course.objects.get(id=course_id)
            user.profile.courses.add(course)  # Assuming 'courses' is a ManyToManyField in the Profile model
            return Response({"detail": "Course added successfully."}, status=status.HTTP_201_CREATED)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

class UserCoursesView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request, user_id):
        try:
            profile = Profile.objects.get(user__id=user_id)  # Adjust this if necessary
            courses = profile.courses.all()
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RemoveCourseFromProfileView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def delete(self, request, course_id):
        profile = request.user.profile  # Assuming user has a profile
        try:
            course = Course.objects.get(id=course_id)
            profile.courses.remove(course)
            return Response({"message": "Course removed from profile"}, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
