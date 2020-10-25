from rest_framework import serializers
from .models import Follower,Tweet
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=User
		fields=['id','username']


class TweetSerializer(serializers.ModelSerializer):
	likes=serializers.SerializerMethodField(read_only=True)
	retweets=serializers.SerializerMethodField(read_only=True)
	author= serializers.StringRelatedField(many=False)
	class Meta:
		model=Tweet
		fields=['id','tweet','author','likes','retweets']

	def get_likes(self,obj):
		return obj.likes.count()

	def get_retweets(self,obj):
		return obj.retweets.count()



class TweetDetailSerializer(serializers.ModelSerializer):
	like=serializers.SerializerMethodField(read_only=True)
	retweet=serializers.SerializerMethodField(read_only=True)
	likes=serializers.SerializerMethodField(read_only=True)
	retweets=serializers.SerializerMethodField(read_only=True)
	author= serializers.StringRelatedField(many=False)
	class Meta:
		model=Tweet
		fields=['id','tweet','author','likes','retweets','like','retweet']

	def get_likes(self,obj):
		return obj.likes.count()

	def get_like(self,obj):
		request = self.context.get("request")
		following=[i.username.username for i in request.user.follow.all()]
		following+=[request.user.username]
		query=[i.username for i in obj.likes.all()]
		return list(set(query) & set(following)) 

	def get_retweets(self,obj):
		return obj.retweets.count()

	def get_retweet(self,obj):
		request = self.context.get("request")
		following=[i.username.username for i in request.user.follow.all()]
		following+=[request.user.username]
		query=[i.username for i in obj.retweets.all()]
		return list(set(query) & set(following)) 



class FollowerSerializer(serializers.ModelSerializer):
	username=serializers.StringRelatedField(many=False)
	followers=serializers.StringRelatedField(many=True)

	class Meta:
		model=Follower
		fields=['username','followers']




class FollowingSerializer(serializers.Serializer):
	username=serializers.SerializerMethodField(read_only=True)
	following=serializers.SerializerMethodField(read_only=True)
	
	class Meta:
		model=Follower
		fields=['username','following']
	def get_username(self,obj):
		user = self.context.get("user")
		print(user)
		
		return user.username

	def get_following(self,obj):
		user = self.context.get("user")
		print(user.follow.all())
		following=[i.username.username for i in user.follow.all()]
		return following





	



