# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 14:33:03 2018

@author: ccorn
"""
from pythymiodw import *
from pythymiodw import io
from pythymiodw.sm import *
from libdw import sm
from time import sleep
from firebase import firebase
url = "https://waste-disposal.firebaseio.com/"
token = "2Xbca5bPhFYfeBWnQ14qZMUQ0BiU0ZxCBRuRGI8y"

firebase_sensor = firebase.FirebaseApplication(url, token)

token1='dLdtWXUFsAv4pfOBfae42s5t0m571PhsNY1FH8xc'
url1='https://guikivy-9f254.firebaseio.com/'

firebase_kivy =firebase.FirebaseApplication(url1, token1)

data = {"bin1": 0, "bin2": 0, "bin3": 0} #To be imported from firebase

barcode = {0: "bin1", 1: "bin2", 7: "bin3", 3: "2nd decision", 6: "stop"}
# bin3: all w (placed on the right, first dustbin encountered)
# bin2: first bit is white (right, second)
# bin1: all black (placed on the left for reading in two directions)
# 2nd decision: first and second bit white (placed on the intersection, right side)

class MySMClass(sm.SM):
    start_state = 0 #Thymio is on the starting line at rest
    reading1 = 0
    reading2 = 0
    reading3 = 0
    counter = -2
    counter_2 = 0
    def barcode_reader(self, reading1, reading2, reading3):
        # barcode comprises of 3 bits (reading1, reading2. reading3)
        info = 0
        if reading1 != 0:
            info += 1
        if reading2 != 0:
            info += 2
        if reading3 != 0:
            info += 4
        # info indicates the barcode in order 10
        return info
    
    def get_next_values(self, state, inp):

        if inp.button_backward:
            return 'halt', io.Action(0,0)
        #####################################
        ground = inp.prox_ground.delta
        wall = inp.prox_horizontal
        print(self.counter)
        print(data)
        #print(ground[0],ground[1])
        if wall[0] > 2500: # stop if there is obstacle in front
            forv = 0.0
            rotv = 0.0
            next_state = state
        elif state == 0: # at initial position
            data["bin1"] = [firebase_sensor.get("/Bin 1"), firebase_kivy.get("/Bin 1")]
            data["bin2"] = [firebase_sensor.get("/Bin 2"), firebase_kivy.get("/Bin 2")]
            data["bin3"] = [firebase_sensor.get("/Bin 3"), firebase_kivy.get("/Bin 3")]
            if 1 in data["bin2"] or 1 in data["bin3"]:
                forv = 0.0
                rotv = 0.0
                next_state = 1
            elif 1 in data["bin1"]:
                forv = 0.0
                rotv = 0.0
                next_state = 2
            else:
                #sleep(0.5)
                forv = 0.0
                rotv = 0.0
                next_state = 0
        elif state == 1: # bin2 or bin3 is full (can also be used as boundary follower)
            if ground[0] < 300 and ground[1] > 920: # breaking point (2nd intersection on the way back)
                sleep(7.5)
                forv = 0.03
                rotv = 0.0
                next_state = 5 # go to transition state
            elif ground[0] < 300: # first bit of barcode
                forv = 0.03
                rotv = 0.0
                next_state = 3
            elif ground[1] < 695: # black line (check value)
                forv = 0.0
                rotv = 0.05
                next_state = 1
            elif ground[1] < 894: # grey line (check value)
                forv = 0.03
                rotv = 0.0
                next_state = 1
            else:
                forv = 0.0
                rotv = -0.05
                next_state = 1
        elif state == 2: # bin1 is full
            if ground[1] < 695:
                forv = 0.0
                rotv = 0.05
                next_state = 2
            elif ground[1] < 920:
                forv = 0.03
                rotv = 0.0
                next_state = 2
            else:
                sleep(4.5)
                forv = 0.03
                rotv = 0.0
                next_state = 1

        elif state == 3: # barcode reading state
            if self.counter > 7: # this line marks the end of barcode
                forv = 0.0
                rotv = 0.0
                next_state = 4

            elif ground[0] > 700: # reading barcode in binary (white indicates 1 and black indicates 0)
                if self.counter == 0:
                    self.reading1 = 1
                elif self.counter == 2:
                    self.reading2 = 2
                elif self.counter == 6:
                    self.reading3 =  4
                forv = 0.03
                rotv = 0.0
                next_state = 3

            else:
                forv = 0.03
                rotv = 0.0
                next_state = 3
            self.counter += 1
        elif state == 4: # determining bin identity and next action
            self.counter = -2
            # print(barcode[self.barcode_reader(self.reading1, self.reading2, self.reading3)])
            # barcode_reader method is called to interpret the binary numbers into order 10
            # this value is then used to identify the bin
            if barcode[self.barcode_reader(self.reading1, self.reading2, self.reading3)] == "stop": # stopping thymio when it is at the initial position
                forv = 0.0
                rotv = 0.0
                next_state = 0
            elif barcode[self.barcode_reader(self.reading1, self.reading2, self.reading3)] == "2nd decision": # This is to decide whether Thymio will return to initial position or continue to collect bin1
                if 1 in data["bin1"]: # continue to bin1
                    sleep(4.2)
                    forv = 0.05
                    rotv = 0.0
                    next_state = 5      
                else: # return to initial position
                    forv = 0.0
                    rotv = 0.08
                    next_state = 6                  
            elif 1 in data[barcode[self.barcode_reader(self.reading1, self.reading2, self.reading3)]]: # check whether current bin is full
                forv = 0.0
                rotv = 0.0
                next_state = 5 # Thymio stops to collect trash 
            else: # bin is empty, return to boundary follower (state 1)
                forv = 0.05
                rotv = 0.0
                next_state = 1
        elif state == 5: # Transition state (to ignore commands for a fixed period of time)
            print("trans")
            forv = 0.05
            rotv = 0.0
            sleep(1.5)
            next_state = 1
        elif state == 6: # finding its way to the line to return to initial position
            sleep(3.5)
            forv = 0.05
            rotv = 0.0
            if self.counter_2 <= 3:
                self.counter_2 += 1
                next_state = 6
            else:
                self.counter_2 = 0
                next_state = 1
                
                

        return next_state, io.Action(fv = forv, rv = rotv)

    #########################################
    # Don't modify the code below.
    # this is to stop the state machine using
    # inputs from the robot
    #########################################
    def done(self,state):
        if state=='halt':
            return True
        else:
            return False

MySM=MySMClass()

############################

m=ThymioSMReal(MySM)
try:
    m.start()
except KeyboardInterrupt:
    m.stop()
