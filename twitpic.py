import twitter # https://github.com/bear/python-twitter
from datetime import datetime


class TwitpicClient(object):
    def __init__(self):
#        SjoerdOptLand.5941@twitpic.com
        self.api = twitter.Api(consumer_key='42wttE14N2RoLomzYOL5ILx0d',
                      consumer_secret='uJm3ZwheGrPU6RDxZADeJF8VQQHCFK3TCgNslJF5066PqA7jO5',
                      access_token_key='2443815272-j85ikskshZzB7fbhZAVYSZFhP5GYJ2KMIzo6QS8',
                      access_token_secret='9MkXOaKiJkiSojg2jeYTPmeUlltJhBkCZpkVxZVGSwC5F')
                      
        self.user = self.api.GetUser(screen_name='SjoerdOptLand')

  
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
    def rawText(self):
        return self.status.GetText()
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
    
