import colorcode
import twitpic
import random

twitterClient = twitpic.TwitpicClient()

gameStart = twitterClient.now()
targetTotalValue = random.randint(2000,60000000)

print 'Try to approach {value:d} ({value:.1e})'.format(value=targetTotalValue)
raw_input('Press any key to stop the game...')

winner = 'nobody'
winnerDifference = 1000000000000
for tweet in twitterClient.tweetsSince(gameStart):
    code = colorcode.ColorCode(tweet.photoUrl())
    totalValue = code.totalValue()
    
    print '* {text}: {value:.1e} ({code})'.format(text=tweet.text(), value=totalValue, code=code)
    
    difference = abs(totalValue-targetTotalValue)
    if difference < winnerDifference:
        winner = tweet.text()
        winnerDifference = difference
        
print 'The winner is',winner
        