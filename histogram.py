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
    
    

def histogram_segmentation( image ):
    rows = image.shape[ 0 ]
    columns = image.shape[ 1 ]
    
    search_threshold = rows * 0.1
    idx_threshold = 2
    print "search_threshold " + str( search_threshold )
    
    horizontal, vertical = histograms( image )
    
    
    segments = [ idx for idx in range( len( horizontal ) )
                if horizontal[ idx ] < search_threshold ]
    
    filtered_segments = [ [ segments[ idx ], segments[ idx + 1 ] ] for idx in range( len( segments ) - 1 )
                        if segments[ idx + 1 ] - segments[ idx ] >= idx_threshold ]
    
    return filtered_segments
    
    
    
def test():
    colorImage = cv2.imread( "purePlates/plate018.jpg", 0 )
    
    horizontal, vertical = histograms( colorImage )
    
    #print horizontal
    #print vertical
    
    plt.plot( horizontal )
    plt.show()
    #plt.plot( vertical )
    #plt.show()
    
    segments = histogram_segmentation( colorImage )
    print segments
    
test()
