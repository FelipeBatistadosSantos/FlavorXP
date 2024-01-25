from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, User
from django.db import models
from cpf_field.models import CPFField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('O endereço de e-mail deve ser fornecido')
        
        if not password:
            raise ValueError('A senha deve ser fornecida')

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    password = models.TextField(verbose_name='password')

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def has_module_perms(self, app_label):
        return True
    
    def has_perm(self, perm, obj=None):
        return True