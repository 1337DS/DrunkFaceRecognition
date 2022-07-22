import pickle
import pandas as pd
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

from face_functions import allign_face, check_for_face, get_facial_landmarks

def get_model(path_to_model):
    loaded_model = pickle.load(open(path_to_model, 'rb'))
    return loaded_model

def get_image(image_path):
    img = Image.open(image_path).convert('RGB')
    #print(type(img))
    img_file_name = image_path
    
    return img, img_file_name

def make_prediction(path_to_file):
    prediction_model = get_model('random_forest_drunken_face_predictor.sav')
    if check_for_face(path_to_file) == True:
        print('yes')
        img = allign_face(path_to_file)
        print('-----------------------', type(img), '-----------------------')
        df = get_facial_landmarks(img)
        #print(df)
        data = df.values
        print(data)
        print(type(data))
        prediction = prediction_model.predict(data)
        prediction = int(prediction[0])
        print(prediction)
        file = open("result.txt", "w")
        file.write(f'{prediction}')
        file.close()
        return prediction
        
        
    
    #print(img)
    
    
    

#make_prediction('/Users/yannikhubrich/Documents/Studium/6Semester/DrunkFaceRecognition/Data/camer_roll/71829863_394586244763145_7808846751268751762_n.jpeg')
make_prediction('foo.jpg')