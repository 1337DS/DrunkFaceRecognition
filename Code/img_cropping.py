from PIL import Image
import re
import cv2
from os import listdir
from os.path import isfile, join


def convert_webp_to_jpg(path_of_image):
    img = Image.open(path_of_image).convert('RGB')
    path_to_safe = re.sub(r'\.webp', '.jpg', path_of_image)
    #print(path_to_safe)
    path_to_safe = re.sub(r'\/webp', '/jpg', path_to_safe)
    #print(path_to_safe)
    img.save(path_to_safe)
    return path_to_safe

def make_four_out_of_one(path_of_image):
    img = cv2.imread(path_of_image)
    path_to_safe = 'Data/raw/cropped_to_four/'
    file_name = re.sub(r'^Data\/raw\/jpg\/', '', path_of_image)
    path_to_safe = path_to_safe + file_name
    ##########################################
    # At first vertical devide image         #
    ##########################################
    
    # start vertical devide image
    height = img.shape[0]
    width = img.shape[1]
    
    # Cut the image in half
    width_cutoff = width // 2
    left1 = img[:, :width_cutoff]
    right1 = img[:, width_cutoff:]
    # finish vertical devide image
    
    
    ##########################################
    # At first Horizontal devide left1 image #
    ##########################################
    
    #rotate image LEFT1 to 90 CLOCKWISE
    img = cv2.rotate(left1, cv2.ROTATE_90_CLOCKWISE)
    
    # start vertical devide image
    height = img.shape[0]
    width = img.shape[1]
    
    # Cut the image in half
    width_cutoff = width // 2
    l1 = img[:, :width_cutoff]
    l2 = img[:, width_cutoff:]
    # finish vertical devide image
    
    #rotate image to 90 COUNTERCLOCKWISE
    l1 = cv2.rotate(l1, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #rotate image to 90 COUNTERCLOCKWISE
    l2 = cv2.rotate(l2, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    
    ##########################################
    # At first Horizontal devide left1 image #
    ##########################################
    
    #rotate image LEFT1 to 90 CLOCKWISE
    img = cv2.rotate(left1, cv2.ROTATE_90_CLOCKWISE)
    
    # start vertical devide image
    height = img.shape[0]
    width = img.shape[1]
    
    # Cut the image in half
    width_cutoff = width // 2
    l1 = img[:, :width_cutoff]
    l2 = img[:, width_cutoff:]
    # finish vertical devide image
   
    #rotate image to 90 COUNTERCLOCKWISE
    l1 = cv2.rotate(l1, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #save
    cv2.imwrite(f"{path_to_safe}_zwei_glaeser.jpg", l1)
    
    #rotate image to 90 COUNTERCLOCKWISE
    l2 = cv2.rotate(l2, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #save
    cv2.imwrite(f"{path_to_safe}_null_glas.jpg", l2)
    
    
    ##########################################
    # At first Horizontal devide right1 image#
    ##########################################
    
    #rotate image RIGHT1 to 90 CLOCKWISE
    img = cv2.rotate(right1, cv2.ROTATE_90_CLOCKWISE)
    # start vertical devide image
    height = img.shape[0]
    width = img.shape[1]
    
    # Cut the image in half
    width_cutoff = width // 2
    r1 = img[:, :width_cutoff]
    r2 = img[:, width_cutoff:]
    # finish vertical devide image
    
    #rotate image to 90 COUNTERCLOCKWISE
    r1 = cv2.rotate(r1, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #save
    cv2.imwrite(f"{path_to_safe}_drei_glaeser.jpg", r1)
    
    #rotate image to 90 COUNTERCLOCKWISE
    r2 = cv2.rotate(r2, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #save
    cv2.imwrite(f"{path_to_safe}_ein_glas.jpg", r2)

def get_files_to_crop(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def convert_all():
    file_list = get_files_to_crop('Data/raw/webp')
    print(file_list)
    for i in file_list:
        path = f'Data/raw/webp/{i}'
        make_four_out_of_one(convert_webp_to_jpg(path))

convert_all()