from PIL import Image
import numpy as np
from os import listdir
from os.path import isfile, join
from imgaug import augmenters as iaa


# img to numpy array
#pix = numpy.array(pic)
# numpy to img
#pic.putdata(pix)

def get_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img_file_name = image_path
    
    return img, img_file_name

def change_brightness(img):
    print(img)
    
#get_image('/Users/yannikhubrich/Documents/Studium/6Semester/DrunkFaceRecognition/Data/raw/alligned/d4a7a2_1b7fef8b5225436f923db06a76c52e4a.jpg_drei_glaeser.jpg')

# Change brightness of images (50-150% of original value).
#iaa.Multiply((0.5, 1.5), per_channel=0.5)