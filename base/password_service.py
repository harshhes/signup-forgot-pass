from django.utils.encoding import force_bytes
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class PasswordService:
    
    def generate_token(self,user):
        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        reset_url = reverse('reset-password',kwargs={'encoded_pk':encoded_pk, 'token': token})
        return reset_url