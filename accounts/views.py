import jwt
from backend.settings import SECRET_KEY
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import UserProfile,Following
from accounts.serializers import UserProfileSerializer,AuthenticateSerializer,FollowingSerializer
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class AuthenticateView(TokenObtainPairView):
    serializer_class = AuthenticateSerializer

class UserDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        token_meta=request.META.get('HTTP_AUTHORIZATION')
        try:
            token=token_meta.split(" ")[1]
            user_email=jwt.decode(token,SECRET_KEY, algorithms=['HS256'])['user_id']
            user=get_object_or_404(UserProfile,email=user_email)
            serializer=UserProfileSerializer(user)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
        

class Follow(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,user_id):
        token_meta=request.META.get('HTTP_AUTHORIZATION')
        try:
            token=token_meta.split(" ")[1]
            user_email=jwt.decode(token,SECRET_KEY, algorithms=['HS256'])['user_id']
            current_user=get_object_or_404(UserProfile,email=user_email)
            follow_user=get_object_or_404(UserProfile,user_id=user_id)

            relation=Following.objects.filter(sender=current_user.user_id,reciever=user_id)
            if relation.exists():
                return Response({"message":"Already Following"},status=status.HTTP_400_BAD_REQUEST)

            serializer=FollowingSerializer(data={'sender':current_user.user_id,'reciever':user_id})
            if serializer.is_valid():
                serializer.save()
                current_user.following_count += 1
                current_user.save()
                follow_user.follower_count += 1
                follow_user.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
        except:
            return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
        
class UnFollow(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,user_id):
        token_meta=request.META.get('HTTP_AUTHORIZATION')
        try:
            token=token_meta.split(" ")[1]
            user_email=jwt.decode(token,SECRET_KEY, algorithms=['HS256'])['user_id']
            current_user=get_object_or_404(UserProfile,email=user_email)
            unfollow_user=get_object_or_404(UserProfile,user_id=user_id)

            relation=Following.objects.filter(sender=current_user.user_id,reciever=user_id)
            if not relation.exists():
                return Response({"message":"Already Not Following this User"},status=status.HTTP_400_BAD_REQUEST)
            
            
            relation.delete()
            current_user.following_count -= 1
            current_user.save()
            unfollow_user.follower_count -= 1
            unfollow_user.save()
            return Response(status=status.HTTP_201_CREATED)
             
        except:
            return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)