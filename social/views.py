from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
from backend.settings import SECRET_KEY
from social.models import Post,Like
from social.models import UserProfile,UserProfile,Following
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from social.serializers import (
PostSerializer,
CommentSerializer,
LikeSerializer,
UserProfileSerializer,
AuthenticateSerializer,
FollowingSerializer,
AllPostSerializer
)

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
            return Response({"message":"User Unfollowed"},status=status.HTTP_201_CREATED)
             
        except:
            return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)

class PostCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        token=request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        user_email=jwt.decode(token,SECRET_KEY, algorithms=['HS256'])['user_id']
        user=UserProfile.objects.get(email=user_email)
        serializer=PostSerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class PostDetailDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,post_id):
        post=get_object_or_404(Post,post_id=post_id)
        serializer=PostSerializer(post)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self,request,post_id):
        token_meta=request.META.get('HTTP_AUTHORIZATION')
        token=token_meta.split(" ")[1]
        user_email=jwt.decode(token,SECRET_KEY, algorithms=['HS256'])['user_id']
        current_user=get_object_or_404(UserProfile,email=user_email)

        post=get_object_or_404(Post,post_id=post_id)
        print(current_user.user_id,post.user.user_id)
        if not current_user.user_id==post.user.user_id:
            return Response({"message":" You are not authorized to perform this action, Deletion of post is only authorized to creator of post."},status=status.HTTP_401_UNAUTHORIZED)
        
        post.delete()
        return Response({"message":" Post Deleted"},status=status.HTTP_200_OK)

class AllPostView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        token=request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        user_email=jwt.decode(token,SECRET_KEY, algorithms=['HS256'])['user_id']
        user=UserProfile.objects.get(email=user_email)
        user_id=user.user_id
        posts=Post.objects.filter(user=user_id)
        serializer=AllPostSerializer(posts,context={'user': user},many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    


class CommentCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request,post_id):
        token=request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        user_email=jwt.decode(token,SECRET_KEY, algorithms=['HS256'])['user_id']
        user=UserProfile.objects.get(email=user_email)
        post=get_object_or_404(Post,post_id=post_id)
        serializer=CommentSerializer(data=request.data, context={'user': user,'post':post})
        if serializer.is_valid():
            serializer.save()
            post.comment_count+=1
            post.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class LikeView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self,request,post_id):
        token=request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        user_email=jwt.decode(token,SECRET_KEY, algorithms=['HS256'])['user_id']
        user=UserProfile.objects.get(email=user_email)
        post=get_object_or_404(Post,post_id=post_id)
        
        relation=Like.objects.filter(user=user,post=post)
        if relation.exists():
            return Response({"message":"Already Liked this Post"},status=status.HTTP_400_BAD_REQUEST)

        serializer=LikeSerializer(data=request.data, context={'user': user,'post':post})
        if serializer.is_valid():
            serializer.save()
            post.like_count+=1
            post.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class UnLikeView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self,request,post_id):
        token=request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        user_email=jwt.decode(token,SECRET_KEY, algorithms=['HS256'])['user_id']
        user=UserProfile.objects.get(email=user_email)
        post=get_object_or_404(Post,post_id=post_id)
        
        relation=Like.objects.filter(user=user,post=post)
        if not relation.exists():
            return Response({"message":"Not Liked this Post. User is allowed to unlike post that they have liked."},status=status.HTTP_400_BAD_REQUEST)

        relation.delete()
        post.like_count-=1
        post.save()
        return Response({"message":"Post Unliked"},status=status.HTTP_201_CREATED)
        