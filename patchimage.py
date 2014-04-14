import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import pylab

from skimage import data
from skimage.filter import threshold_otsu
from skimage.segmentation import clear_border
from skimage.morphology import label, closing, square
from skimage.measure import regionprops
from skimage import color
from skimage.color import rgb2hsv,hsv2rgb,rgb2lab



def hsvToChromaticity(hue,saturation=1.0,value=1.0):
    hue = np.array(hue)
    hsvVector = np.array([np.array([hue,hue*0+saturation,hue*0+value]).T])
    rgbVector = color.hsv2rgb(hsvVector)
    return color.rgb2lab(rgbVector)[:,:,1:]
    
colorNames = ['red','orange','yellow','green','blue', 'purple']
colorRgbs = hsvToChromaticity(np.array([0.0, 30.0, 60.0, 120.0, 240.0, 300.0])  /360.0)
colorValues = [2,3,4,5,6,7]

class Color(object):
    def __init__(self,rgbValue):
        self.rgbValue = rgbValue
        
        self.chromaticity = color.rgb2lab(np.array([[rgbValue]]))[:,:,1:]
    
    def _findColorId(self):
        squaredDifferences = (colorRgbs-self.chromaticity)[0,:,0]**2 + (colorRgbs-self.chromaticity)[0,:,1]**2
        return np.argmin(squaredDifferences)
        
    @property
    def name(self):
        return colorNames[self._findColorId()]
    @property
    def value(self):
        return colorValues[self._findColorId()]
    
    
class Patch(object):
    def __init__(self,boundingBox,averageColor):
        self.boundingBox = boundingBox
        self.averageColor = averageColor
        
    def plot(self,axis):
        rect = mpatches.Rectangle(self.topLeft[::-1], self.width, self.height,
                                      fill=False, edgecolor='red', linewidth=2)
        axis.add_patch(rect)
        pylab.text(self.centroid[1],self.centroid[0],self.label(),color='red',horizontalalignment='center',verticalalignment='center')
    
    def label(self):
        return self.averageColor.name
        
    
    @property
    def centroid(self):
        return np.average(self.boundingBox,axis=0)
    
    @property
    def topLeft(self):
        return self.boundingBox[0,:]
    
    @property
    def height(self):
        return self.boundingBox[1,0]-self.boundingBox[0,0]
        
    @property
    def width(self):
        return self.boundingBox[1,1]-self.boundingBox[0,1]

class PatchImage(list):
    def __init__(self,imageUrl):
        self.rgbImage = data.imread(imageUrl)
        imageHsv = rgb2hsv(self.rgbImage)
        
        # http://scikit-image.org/docs/dev/auto_examples/plot_label.html
        # apply threshold
        imageSaturation = imageHsv[:,:,1]
        thresh = threshold_otsu(imageSaturation)
        bw = closing(imageSaturation > thresh, square(3))
        
        # remove artifacts connected to image border
        cleared = bw.copy()
        clear_border(cleared)
        
        # label image regions
        label_image = label(cleared)
        borders = np.logical_xor(bw, cleared)
        label_image[borders] = -1
              
                
        for region in regionprops(label_image, ['EquivDiameter','Coordinates','Area', 'BoundingBox']):
            # skip small images
            if region['Area'] < 100:
                continue
        
            # normalize boundingbox
            minr, minc, maxr, maxc = region['BoundingBox']
            boundingBox = np.array([[minr,minc],[maxr,maxc]])
        
            averageSide =  np.average(boundingBox[1,:]-boundingBox[0,:])
            sideDifference = np.abs(region['EquivDiameter']-averageSide)
            if sideDifference/averageSide > 0.1:
                continue
            
                     
            labeledRgbValues = self.rgbImage[label_image == region['Label'],:]
            averageRgbValue = np.average(labeledRgbValues,0)
            
            
            self.append(Patch(boundingBox,Color(averageRgbValue)))

            
    def show(self):
        fig, axis = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
        axis.imshow(self.rgbImage)

        for patch in self:
            patch.plot(axis)
            
        plt.show()
    
if __name__ == '__main__':
    from twitpic import TwitpicClient
    imageUrl = TwitpicClient().lastTweet().photoUrl()
    scannedImage = PatchImage(imageUrl)
    scannedImage.show()
