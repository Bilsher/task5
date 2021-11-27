import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from scipy.ndimage import label
from skimage.filters import threshold_otsu, gaussian
from skimage import color

from skimage.exposure import adjust_sigmoid
from skimage.transform import resize
from skimage.filters import (gaussian, threshold_otsu, 
                             threshold_local, 
                             threshold_yen, 
                             threshold_li)

def check(image, y, x): 
	if not 0 <= x < image.shape[1]: 
		return False 
	if not 0 <= y < image.shape[0]: 
		return False 
	if image[y, x] != 0: 
		return True 
	return False 

 

def neighbors8(image,y, x):
    return (y-1, x), (y-1, x+1), (y, x+1), (y+1, x+1), (y+1, x), (y+1, x-1), (y, x-1), (y-1, x-1)

 
def neighbours4(image, y, x): 
	left = y, x - 1 
	top = y - 1, x 
	right = y, x + 1 
	down = y + 1, x 
	if not check(image, *left): 
		left = None, None 
	if not check(image, *top): 
		top = None, None 
	if not check(image, *right): 
		right = None, None 
	if not check(image, *down): 
		down = None, None 
	return left, top, right, down 

def area(LB, label = 1): 
	pxs = np.where(LB == label) 
	return len(pxs[0]) 
 
def get_boundaries(LB, label = 1): 
	pxs = np.where(LB == label) 
	boundaries = [] 
	for y, x in zip(*pxs): 
		for yn, xn, in neighbours4(LB, y, x): 
			if yn == None: 
				boundaries.append((y,x)) 
				break 
			elif xn == None: 
				boundaries.append((y,x)) 
				break 
			elif LB[yn, xn] != label: 
				boundaries.append((y,x)) 
				break 
	return boundaries
 
def perimeter(LB, label = 1): 
	return len(get_boundaries(LB, label)) 


def pencils(arrpic, path):
    counter = 0
    
    for pic in arrpic:
        image = plt.imread(path + pic)
        pin = color.rgb2gray(image)
        pin = resize(pin, (pin.shape[0]//10, pin.shape[1]//10))
        pin = adjust_sigmoid(pin, cutoff=10, gain=3)
        pin = gaussian(pin, sigma=3)
        
        binary = pin.copy()
        binary[pin >= threshold_otsu(pin)] = 0
        binary[binary > 0] = 1
    
        labeled = label(binary)[0]
        
        for i in range(1, np.max(labeled) + 1):
            S = area(labeled, i)
            P = perimeter(labeled, i)
            Pen_P = S / P
            if 5 < Pen_P < 11 and 2870 < S < 5450:
                counter += 1
                
    return(str(counter))

def find(label, linked):
    x = label
    while linked[x] != 0:
        x = linked[x]
    return x

path = "images/"
arrpic = [pic for pic in listdir(path)]
print("Pencils: " + pencils(arrpic,path))