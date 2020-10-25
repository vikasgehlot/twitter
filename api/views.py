from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import UserSerializer,TweetDetailSerializer,TweetSerializer,FollowerSerializer,FollowingSerializer
from .models import Follower,Tweet
from django.contrib.auth.models import User
from django.http import Http404
import datetime


@api_view(['GET'])
def tweets(request):
	all_tweets=Tweet.objects.none()
	timeline=datetime.datetime.now()-datetime.timedelta(days=1)
	following_tweets=Tweet.objects.filter(author__in=[query.username for query in request.user.follow.all()],created__gt=timeline)
	my_tweets=Tweet.objects.filter(author =request.user, created__gt=timeline)
	all_tweets=following_tweets.union(my_tweets)
	serilaizer=TweetSerializer(all_tweets.order_by('-created'),many=True)
	return Response(serilaizer.data)


@api_view(['GET'])
def tweet_detail(request,id):
	try:
		tweet=Tweet.objects.get(id=id)
		user=tweet.author
		if user ==request.user or request.user.follow.filter(username__username=user).exists():
			print(tweet.author)
			serializer=TweetDetailSerializer(tweet,context={'request': request})
			return Response(serializer.data)
		else:
			return Response(data={'detail':'permission denied'},status=status.HTTP_403_FORBIDDEN)
	except:
		raise Http404




@api_view(['GET'])
def following(request):
	try:
		user=request.query_params['user']
		if request.user.follow.filter(username__username=user).exists():
			following=request.user.follow.none()
			user=User.objects.filter(username=user).get()
			serializer=FollowingSerializer(following,context={'user': user})
			return Response(serializer.data)
		else:
			forbidden={'message':'permission denied or user not exist'}
			return Response(data=forbidden,status=status.HTTP_403_FORBIDDEN)
	except:
		following=request.user.follow.none()
		serializer=FollowingSerializer(following,context={'user': request.user})
		return Response(serializer.data)


@api_view(['GET'])
def follower(request):
	try:
		user=request.query_params['user']
		if request.user.follow.filter(username__username=user).exists():
			follower=Follower.objects.filter(username__username=user)
			serializer=FollowerSerializer(follower,many=True)
			return Response(serializer.data)
		else:
			forbidden={'message':'permission denied or user not exits'}
			return Response(data=forbidden,status=status.HTTP_403_FORBIDDEN)
	except:
		follower=Follower.objects.filter(username__username=request.user)
		serializer=FollowerSerializer(follower,many=True)
		return Response(serializer.data)





@api_view(['GET'])
def like(request,id):
	try:
		print(id)
		tweet=Tweet.objects.get(id=id)
		tweet.likes.add(request.user)
		return Response(status=status.HTTP_202_ACCEPTED)
	except:
		raise Http404



@api_view(['GET'])
def unlike(request,id):
	try:
		tweet=Tweet.objects.get(id=id)
		tweet.likes.remove(request.user)
		return Response(status=status.HTTP_202_ACCEPTED)
	except:
		raise Http404





@api_view(['GET'])
def follow(request,user):
	try:
		follow=Follower.objects.filter(username__username=user).get()
		follow.followers.add(request.user)
		return Response(status=status.HTTP_202_ACCEPTED)
	except:
		raise Http404



@api_view(['GET'])
def unfollow(request,user):
	try:
		follow=Follower.objects.filter(username__username=user).get()
		follow.followers.remove(request.user)
		return Response(status=status.HTTP_202_ACCEPTED)
	except:
		raise Http404



@api_view(['GET'])
def retweet(request,id):
	try:
		tweet=Tweet.objects.get(id=id)
		tweet.retweets.add(request.user)
		return Response(status=status.HTTP_202_ACCEPTED)
	except:
		raise Http404



@api_view(['GET'])
def unretweet(request,id):
	try:
		tweet=Tweet.objects.get(id=id)
		tweet.retweets.remove(request.user)
		return Response(status=status.HTTP_202_ACCEPTED)
	except:
		raise Http404


@api_view(['GET'])
def user(request):
	user=User.objects.all()
	serilaizer=UserSerializer(user,many=True)
	return Response(serilaizer.data)


