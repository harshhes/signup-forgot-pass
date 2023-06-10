from django.urls import path, include
from .views import RegisterUserView, LoginView, ForgotPasswordView, ResetPasswordView, UserView

urlpatterns =[
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('reset-password/', ForgotPasswordView.as_view(), name='reset-password'),
    path('reset-password/<str:encoded_pk>/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),
    path('user-detail', UserView.as_view(), name='user-detail')
]
