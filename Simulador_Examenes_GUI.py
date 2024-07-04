#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
from PIL import ImageTk,Image
import random
import time
import datetime


# ## Funcion de contador del examen

# In[5]:


def countdown(parent,s):
 
    # Calculate the total number of seconds
    #total_seconds = h * 3600 + m * 60 + s
    timer = datetime.timedelta(seconds = s)
    timer_text = str(timer)
    print(timer, end="\r")
    time_label = ttk.Label(parent,text=timer_text,background='white',font=('Brass Mono',10),wraplength=1000)
    time_label.grid(row=0,column=2)
    time.sleep(1)
    s -= 1
 
    #print("Bzzzt! The countdown is at zero seconds!")
 


# ## Algoritmo de selección de la base de datos (sin repetir filas)

# In[6]:


df = pd.read_csv('C:/Banco de Preguntas/Datasets/dataset cuestionario examen prueba.csv', sep = ';')
df2 = df.copy()
df2.drop(df2.index[:12],inplace=True)

for i in range(len(df)):
    print(i)
    index = random.randint(0,11)
    entry = df.loc[index]
    print('Dato extraido:',entry['Pregunta'])
    if i == 0:
        print('Se guardo dato')
        df2.loc[i] = entry
    else:
        bandera = 0
        for j in range(len(df2)):
            print('Dato a comparar:',df2['Pregunta'][j])
            if df2['Pregunta'][j] == entry['Pregunta']:
                print('Ya existe en la base de datos')
                bandera = 1
                while bandera == 1:
                    print('Entrando a bucle de correccion')
                    index = random.randint(0,11)
                    entry = df.loc[index]
                    print('Dato extraido:',entry['Pregunta'])
                    for j in range(len(df2)):
                        print('Dato a comparar:',df2['Pregunta'][j])
                        if df2['Pregunta'][j] == entry['Pregunta']:
                            print('Ya existe en la base de datos')
                            break
                        elif df2['Pregunta'][j] != entry['Pregunta'] and j==len(df2)-1:
                            print('Se sale del bucle de correccion...')
                            bandera = 0
                break
        if bandera == 0:
            print('Se guardo dato')
            df2.loc[i] = entry


# In[7]:


df2


# ## Algoritmo para crear Interface de Usuario

# In[8]:


root = tk.Tk()
root.geometry('1400x700')
frame = tk.Frame(root, width=1400, height=700)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

canvas = tk.Canvas(frame,width=1400,height=700)
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
content_frame = ttk.Frame(canvas)
content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

#Select number of questions
number_questions = [4,8,12]
select_questions = ttk.Combobox(content_frame,values=number_questions)
select_questions.grid(row=0,column=0,pady=10)

#Generator of exam
selected = 0
def create():
    global selected
    n_questions = select_questions.get()
    if n_questions == '':
        messagebox.showinfo(message='Select an amount of questions')
    else:
        selected = 1
        messagebox.showinfo(message='Exam was created')
        n_questions = int(n_questions)
        return n_questions

def calcular_puntaje():
    puntaje = 0
    for i in range(len(solucionario)):
        if respuestas_examen[i] == solucionario[i]:
            puntaje += 1

    messagebox.showinfo(title='NOTA',message=f'Tu nota es de: {puntaje}')

generator = ttk.Button(content_frame,text='Calcular nota',command=calcular_puntaje)
generator.grid(row=0,column=1,pady=10)

#List for buttons, images, and answers
A = [None]*12
B = [None]*12
C = [None]*12
D = [None]*12
E = [None]*12
A_respuestas = [None]*12
B_respuestas = [None]*12
C_respuestas = [None]*12
D_respuestas = [None]*12
E_respuestas = [None]*12
respuestas = [[None]*5]*12
solucionario = [None]*12

#Sacamos el solucionario
for solucion in range(len(solucionario)):
    solucionario[solucion] = df2['Respuesta'][solucion]

#Posible answers
for i in range(len(df2)):
    respuestas[i] = [df2['A'][i],df2['B'][i],df2['C'][i],df2['D'][i],df2['E'][i]]

Button_commands = {}
img = [None]*10
respuestas_examen = [None]*12

#Funcion de guardar mis respuestas
def mis_respuestas(text,position,num):
    mi_respuesta = text
    print('Fila:',position)
    print('Salto:',num)
    respuestas_examen[int((position-num)/6)] = mi_respuesta
    print(respuestas_examen)

for respuesta in respuestas:
    texto = ttk.Label(content_frame,text=str(respuestas.index(respuesta)+1)+'. ' +df2['Pregunta'][respuestas.index(respuesta)],background='white',font=('Brass Mono',10),wraplength=1000)
    texto.grid(row=6*respuestas.index(respuesta)+1,column=0,pady=10)
    A = ttk.Button(content_frame,text='A. '+ respuestas[respuestas.index(respuesta)][0],command= lambda idx=6*respuestas.index(respuesta)+2,t=respuestas[respuestas.index(respuesta)][0]: mis_respuestas(t,idx,2))
    A.grid(row=6*respuestas.index(respuesta)+2,column=0,pady=10)
    B = ttk.Button(content_frame,text='B. '+ respuestas[respuestas.index(respuesta)][1],command= lambda idx=6*respuestas.index(respuesta)+3,t=respuestas[respuestas.index(respuesta)][1]: mis_respuestas(t,idx,3))
    B.grid(row=6*respuestas.index(respuesta)+3,column=0,pady=10)
    C = ttk.Button(content_frame,text='C. '+ respuestas[respuestas.index(respuesta)][2],command= lambda idx=6*respuestas.index(respuesta)+4,t=respuestas[respuestas.index(respuesta)][2]: mis_respuestas(t,idx,4))
    C.grid(row=6*respuestas.index(respuesta)+4,column=0,pady=10)
    D = ttk.Button(content_frame,text='D. '+ respuestas[respuestas.index(respuesta)][3],command= lambda idx=6*respuestas.index(respuesta)+5,t=respuestas[respuestas.index(respuesta)][3]: mis_respuestas(t,idx,5))
    D.grid(row=6*respuestas.index(respuesta)+5,column=0,pady=10)
    E = ttk.Button(content_frame,text='E. '+ respuestas[respuestas.index(respuesta)][4],command= lambda idx=6*respuestas.index(respuesta)+6,t=respuestas[respuestas.index(respuesta)][4]: mis_respuestas(t,idx,6))
    E.grid(row=6*respuestas.index(respuesta)+6,column=0,pady=10)
    if df2['Imagen'][respuestas.index(respuesta)] != 'No':
        if img[0] == None:
            imagen = 'C:/Banco de Preguntas/Imagenes/'+df2['Imagen'][respuestas.index(respuesta)] + '.png'
            img[0] = ImageTk.PhotoImage(Image.open(imagen))
            label = ttk.Label(content_frame,image=img[0])
            label.grid(row=6*respuestas.index(respuesta)+2,column=1,rowspan=5)
        else:
            for j in range(len(img)):
                if img[j] == None:
                    imagen = 'C:/Banco de Preguntas/Imagenes/'+df2['Imagen'][respuestas.index(respuesta)] + '.png'
                    img[j] = ImageTk.PhotoImage(Image.open(imagen))
                    label = ttk.Label(content_frame,image=img[j])
                    label.grid(row=6*respuestas.index(respuesta)+2,column=1,rowspan=5)
                    break

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

canvas.create_window((0, 0), window=content_frame, anchor="nw")
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

def _on_mousewheel(event):
   canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)


root.mainloop()


# In[315]: