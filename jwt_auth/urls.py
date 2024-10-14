from django.urls import path
from .views import RegisterView, LoginView, UserInfoView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserInfoView.as_view()),
    path('profile/', UserProfileView.as_view()),
]