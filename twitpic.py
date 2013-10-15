import twitter # https://github.com/bear/python-twitter
from datetime import datetime


class TwitpicClient(object):
    def __init__(self):
        self.api = twitter.Api(consumer_key='<your key here>',
                      consumer_secret='<your secret here>',
                      access_token_key='<your access key here>',
                      access_token_secret='<your access secret here>')
                      
        self.user = self.api.GetUser(screen_name='<your screen name here>')

  
    def lastTweet(self):
        status = self.user.GetStatus()
        return PhotoTweet(status)
#        photoLink = status.urls[0]
#        photoId = photoLink.expanded_url.split('/')[-1]              
#        return u'http://twitpic.com/show/thumb/'+photoId
    
    def now(self):
        return datetime.now()

        
    
    def tweetsSince(self,since=None):
        tweetList = []
        for status in self.api.GetUserTimeline(self.user):
            photoTweet = PhotoTweet(status)
            if since and photoTweet.createdAt() < since:
                break
            tweetList += [photoTweet]
        return tweetList
    

class PhotoTweet(object):
    def __init__(self,status):
        self.status = status
    def photoUrl(self):                
        return self.status.media[0][u'media_url']
    def createdAt(self):
        return datetime.fromtimestamp(self.status.created_at_in_seconds)
    def text(self):
        return ''.join(self.status.GetText().split(' ')[:-1])
    def __str__(self):
        return self.text() + ' (' + self.photoUrl() + ')'

if __name__ == '__main__':
    client = TwitpicClient()
    tweet = client.lastTweet()
    print tweet
    
#    start = client.now()
#    client.tweetsSince(start)
    
