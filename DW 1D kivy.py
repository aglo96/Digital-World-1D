# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 23:47:41 2018

@author: admin
"""

#==============================================================================
# from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# import matplotlib.pyplot as plt
# from firebase import firebase
# 
# plt.bar([0,1,2],[212,357,300])
# plt.ylabel('some numbers')
# token='dLdtWXUFsAv4pfOBfae42s5t0m571PhsNY1FH8xc'
# 
# url='https://guikivy-9f254.firebaseio.com/'
# 
# firebase=firebase.FirebaseApplication(url,token)
# 
#         
# 
# class MyApp(App):
# 
#     def build(self):
#         box = BoxLayout()
#         box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
#         return box
# 
# MyApp().run()   
#==============================================================================
#==============================================================================
# from kivy.app import App
# from kivy.uix.gridlayout import GridLayout
# from kivy.lang import Builder
# from kivy.uix.button import Button
# from firebase import firebase
# 
# token='dLdtWXUFsAv4pfOBfae42s5t0m571PhsNY1FH8xc'
# 
# url='https://guikivy-9f254.firebaseio.com/'
# 
# firebase=firebase.FirebaseApplication(url,token)
# 
# Builder.load_string("""
# <Dw>
#     rows:2
#     cols:3
#     Label:
#         text:'Bin 1'
#         font_size:32
# 
#     Label:
#         text:'Bin 2'
#         font_size:32
#     Label:
#         text:'Bin 3'
#         font_size:32
#     Button:
#         id:bin1
#         text:'Collect'
#         font_size:32
#         on_press:root.collect1()
# 
#     Button:
#         id:bin2
#         text:'Collect'
#         font_size:32
#         on_press:root.collect2()
#         
#     Button:
#         id:bin3
#         text:'Collect'
#         font_size:32
#         on_press:root.collect3()
# 
# 
# """)
# 
# class Dw(GridLayout):
#     c1=1
#     c2=1
#     c3=1
#     def collect1(self):
#         self.c1+=1
#         if self.c1%2==0:
#             output=firebase.put("/","Bin 1", "True")
#         else:
#             output=firebase.put("/","Bin 1", "False")
#         return output
#    
#     def collect2(self):
#         self.c2+=1
#         if self.c2%2==0:
#             output=firebase.put("/","Bin 2", "True")
#         else:
#             output=firebase.put("/","Bin 2", "False")
#         return output
#     
#     def collect3(self):
#         self.c3+=1
#         if self.c3%2==0:
#             output=firebase.put("/","Bin 3", "True")
#         else:
#             output=firebase.put("/","Bin 3", "False")
#         return output
#     
# class DwApp(App):
#     def build(self):
#         return Dw()
# 
# DwApp().run()
#==============================================================================


from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from firebase import firebase
from kivy.clock import Clock

token='dLdtWXUFsAv4pfOBfae42s5t0m571PhsNY1FH8xc'

url='https://guikivy-9f254.firebaseio.com/'

firebase=firebase.FirebaseApplication(url,token)

Builder.load_string("""
<Dw>
    rows:3
    cols:3
    Label:
        text:'Bin 1'
        font_size:32

    Label:
        text:'Bin 2'
        font_size:32
    Label:
        text:'Bin 3'
        font_size:32
    Label:
        id:bin1
        text:root.bin1
        font_size:32
        color:1,1,1,1
    
    Label:
        id:bin2
        text:root.bin2
        font_size:32
        color:1,1,1,1
    Label:
        id:bin3
        text:root.bin3
        font_size:32
        color:1,1,1,1
    
    ToggleButton:
        text:'Collect'
        font_size:32
        on_press:root.collect1()

    ToggleButton:
        text:'Collect'
        font_size:32
        on_press:root.collect2()
        
    ToggleButton:
        text:'Collect'
        font_size:32
        on_press:root.collect3()
    

""")

class Dw(GridLayout):
    def __init__(self):
        super().__init__()
        Clock.schedule_interval(self.collect4,3)
        Clock.schedule_interval(self.collect5,3)
        Clock.schedule_interval(self.collect6,3)
    c1=1
    c2=1
    c3=1
    bin1=''
    bin2=''
    bin3=''
    def collect1(self):
        self.c1+=1
        print(self.c1)
        if self.c1%2!=0:
            output=firebase.put("/","Bin 1", "True")
        else:
            output=firebase.put("/","Bin 1", "False")
        return output
   
    def collect2(self):
        self.c2+=1
        if self.c2%2!=0:
            output=firebase.put("/","Bin 2", "True")
        else:
            output=firebase.put("/","Bin 2", "False")
        return output
    
    def collect3(self):
        self.c3+=1
        if self.c3%2!=0:
            output=firebase.put("/","Bin 3", "True")
        else:
            output=firebase.put("/","Bin 3", "False")
        return output
    def collect4(self,apple):
        if firebase.get('/Bin 1')=='True':        
            self.bin1='Filled'
            self.ids.bin1.text = self.bin1
            self.ids.bin1.color=1,0,0,1
        elif firebase.get('/Bin 1')=='False':
            self.bin1='Empty'
            self.ids.bin1.text=self.bin1
            self.ids.bin1.color=1,1,1,1
            
    def collect5(self,apple):
        if firebase.get('/Bin 2')=='True':        
            self.bin2='Filled'
            self.ids.bin2.text = self.bin2
            self.ids.bin2.color=1,0,0,1
        elif firebase.get('/Bin 2')=='False':
            self.bin2='Empty'
            self.ids.bin2.text=self.bin2
            self.ids.bin2.color=1,1,1,1
            
    def collect6(self,apple):
        if firebase.get('/Bin 3')=='True':        
            self.bin3='Filled'
            self.ids.bin3.text = self.bin3
            self.ids.bin3.color=1,0,0,1
        elif firebase.get('/Bin 3')=='False':
            self.bin3='Empty'
            self.ids.bin3.text=self.bin3    
            self.ids.bin3.color=1,1,1,1

    
class DwApp(App):
    def build(self):
        return Dw()

DwApp().run()
