from django.urls import path
from . import views

urlpatterns=[

	path('follower/',views.follower),
	path('following/',views.following),

	path('user/',views.user),

	path('follow/<str:user>/',views.follow),
	path('unfollow/<str:user>/',views.unfollow),
	
	path('tweets/',views.tweets),
	path('tweets/<int:id>/',views.tweet_detail),
	path('tweets/<int:id>/like/',views.like),
	path('tweets/<int:id>/unlike/',views.unlike),
	path('tweets/<int:id>/retweet/',views.retweet),
	path('tweets/<int:id>/unretweet/',views.unretweet),

	

]