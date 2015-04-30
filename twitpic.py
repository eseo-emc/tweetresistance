import twitter # https://github.com/bear/python-twitter
from datetime import datetime


class TwitpicClient(object):
    def __init__(self):
#        SjoerdOptLand.5941@twitpic.com
        self.api = twitter.Api(consumer_key='QxilFASaWBzvu0Nv00ku8i5bg',
                      consumer_secret='ERrof3uzwNVqZQYepiijvLsX3ILIjC2RCPkdzHkgFywQwSxPif',
                      access_token_key='3223538032-uv5y8sUdMUwnbCgyuEE7tbkGcMmLoVv1FUcFjsq',
                      access_token_secret='LPPkb6L43SLDwK4LaJQZrFycoKIEbzcVK9uQYbkAGXVtf')
                      
        self.user = self.api.GetUser(screen_name='SjoerdEMC')

  
    def lastTweet(self):
        status = self.user.status
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
        return datetime.fromtimestamp(self.status.CreatedAtInSeconds)
    def rawText(self):
        return self.status.text
    def text(self):
        return ' '.join(self.rawText().split(' ')[:-1])
    def __str__(self):
        return self.text() + ' (' + self.photoUrl() + ')'

if __name__ == '__main__':
    client = TwitpicClient()
    tweet = client.lastTweet()
    print tweet.rawText()
    
#    start = client.now()
#    client.tweetsSince(start)
    
