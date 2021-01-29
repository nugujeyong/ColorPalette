from PIL import Image
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
import matplotlib.pyplot as plt
import sys
import os 

class ColorPalette:
    
    def __init__(self, eps, min_samples):
        self.widths = []
        self.heights = []
        self.img1 = None
        self.eps = eps
        self.min_samples = min_samples
        
    def get_pixel(self,filename):
        pixels = []
        filename = './images/'+filename
        img = Image.open(filename)
        self.img1 = img
        self.widths.append(self.img1.size[0])
        self.heights.append(self.img1.size[1])
        img = img.resize((128,128))
        width,height = img.size
        for i in range(width):
            for j in range(height):
                pixel = img.getpixel((i,j))
                pixels.append(pixel)
        return pixels, filename

    #computes dbscan combined with kmeans
    #changing parameters in dbscan(eps, min_samples) may change the results of the palette
    def get_colors(self,pixels, n_colors):
        
        dbscan = DBSCAN(eps = self.eps, min_samples= self.min_samples).fit(pixels)
        clusters = {}
        for i,cluster in enumerate(dbscan.labels_):
            if cluster not in clusters.keys():
                clusters[cluster] = []
            clusters[cluster].append(pixels[i])

        centerlist = []
        for key in clusters.keys():
            center = np.mean(np.array(clusters[key]),axis = 0)
            centerlist.append(np.array(center,dtype=int))
    
        kmeans = KMeans(n_clusters = n_colors, random_state = 10).fit(centerlist)
        centerlist = np.array(kmeans.cluster_centers_,dtype = int)
        return centerlist
        
    def make_palette(self,centerlist, filename):
        filename = filename.split('.')[-2].split('/')[-1]
        centerlist = tuple(map(tuple, centerlist))
        img2 = Image.open("palettesample_b.png", 'r')
        width,height = img2.size
        pixdata = img2.load()
        for i in range(0,1):
            for y in range(0, height):
                for x in range(0, width):
                    if pixdata[x, y] == (44,44,44): 
                        pixdata[x, y] = centerlist[i]
                    elif pixdata[x, y] == (45, 45, 45): 
                        pixdata[x, y] = centerlist[i+1]
                    elif pixdata[x, y] == (46,46, 46): 
                        pixdata[x, y] = centerlist[i+2]
                    elif pixdata[x, y] == (47,47, 47): 
                        pixdata[x, y] = centerlist[i+3]
                    elif pixdata[x, y] == (48,48, 48): 
                        pixdata[x, y] = centerlist[i+4]
                    elif pixdata[x, y] == (49,49, 49): 
                        pixdata[x, y] = centerlist[i+5]
                    elif pixdata[x, y] == (50,50, 50): 
                        pixdata[x, y] = centerlist[i+6]
                    elif pixdata[x, y] == (55,55, 55): 
                        pixdata[x, y] = centerlist[i+7]
        img2 = img2.resize((1448,1024))
        width,height = img2.size
        self.widths.append(width)
        self.heights.append(height)
        maxwidth = max(self.widths)
        sumheight = sum(self.heights)
        middlepoint1 = int(maxwidth/2-(self.img1.size[0]/2))
        middlepoint2 = int(maxwidth/2-(width/2))

        if not os.path.exists('./palettes'):
            os.makedirs('./palettes')
        
        new_image = Image.new('RGB',(maxwidth, sumheight), (250,250,250))
        new_image.paste(self.img1,(middlepoint1,0))
        new_image.paste(img2,(middlepoint2,self.img1.size[1]))
        new_image.save("./palettes/"+filename+"_palette.png")
        new_image.show()
    
    def run(self, filepath):
        pixels,filename = self.get_pixel(filepath)
        centerlist = self.get_colors(pixels, 8)
        self.make_palette(centerlist, filename)

if len(sys.argv) != 2:
    print("You have to include image file name")
    exit()

ColorPalette(eps = 2, min_samples = 3).run(sys.argv[1])



