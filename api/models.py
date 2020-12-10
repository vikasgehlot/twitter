from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


#Here follower indicates the people followed by the request user
class Follower(models.Model):
	username=models.OneToOneField(User,null=True,on_delete=models.CASCADE )
	followers=models.ManyToManyField(User,related_name='follow',blank=True)
	def __str__(self):
		return str(self.username)
	

def create_follower(sender,instance ,created ,**kwargs):
	if created:
		Follower.objects.create(username=instance)
		print("follower created")

post_save.connect(create_follower,sender=User)



class Tweet(models.Model):
	tweet=models.CharField(max_length=280)
	created=models.DateTimeField(auto_now_add=True)
	author=models.ForeignKey(User,on_delete=models.CASCADE)
	likes=models.ManyToManyField(User,related_name='like',blank=True)
	retweets=models.ManyToManyField(User,related_name='ret',blank=True)

	def __str__(self):
		return self.tweet


class Reach(models.Model):
	tweet=models.ForeignKey(Tweet, related_name='tweet_reach')
	viewed=models.IntegerField()



	

	
