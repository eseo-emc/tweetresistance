import twitpic
import patchimage

class ColorCode(patchimage.PatchImage):
    def resistors(self):
        if len(self) % 3 > 0:
            raise ValueError, 'Did not recognize multiple of 3 patches'
#        for patch in self:
#            print patch.averageColor.name, patch.averageColor.value
        resistorValues= []
        for (decimalOne,decimalTwo,exponent) in zip(self[0::3],self[1::3],self[2::3]):
            resistorValue = (10*decimalOne.averageColor.value \
                + decimalTwo.averageColor.value) \
                * 10**exponent.averageColor.value
            resistorValues.append(resistorValue)
        return resistorValues
            
    def totalValue(self):
        value = 0
        for resistor in self.resistors():
            value += resistor
        return value
                    
if __name__ == '__main__':
    twitpicClient = twitpic.TwitpicClient()
    imageUrl = twitpicClient.lastTweet().photoUrl()
    
    scannedImage = ColorCode(imageUrl)
    scannedImage.show()
    
    print scannedImage.resistors()