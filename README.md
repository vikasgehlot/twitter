API endpoints

User can be added at /api/user/
tweets can be added at /api/tweets/
User can login to acces it from Browser now

Basic Authentication is used 

1) /api/tweets/
   To get all the tweets by all the users whom authenticated user follows as well as tweets by logged/request in user in past 1 day.
   This is the timeline of request user

   sample output
    {
        "id": 11,
        "tweet": "",
        "author": "",
        "likes": 1,
        "retweets": 0
    },



2) /api/tweets/id/action/
   action can be like,unlike,retweet,unretweet
   only if tweet belong to user or users followed by

   output only satus code




3) /api/tweets/id/
   To get details of a particular tweet, details include names of users who liked or retweeted but will only display names of user followed by request user.
   only if tweet belong to user or users followed by

      sample output
   {
    "id": 11,
    "tweet": "",
    "author": "",
    "likes": 1,
    "retweets": 0,
    "like": [
    ""
        
    ],
    "retweet": []
}



4) /api/follower/
   list all the followers of the request user
   A parameter caan be passed user=username will give the follower of the user only if the user is followed by request user

   [
    {
        "username": ,
        "followers": [
        ""
            
        ]
    }
]

  /api/following/
  it will list all the users whom request user is following ,also parameter can be given as above

  {
    "username": ,
    "following": [
    ""
    ""
       
    ]
}



Additional endpoints
api/follow/username To follow a user
api/unfolow/username  To unfollow a user


User can be added at /api/user/
tweets can be added at /api/tweets/
User can login to acces it from Browser now