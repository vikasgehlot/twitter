from django.contrib import admin
from .models import Follower,Tweet




class TweetAdmin(admin.ModelAdmin):
	# inlines=[TweetLikeAdmin,]
	list_display=['__str__','author']
	search_fields=['author__username','tweet']
	class Meta:
		model=Tweet
	

admin.site.register(Tweet,TweetAdmin)
admin.site.register(Follower)

