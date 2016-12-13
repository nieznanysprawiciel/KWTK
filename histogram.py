import cv2
import numpy as np
import matplotlib.pyplot as plt



def histograms( image ):
    print image.shape
    
    rows = image.shape[ 0 ]
    columns = image.shape[ 1 ]
    
    horizontal = [0] * columns
    vertical = [0] * rows
    
    for rowIdx in range( rows ):        # rows
        for colIdx in range( columns ):    # columns
            value = image[ rowIdx, colIdx ]
            if value > 0:
                value = 0
            else:
                value = 1
            
            vertical[ rowIdx ] += value
            horizontal[ colIdx ] += value

    return horizontal, vertical
    
    
    
def test():
    colorImage = cv2.imread( "purePlates/plate018.jpg", 0 )
    
    horizontal, vertical = histograms( colorImage )
    
    print horizontal
    print vertical
    
    plt.plot( horizontal )
    plt.show()
    plt.plot( vertical )
    plt.show()
    
test()
