import twitpic
import patchimage
import numpy as np

class ColorCode(patchimage.PatchImage):
    def resistors(self):
        if len(self) % 3 > 0:
            raise ValueError, 'Did not recognize multiple of 3 patches, but {0}'.format([patch.averageColor.name for patch in self])
        resistorValues = []
        colorNames = []
        for (decimalOne,decimalTwo,exponent) in zip(self[0::3],self[1::3],self[2::3]):
            resistorValue = (10*decimalOne.averageColor.value \
                + decimalTwo.averageColor.value) \
                * 10**exponent.averageColor.value
            resistorValues.append(resistorValue)
            colorNames.append('{0:s}-{1:s}*10^{2:s}'.format(decimalOne.averageColor.name, \
                                                           decimalTwo.averageColor.name, \
                                                           exponent.averageColor.name))
        return (resistorValues,colorNames)
        
    def resistorValues(self):
        (resistorValues,dummy) = self.resistors()
        return np.array(resistorValues)
    def colorNames(self):
        (dummy,colorNames) = self.resistors()
        return np.array(colorNames)            
            
    def totalValue(self):
        return self.resistorValues().sum()
    def __str__(self):
        return ', '.join(self.colorNames())
                    
if __name__ == '__main__':
    twitpicClient = twitpic.TwitpicClient()
    imageUrl = twitpicClient.lastTweet().photoUrl()
    
    scannedImage = ColorCode(imageUrl)
    scannedImage.show()
    
    print scannedImage        
    print scannedImage.resistors()
    