from rest_framework import serializers 
from social.models import Post,Comment,Like
from accounts.serializers import UserProfileSerializer
from rest_framework.exceptions import ValidationError

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post   
        fields=('post_id','title','description')

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