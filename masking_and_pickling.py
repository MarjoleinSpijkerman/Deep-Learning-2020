#!/usr/bin/python
#By Marjolein Spijkerman (S3219305)
import cv2
import os
import numpy
import random
import cv2
from PIL import Image, ImageDraw, ImageFilter
import pickle

#This is used to create the square masks
def create_square_mask(min_x,min_y,max_x,max_y):
    im = Image.new("RGB", (64, 64), "white")
    im.paste((0,0,0),(min_x,min_y,max_x,max_y))
    open_cv_image = numpy.array(im)
    #open_cv_image = cv2.resize(open_cv_image, (64, 64))
    return open_cv_image

#https://note.nkmk.me/en/python-pillow-square-circle-thumbnail/
#This is used to create the circular masks
def create_circular_mask(min_x, min_y, max_x, max_y):
    im_new = Image.new("RGB", (64,64), "black")
    background = Image.new(im_new.mode, (64,64), "white")
    mask = Image.new("L",im_new.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((min_x, min_y, max_x, max_y), fill=255)
    im = Image.composite(im_new, background, mask)
    open_cv_image = numpy.array(im)
    #open_cv_image = cv2.resize(open_cv_image, (64, 64))
    return open_cv_image

#determine whether to create a circular or square mask, plus size and location
def create_mask():
	x1 =0
	x2 =0
	y1 =0 
	y2 = 0
	while ((abs(x1-x2) < 6) or (abs(x1-x2) > 25)):
		x1 = random.randint(0,256)
		x2 = random.randint(0,256)

	while ((abs(y1-y2) < 6) or (abs(y1-y2) > 25)):
		y1 = random.randint(0,256)
		y2 = random.randint(0,256)

	min_x = min(x1, x2)
	max_x = max(x1, x2)
	min_y = min(y1, y2)
	max_y = max(y1, y2)

	rndm = random.randint(0,1)
	if rndm is 1:
		im = create_square_mask(min_x, min_y, max_x, max_y)
		return im
	elif rndm is 0:
		im = create_circular_mask(min_x, min_y, max_x, max_y)
		return im

#Run the program
def load_images_from_folder2(folder):
	#for all images in the folder do
    for filename in os.listdir(folder):
		#here we load the image
        path = folder + '/' + filename
        img = cv2.imread(path)
        img = cv2.resize(img, (64, 64))
        #here we save the name of the image
        name = filename
        name = ''.join(map(str, name))
        name = name[:-4]
        #Here we create the path where we will save the first pickle
        path1 = "/media/tux/Backup/pickles_resized/boat_deck/"
        path1 = path1 + name + ".pickle"
        #Here we pickle the original image
        pickling_on = open(path1,"wb")
        pickle.dump(img, pickling_on)
        pickling_on.close()
        
        i = 0
        #We create 3 masks per image
        for num in range (3):
			#add the number of the mask
            i = i+1
            
            #create the mask
            src2 = create_mask()
            src2 = cv2.resize(src2, img.shape[1::-1])
            dst = cv2.bitwise_and(img, src2)
            
            #save the mask as pickle
            mask_name = "/media/tux/Backup/pickles_resized/boat_deck/" + name +  "_mask" + str(i) + ".pickle"
            #print(mask_name)
            pickling_on = open(mask_name,"wb")
            pickle.dump(src2, pickling_on)
            pickling_on.close()
            
            #create the path for combined item
            new = name 
            new = new + "_combined" + str(i)
            new = ''.join(map(str, new))
            path = "/media/tux/Backup/pickles_resized/boat_deck/"
            path = path + new + ".pickle"
            #print(path)
			#Pickle the combined image
            pickling_on = open(path,"wb")
            pickle.dump(dst, pickling_on)
            pickling_on.close()            

#Fill in the correct folder. Also define the save location in line 72, 91 and 101 !!!
path = "/media/tux/Backup/data/b/" + "boat_deck"
images = load_images_from_folder2(path)

