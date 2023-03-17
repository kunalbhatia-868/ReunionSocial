from rest_framework import serializers 
from social.models import Post,Comment,Like
from rest_framework.exceptions import ValidationError

from rest_framework import serializers
from social.models import UserProfile,Following
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

    def to_representation(self, instance):
        rep= super().to_representation(instance)
        rep['sender']=UserProfileSerializer(instance.sender).data
        rep['reciever']=UserProfileSerializer(instance.reciever).data
        return rep 

class AuthenticateSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print("validating")  
        data={
            'token':super().validate(attrs),
        }
        return data
    

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post   
        fields=('post_id','title','description','like_count','comment_count')

    def create(self, validated_data):
        try:
            post = Post.objects.create(
                title=validated_data.get('title', ''),
                description=validated_data.get('description', ''),
                user=self.context['user']
            )
            return post
        
        except ValidationError as e:
            raise serializers.ValidationError(e)

    def validate(self, data):
        title = data.get('title', '')
        description = data.get('description', '')

        if not title or not description:
            raise serializers.ValidationError("Title and Description are required fields in Post.")

        if len(title) > 100:
            raise serializers.ValidationError("Title cannot be longer than 100 characters.")

        if len(description) < 5:
            raise serializers.ValidationError("Description must be at least 5 characters long.")

        return data
    
    def to_representation(self, instance):
        rep= super().to_representation(instance)
        rep['user']=UserProfileSerializer(instance.user).data
        return rep
    
class AllPostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model=Post
        fields=('post_id','title','description','created_on','like_count','comments')
    
    def get_comments(self, obj):
        user=self.context['user']
        comments = Comment.objects.filter(user=user)
        return [comment.text for comment in comments]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['text']

    def to_representation(self, instance):
        rep= super().to_representation(instance)
        rep['user']=UserProfileSerializer(instance.user).data
        rep['post']=PostSerializer(instance.post).data
        return rep
    
    def create(self, validated_data):
        try:
            comment = Comment.objects.create(
                text=validated_data.get('text', ''),
                user=self.context['user'],
                post=self.context['post'],
            )
            return comment
        
        except ValidationError as e:
            raise serializers.ValidationError(e) 

    def validate(self, data):
        text = data.get('text', '')
        if not text:
            raise serializers.ValidationError("Text are required fields in Comment.")
        return data   
    
  
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields=[]

    def to_representation(self, instance):
        rep= super().to_representation(instance)
        rep['user']=UserProfileSerializer(instance.user).data
        rep['post']=PostSerializer(instance.post).data
        return rep
    
    def create(self, validated_data):
        try:
            like = Like.objects.create(
                user=self.context['user'],
                post=self.context['post'],
            )
            return like
        
        except ValidationError as e:
            raise serializers.ValidationError(e) 