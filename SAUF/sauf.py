#!/usr/bin/env python
from os import listdir
from os.path import isfile, join
from picamera import PiCamera 
from datetime import datetime
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
reader = SimpleMFRC522()
camera = PiCamera() 
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)


# Anzahl maximal erlaubter Drinks 
maxdrinks=3
# Schleife die permanent durchläuft
while True:
  try:
    #gibt die ID des chips aus
    print("S.A.U.F. online")
    id, text = reader.read()  
    print('id ',id,' erkannt')
    #optional Ausgabe für auf chip gespeichertem text 
    # print(text)
    
    # Abfrage Dateien in Verzeichnis
    dateien=[d for d in listdir('/home/pi/Desktop/drunkfaces') if isfile(join('/home/pi/Desktop/drunkfaces',d))]    
    #print(dateien)
    anzahl=sum(str(id) in s for s in dateien)
    print('Anzahl getrunkener Getränke:', anzahl)
    if anzahl>maxdrinks:
        print('Maximale Anzahl an Drinks erreicht')	
        GPIO.output(7,True)
        sleep(1)
        GPIO.output(7,False)
    # Bildname, zusammengesetzt aus id + Anzahl Drinks + Uhrzeit
    now=datetime.now()
    aktuelle_uhrzeit=now.strftime("%H_%M")
    bildname=str(id)+'_'+str(anzahl)+'_'+aktuelle_uhrzeit+'.jpg'

    # Aufnahme des Bildes, Bestätigung mit grüner LED und 10 Sekunden Wartezeit um Doppelbilder zu vermeiden 
    sleep(1)
    camera.capture('/home/pi/Desktop/drunkfaces/'+bildname)
    GPIO.output(7,True)
    sleep(1)
    GPIO.output(7,False)
    sleep(10)  
  
  except KeyboardInterrupt:
    print('interrupted!')
    break
  




