from rest_framework import serializers
from accounts.models import UserProfile,Following
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields=["user_id","username","email","first_name","last_name","bio","follower_count","following_count","created_on","updated_on"]
        extra_kwargs = {'password': {'write_only': True}}

    def save(self,**kwargs):
        username=self.validated_data['username']   
        password=self.validated_data['password']
        email=self.validated_data['email']
        first_name=self.validated_data['first_name']    
        last_name=self.validated_data['last_name']    
        bio=self.validated_data['bio']     
        
        if(UserProfile.objects.filter(username=username)).exists():
            return serializers.ValidationError("Username already have an Account")

        if(UserProfile.objects.filter(email=email)).exists():
            return serializers.ValidationError("Email already have an Account")

        account=UserProfile(email=email,username=username,first_name=first_name,last_name=last_name,bio=bio)
        account.set_password(password)
        account.save()
        return account

class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Following
        fields="__all__"  

class AuthenticateSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print("validating")  
        data={
            'token':super().validate(attrs),
        }
        return data