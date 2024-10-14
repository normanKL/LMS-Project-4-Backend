from django.urls import path
from .views import CourseListView, CourseDetailView, AddCourseToProfileView, UserCoursesView, RemoveCourseFromProfileView

urlpatterns = [
    path('', CourseListView.as_view()),
    path('<int:pk>/', CourseDetailView.as_view()),
    path('<int:course_id>/add/', AddCourseToProfileView.as_view()),
    path('user/<str:user_id>/', UserCoursesView.as_view()),
    path('<int:course_id>/remove/', RemoveCourseFromProfileView.as_view()),
]