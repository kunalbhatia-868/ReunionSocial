from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class UserProfileManager(BaseUserManager):
    def create_user(self,email,password,**fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        
        email=self.normalize_email(email)
        user=self.model(email=email,**fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,**fields):
        fields.setdefault('is_staff',True)
        fields.setdefault('is_superuser',True)
        fields.setdefault('is_active',True)
        
        if fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        
        if fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email,password,**fields)