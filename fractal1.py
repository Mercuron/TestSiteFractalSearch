#PSP_boxCounting
from __future__ import print_function, division
import math
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def identifyPores(colorGrid, width, height, myColor,rgbthr):
    print("identifying pores...")
    nrPores = 0
    #rgbThreshold = 128          # 128, 128, 128 = gray
    rgbThreshold = rgbthr
    for x in range(width):
        for y in range(height):
            color = colorGrid[x, y]
            print("COLOR",color)
            if ((color[0] > rgbThreshold) and
                (color[1] > rgbThreshold) and (color[2] > rgbThreshold)):
                nrPores += 1
                colorGrid[x, y] = myColor
    return(nrPores, colorGrid)

def boxCounting(colorGrid, width, height, size, threshold, myColor):
    nrPixelsThreshold = threshold * size * size
    nrXBoxes = int(width / size)
    nrYBoxes = int(height / size)
    nrOccupiedBoxes = 0
    for i in range(nrXBoxes):
        for j in range(nrYBoxes):
            nrPorePixels = 0
            for dx in range(size):
                for dy in range(size):
                    x = i * size + dx
                    y = j * size + dy
                    color = colorGrid[x, y]
                    if color == myColor: nrPorePixels += 1
            if (nrPorePixels > nrPixelsThreshold):
                nrOccupiedBoxes += 1

    # normalized one-dimensional size
    L = 1./math.sqrt(nrXBoxes*nrYBoxes)
    # fractal dimension
    if (nrOccupiedBoxes > 0):
        D = math.log(nrOccupiedBoxes) / math.log(L)
    else:
        D = 0
    print ("ITS FROM LOOP box size =", size, " pores =", nrOccupiedBoxes,
           " L =", format(L, '.3f')," D =", format(D, '.3f'))
    outtext=str("box size =" + str(size)+ " pores ="+ str(nrOccupiedBoxes)+ " L ="+ str(format(L, '.3f'))+" D ="+ str(format(D, '.3f')))
    return(nrOccupiedBoxes,outtext)

def main_fractal(image,path,rgbthr):
    with Image.open(image) as picture:
        colorGrid = picture.load()
        [width, height] = picture.size
        nrPixels = width * height
        print ("width =", width)
        print ("height =", height)

        myColor = (255,0,0) 		# red, green, blue (0-255)
        nrPores, colorGrid = identifyPores(colorGrid, width, height, myColor,rgbthr)
        poresPercentage = float(nrPores) / float(nrPixels) * 100.
        print ("% of pores =", format(poresPercentage, '.3f'))
        picture.save(path+'result_of_fractal_pores.jpg')
        plt.xlabel('Box size',fontsize=16,labelpad=3)
        plt.ylabel('N',fontsize=16,labelpad=3)
        plt.ion()
        size = 200          			# pixels
        threshold = 0.2
        outarr=[]
        while (size >= 1):
            print('OurArr before boxcounting',outarr)
            nrOccupiedBoxes,out = boxCounting(colorGrid, width, height, size, threshold, myColor)
            print('OutArr after',outarr)
            outarr.append(out)
            print('OutArr after',outarr)
            if (nrOccupiedBoxes > 0):
                plt.loglog(size, nrOccupiedBoxes, 'ko')
                plt.draw()
            size = int(size / 2)

        plt.ioff()
        plt.savefig(path)
        plt.close()
        return(path,outarr)
