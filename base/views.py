from rest_framework import generics, viewsets, permissions
from .password_service import PasswordService
from .serializers import RegisterUserSerializer, LoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer, UserSerializer
from .models import User
from django.contrib.auth import login
from utility.response_handler import HTTPResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django_task.settings import EMAIL_HOST_USER


# generate JWT token after login
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# authenticate user via email
def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    if user.check_password(password):
        return user


class RegisterUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request, format=None):

        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email') 
            password = serializer.data.get('password') 

            user = authenticate_user(email=email, password=password)
            
            if user is not None:
                token = get_tokens_for_user(user)
                login(request,user)
                data = {'msg':"Login Success!", 'token':token}
                return HTTPResponse(status_code=200).generic_response(data=data)
            else:
                return HTTPResponse(status_code=404).generic_response(data="email or password is not valid!!")

        return HTTPResponse(status_code=400).generic_response(data=serializer.errors)


class ForgotPasswordView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        current_user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.data.get('email')
        user = User.objects.get(email=user_email)
        if user and (current_user.email == user_email):
            reset_token = PasswordService().generate_token(user)
            send_mail('Reset Password Email',
            f'''
Hi {current_user.name.split(" ")[0].capitalize()},
There was a request to reset your password!

If you did not make this request then please ignore this email.

Otherwise, Please refer to this link to change your password: http://localhost:8000{reset_token}''',
            EMAIL_HOST_USER,
            [user_email],
            fail_silently=False)

            return HTTPResponse().generic_response(data=f"A email with instructions of how to reset-password has been sent to {current_user.email}")

        else:
            return HTTPResponse().generic_response(data="You can't change someone else's account's password!!")
        

class ResetPasswordView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer

    def patch(self,request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'kwargs':kwargs})

        serializer.is_valid(raise_exception=True)
        return HTTPResponse(200).success_response("Password reset successfully!")


class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

