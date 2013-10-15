import twitter # https://github.com/bear/python-twitter
from datetime import datetime


class TwitpicClient(object):
    def __init__(self):
#        SjoerdOptLand.5941@twitpic.com
        self.api = twitter.Api(consumer_key='Z0zCm7psyCrIXlSgg4oLw',
                      consumer_secret='97djGNT5mJ0Qx4XXtbZNAx3TaWGtyKB5jV7wzTE',
                      access_token_key='1962326917-Bfrm5ZP60TrZSrf4PF9i7oHqqRxiELoomTLz49l',
                      access_token_secret='BeyZdsYYh0MeBluNYlE2RfihjQnyJqv4SLmlAWonLs')
                      
        self.user = self.api.GetUser(screen_name='DreojsSjoerd')

  
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
    
