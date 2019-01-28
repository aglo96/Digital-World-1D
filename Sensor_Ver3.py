import RPi.GPIO as GPIO
import time
from firebase import firebase

url = "https://waste-disposal.firebaseio.com/"
token = "2Xbca5bPhFYfeBWnQ14qZMUQ0BiU0ZxCBRuRGI8y"

firebase = firebase.FirebaseApplication(url, token)

data1 = firebase.get("/Bin 1")
data2 = firebase.get("/Bin 2")
data3 = firebase.get("/Bin 3")


GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)

# green for input
# orange for power in
# yellow for ground

c1 = 0
c2 = 0
c3 = 0

while True:
    i = GPIO.input(18)
    j = GPIO.input(23)
    k = GPIO.input(24)
    
    if i == 0:
        print ("Bin 1 Active")
        time.sleep(0.1)
        c1 += 1
        if c1 >= 3:
            firebase.put("/", "Bin 1", 1)
            c1 = 0
    elif i == 1:
        print ("Bin 1 Inactive")
        firebase.put("/", "Bin 1", 0)
        time.sleep(0.1)

    if j == 0:
        print ("Bin 2 Active")
        time.sleep(0.1)
        c2 += 1
        if c2 >= 3:
            firebase.put("/", "Bin 2", 1)
            c2 = 0
    elif j == 1:
        print ("Bin 2 Inactive")
        firebase.put("/", "Bin 2", 0)
        time.sleep(0.1)
        
    if k == 0:
        print ("Bin 3 Active")
        time.sleep(0.1)
        c3 += 1
        if c3 >= 3:
            firebase.put("/", "Bin 3", 1)
            c3 = 0
    elif k == 1:
        print ("Bin 3 Inactive")
        firebase.put("/", "Bin 3", 0)
        time.sleep(0.1)
