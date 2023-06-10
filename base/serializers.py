from re import search
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import User
from rest_framework import serializers
from utility.constants import UserRoles
from django.contrib.auth.models import Group
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset = User.objects.all())])

    password = serializers.CharField(write_only =True,required=True, validators=[validate_password], style ={'input_type': 'password'})

    confirm_password = serializers.CharField(write_only=True, required=True, style ={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'username','role', 'password', 'confirm_password')
        extra_kwargs = {
            'name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password':{"Password fields didn't match"}})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email = validated_data['email'],
            name = validated_data['name'],
            username = validated_data['username'],
            role = validated_data['role']
            )
        print(user)
        user.set_password(validated_data['password'])
        if user.role == UserRoles.teacher.value:
            teacher_group = Group.objects.get(name='Teacher')
            user.groups.add(teacher_group)

        elif user.role == UserRoles.student.value:
            student_group = Group.objects.get(name='Student')
            user.groups.add(student_group)

        elif user.role == UserRoles.super_admin.value:
            admin_group = Group.objects.get(name='Admin')
            user.groups.add(admin_group)

        user.save()

        return user

  
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields= ['email', 'password']


    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)    

    
class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=100, write_only=True)
    confirm_new_password = serializers.CharField(max_length=100, write_only=True)

    def validate(self, attrs):
        password = attrs['new_password']
        token = self.context.get('kwargs').get('token')
        encoded_pk = self.context.get('kwargs').get('encoded_pk')

        if password != attrs['confirm_new_password']:
            raise serializers.ValidationError({'password':{"Password fields didn't match"}})

        elif (token and encoded_pk) is None:
            raise serializers.ValidationError("Please provide Required Data!!")
        
        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)

        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError("Reset token is not valid!!!")

        user.set_password(password)
        user.password_changed = True
        user.save()

        return attrs


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        exclude = ['id', 'password', 'last_login']
        