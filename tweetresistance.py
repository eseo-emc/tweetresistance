import colorcode
import twitpic
import random
import datetime

twitterClient = twitpic.TwitpicClient()

gameStart = twitterClient.now()
targetTotalValue = random.randint(2000,60000000)

print 'Try to approach {value:d} ({value:.1e})'.format(value=targetTotalValue)
raw_input('Press any key to stop the game...')

winner = 'nobody'
winnerDifference = 1000000000000
for tweet in twitterClient.tweetsSince(datetime.datetime(2016, 4, 18, 14, 35, 28)): #gameStart):
    try:    
        code = colorcode.ColorCode(tweet.photoUrl())
        totalValue = code.totalValue()
    except ValueError as error:
        print 'Error for {name}: {error}'.format(name=tweet.text(), error=error)
    else:

        print '* {text}: {value:.1e} ({code})'.format(text=tweet.text(), value=totalValue, code=code)
        
        difference = abs(totalValue-targetTotalValue)
        if difference < winnerDifference:
            winner = tweet.text()
            winnerDifference = difference
        
print 'The winner is',winner
        