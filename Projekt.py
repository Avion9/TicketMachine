#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#Wichtig Imports
import math
import numpy as np
from tkinter import * 
from tkinter import filedialog,messagebox
import tkinter as tk 
import pathlib
import os


#Alle Fahrpreisen in ein Array speichern von 0.90 bis 19.90
Fahrpreisen =[]
for i in np.arange(90,2000,10):
    i=i/100
    Fahrpreisen.append(i)
#diese funktion pruft ob die eingabe Preis ist richtig oder falsh
def preischeck(preis):
    if preis in Fahrpreisen :
        return preis
    else :
        return 0
#diese funktion berechnt die total Betrag in ein Array und zuruckliefert einen Betrag im Cents zum beispiel 300 cents => 3 Euro
def getTotal(list):
    stücke = [1000 , 500 , 200 , 100 , 50 , 20 , 10]
    amount = 0
    for i in range(len(list)):
        amount = int(amount) + (int(int(list[i])) * int(stücke[i]))
        amount=int(amount)
    return amount
#diese funktion berechnt die Gesamtbestand ,sie hat zwei operationen minus und plus 
#minus : nachzieht die Ruckgabe zu
#plus : fügen Sie die Eingabe betrag zu

def addToGesamtbestand(values,stock,operation):
    nStock=[0]*7
    nStock=stock
   
    for i in range(len(stock)-len(values),len(stock)):
           
        if operation=="+":
            nStock[i]=values[i-(len(stock)-len(values))]+stock[i]
        elif operation=="-" :
            nStock[i]=stock[i]-values[i-(len(stock)-len(values))]
                
    return nStock

#diese funktion überprüft Sie die Münzen in der Maschine und berechnet die Ruckgabe dann liefert die Ruckgabe 
def Ruckgabe(value,preis,stock) :
    Stücke=[1000 , 500 , 200 , 100 , 50 , 20 , 10]
    out = [0]*7
    p=preis * 100
    k=int(getTotal(value)-p)
    if k<0 :
        raise AttributeError("Sorry, Zuwenig Geld ")
        
    for i in range (2,7):
        out[i]=int(k/Stücke[i])
        k= k % Stücke[i]
      
        if out[i] > stock[i] :
            k= k % Stücke[i] + (out[i]-stock[i])*Stücke[i]
            out[i]=stock[i]
           
    if k!=0 :
        raise ValueError("Sorry, keine Münzen mehr")
    
    return out

#hier erstellen wir ein Window fur die Programm
window = Tk()
window.title('FahrKartenAutomat')
window.configure(background='white')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.geometry("1050x170")

#mit diese Funktion konnen wir ein File durchsuchen und den Path "://C:beispiel/.." auf dem Bildschirm anzeigen
def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
    
    # Change label contents
    txt.insert(0,filename)
    txt.place(x=200, y=10)
    

#hier ist die main funktion wenn wie klicken Generate diese Funktion fuhrt aus.
    
def GenerateOutputs():
    #liest den pfadinformationen 
    path = txt.get()
    filename = str(path)
    ausgangszustand=[0]*7
    Geschäftsvorgänge=[]
    lineIndex=0
    Kommentare=""
    #eine Ausgabedatei erstellen
    outF = open("./OutFile.txt", "w")
    #prufen ob die Datei sind Richtig eingegeben
    try:
        with open(filename) as f:
            content = f.readlines()  
        if len(content) >= 4 : 
            for line in content:
                lineIndex+=1
                if(lineIndex<=3):
                    Kommentare="{}{}".format(Kommentare,line)
                elif(lineIndex==4):
                    ausgangszustand=line.split(";",7)
                else:
                    Geschäftsvorgänge.append(line.strip())
        else:
            #Fehlerfalle 1
            outF.write(" Error! Zu wenig Zeilen !\n")
    except FileNotFoundError:
        #Fehlerfalle 2
        outF.write(" Error! Datei nicht vorhanden \n")
    
    

    #liefert ein nachricht wenn die Ausgabe Datei sind bereit
    lbl2 = tk.Label(
        window,
        text='Ergebnisse sind in der Ausgabedatei eingeschrieben',
        width=50,
        height=2,
        fg='black',
        bg='white',
        font=('times', 15, ' bold '),
        )
  
    if os.path.isfile(path) :
        
        stücke=["10€", "5€", "2€", "1€", "50 Cent","20 Cent", "10 Cent"]
        n_Stücke=[10 , 5 , 2 , 1 , 0.50 , 0.20 , 0.10]
        n=1
        #hier die programm pruft ob di Anfangsbestand ist richtig eingeschriben
        try :
            Anfangsbestand=[int(n) for n in ausgangszustand]
            for line in Kommentare:
                outF.write(line)
            summ=getTotal(Anfangsbestand)/100
            if summ > 0:
                outF.write("Anfangsbestand: {}€ {}\n".format(summ,Anfangsbestand))
        except ValueError:
            #Fehlerfalle 3
            outF.write(" Error! Falsche Anfangsbestands \n")


        for G in Geschäftsvorgänge:

            preis=float(G.split(";")[0])
            p=preischeck(preis)

            if p!=0 :
                try :
                    index=0
                    total=0
                    #liest die eingabe betrag in ein Array
                    arr=[int(n) for n in G.split(";")[1::]]
                    #convertiert die eingabe betrag von ain Array datei zu ein float datei
                    for item in arr:
                        total+=float(n_Stücke[index])*item
                        index+=1

                    try:
                        
                        ausgangszustand= Anfangsbestand 
                        #berechnen die Ruckgabe
                        rückgabe=Ruckgabe(arr,preis,ausgangszustand)
                        #macht ein plus und verandert die Gesamtbestand
                        ausgangszustand=addToGesamtbestand(arr,ausgangszustand,"+")
                        #macht ein minus und verandert die Gesamtbestand
                        ausgangszustand=addToGesamtbestand(rückgabe,ausgangszustand,"-")
                        #schreibt die Buchung , Preis ,Ruckgabe und Gesamtbestand in die Ausgabedatei "OutFile"
                        outF.write("{}.Buchung : Preis: {}€ /Rückgabe: {}/ Gesamtbestand {} € ({}) \n".format(n,preis,rückgabe,getTotal(ausgangszustand)/100,ausgangszustand))
                        n=n+1
                    except AttributeError:
                        #Sonderfalle 1
                        outF.write("{}. Error! Zuwenig Geld eingeworfen => Rückgabe: {} \n".format(n,arr))
                        n=n+1
                    except ValueError:
                        #Sonderfalle 2
                        outF.write("{}. Error! Wechselgeld kann nicht passend ausgezahlt werden \n".format(n))
                        n=n+1
                except IndexError:
                    #Fehlerfalle 4
                    outF.write("{}. Error! Buchung falsh angegeben \n".format(n))
                    n=n+1

            else :
                #Sonderfalle 3
                outF.write("{}.Buchung : Preis: {} € ist falshe . Bitte, geben sie einen richtigen Fahrpreis ein !\n".format(n,preis))
                n=n+1
        outF.close()
       
    else:
        lbl.place(x=250, y=38)
        lbl.destroy()
    lbl2.place(x=250, y=38)

        

#Directory label in die Window schreiben
lbl = tk.Label(
    window,
    text='Directory :',
    width=20,
    height=2,
    fg='black',
    bg='white',
    font=('times', 15, ' bold '),
    )
lbl.place(x=-5, y=0)

txt = tk.Entry(window, width=70, bg='white', fg='green', font=('times',
               15, ' bold '))
txt.place(x=200, y=10)

# Generate "Schaltflächen anzeigen"

Generate = tk.Button(
    window,
    text='Generate',
    command=GenerateOutputs,
    fg='white',
    bg='green',
    width=15,
    height=2,
    activebackground='blue',
    font=('times', 15, ' bold '),
    )
Generate.place(x=260, y=100)
# Browse "Schaltflächen anzeigen"
Browse = tk.Button(
    window,
    text='Browse',
    command=browseFiles,
    fg='white',
    bg='black',
    width=7,
    height=0,
    activebackground='blue',
    font=('times', 15, ' bold '),
    )
Browse.place(x=910, y=5)

# Quit "Schaltfläche anzeigen"
quitWindow = tk.Button(
    window,
    text='Quit',
    command=window.destroy,
    fg='white',
    bg='red',
    width=15,
    height=2,
    activebackground='Red',
    font=('times', 15, ' bold '),
    )
quitWindow.place(x=560, y=100)

window.mainloop()

