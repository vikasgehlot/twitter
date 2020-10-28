from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from .serializer import UserSerializer,TweetDetailSerializer,TweetSerializer,FollowerSerializer,FollowingSerializer
from .models import Follower,Tweet
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
import datetime
from  django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login


@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def tweets(request):
	print(request.method)
	serializer=TweetSerializer()
	if request.method=='GET':
		all_tweets=Tweet.objects.none()
		timeline=datetime.datetime.now()-datetime.timedelta(days=20)
		following_tweets=Tweet.objects.filter(author__in=[query.username for query in request.user.follow.all()],created__gt=timeline)
		my_tweets=Tweet.objects.filter(author =request.user, created__gt=timeline)
		all_tweets=following_tweets.union(my_tweets)
		serilaizer=TweetSerializer(all_tweets.order_by('-created'),many=True)
		return Response(serilaizer.data)
	else:
		print(request.data)
		# return Response(status=status.HTTP_202_ACCEPTED)
		serializer =TweetSerializer(data=request.data,context={'request': request})
		if serializer.is_valid():
			print("valid")
			serializer.save()
			print(serializer)
			return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
		else:
			print(serializer)
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def tweet_detail(request,id):
	# serializer=TweetDetailSerializer()
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
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def like(request,id):
	try:
		tweet=Tweet.objects.get(id=id)
		user=tweet.author
		if user ==request.user or request.user.follow.filter(username__username=user).exists():
			tweet.likes.add(request.user)
			return Response(status=status.HTTP_202_ACCEPTED)
		else:
			return Response(data={'detail':'permission denied'},status=status.HTTP_403_FORBIDDEN)

	except:
		raise Http404



@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def unlike(request,id):

	try:
		tweet=Tweet.objects.get(id=id)
		user=tweet.author
		if user ==request.user or request.user.follow.filter(username__username=user).exists():
			tweet.likes.remove(request.user)
			return Response(status=status.HTTP_202_ACCEPTED)
		else:
			return Response(data={'detail':'permission denied'},status=status.HTTP_403_FORBIDDEN)

	except:
		raise Http404





@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def follow(request,user):
	try:
		follow=Follower.objects.filter(username__username=user).get()
		follow.followers.add(request.user)
		return Response(status=status.HTTP_202_ACCEPTED)
	except:
		raise Http404



@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def unfollow(request,user):
	try:
		follow=Follower.objects.filter(username__username=user).get()
		follow.followers.remove(request.user)
		return Response(status=status.HTTP_202_ACCEPTED)
	except:
		raise Http404



@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def retweet(request,id):
	try:
		tweet=Tweet.objects.get(id=id)
		user=tweet.author
		if user ==request.user or request.user.follow.filter(username__username=user).exists():
			tweet.retweets.add(request.user)
			return Response(status=status.HTTP_202_ACCEPTED)
		else:
			return Response(data={'detail':'permission denied'},status=status.HTTP_403_FORBIDDEN)
	
	except:
		raise Http404




@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def unretweet(request,id):
	try:
		tweet=Tweet.objects.get(id=id)
		user=tweet.author
		if user ==request.user or request.user.follow.filter(username__username=user).exists():
			tweet.retweets.remove(request.user)
			return Response(status=status.HTTP_202_ACCEPTED)
		else:
			return Response(data={'detail':'permission denied'},status=status.HTTP_403_FORBIDDEN)

	except:
		raise Http404
	


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete(request,id):
	try:
		tweet=Tweet.objects.get(id=id)
		user=tweet.author
		if user ==request.user:
			# print("Found")
			tweet.delete()
			return Response(status=status.HTTP_200_OK)
		else:
			return Response(data={'detail':'permission denied'},status=status.HTTP_403_FORBIDDEN)
	except ObjectDoesNotExist:
		# print("Alreday deleted in this request")
		raise Http404


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request):
	request.user.delete()
	return Response(status=status.HTTP_200_OK)



@api_view(['GET','POST'])
def user(request):
	if request.method=='POST':
		serilaizer=UserSerializer(data=request.data)
		print(serilaizer)
		if serilaizer.is_valid():
			print(serilaizer)
			serilaizer.save()
			return Response(serilaizer.data,status=status.HTTP_201_CREATED)
		else:
			return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)
	else:

		user=User.objects.all()
		serilaizer=UserSerializer(user,many=True)
		return Response(serilaizer.data)


      

