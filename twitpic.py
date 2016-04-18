import twitter # https://github.com/bear/python-twitter
from datetime import datetime


class TwitpicClient(object):
    def __init__(self):
        self.api = twitter.Api(consumer_key='zejoKxmd6rFVKE3UNyxIUFvJR',
                      consumer_secret='xCh6Ad08Ni91T4fvjYUj3sj8OW8buWH2kAp4t3sooKRNZcj1cu',
                      access_token_key='3223538032-39HR7hZGURNqS4vPuxD5Cv7p5px611u8rmEDnjU',
                      access_token_secret='acbHQsemLRIaEFNGBpPhAk0zFkIHyiSxFUlWHbROZoeaZ')
                      
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
        return self.status.media[0].media_url
    def createdAt(self):
        return datetime.fromtimestamp(self.status.created_at_in_seconds)
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
    
