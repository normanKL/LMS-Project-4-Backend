from django.urls import path
from .views import AuthorListView, AuthorDetailView, AuthorCoursesView

urlpatterns = [
    path('', AuthorListView.as_view()),
    path('<int:pk>/', AuthorDetailView.as_view()),
    path('<int:author_id>/courses/', AuthorCoursesView.as_view())
]