import tkinter as tk

def calculoFlexion():
    #INGRESO DE DATOS
    b = float(entry1.get())
    h = float(entry2.get())
    recub = float(entry3.get())
    fc = float(entry4.get())
    fy = float(entry5.get())
    Mu = float(entry6.get())

    #CÁLCULO DE SECCIÓN DE ACERO A FLEXIÓN
    Mu = Mu/1000
    d = h-recub
    dp = recub
    gamma = 0.85
    eu = 0.003
    Es = 200e3

    if fc<=28:
        beta1 = 0.85
    elif fc>=55:
        beta1 = 0.65
    else:
        beta1 = 0.85 - 0.05*(fc-28)/7

    roMax = gamma*beta1*fc/fy*eu/(eu+0.005)
    AsMax = roMax*b*d
    fiMmax = 0.9*AsMax*fy*(d-AsMax*fy/(2*gamma*fc*b))

    AsMin1 = fc**0.5/(4*fy)*b*d
    AsMin2 = 1.4*b*d/fy

    AsMin = max(AsMin1, AsMin2)

    if Mu<fiMmax:
        numerador = 0.9*d-(0.81*d**2-1.8*Mu/(gamma*fc*b))**0.5
        denominador = 0.9*fy/(gamma*fc*b)
        As = numerador/denominador

        texto1 = "Acero a tracción = " + str(round(As*1e4,2)) + "[cm2]"
        texto2 = "Acero a compresión = 0[cm2]"
        texto3 = "Acero mínimo a tracción = " + str(round(AsMin*1e4,2)) + "[cm2]"
        texto4 = "La viga no necesita acero a compresión"

    else:
        M2 = (Mu - fiMmax)/0.9
        As2 = M2/(fy*(d-dp))
        As = AsMax + As2
        Asp = As2

        roY = gamma*fc/fy*beta1*eu/(eu-fy/Es)*dp/d+Asp*(b*d)
        ro = As/(b*d)
        if ro>roY:
            texto1 = "Acero a tracción = " + str(round(As*1e4,2)) + "[cm2]"
            texto2 = "Acero a compresión = " + str(round(Asp*1e4,2)) + "[cm2]"
            texto3 = "Acero mínimo a tracción = " + str(round(AsMin*1e4,2)) + "[cm2]"
            texto4 = "La viga NECESITA acero a compresión. As' fluye"
        else:
            a = (As-Asp)*fy/(gamma*fc*b)
            c = a/beta1
            fsp = eu*Es*(c-dp)/c
            AsRev = Asp*fy/fsp
            texto1 = "Acero a tracción = " + str(round(As*1e4,2)) + "[cm2]"
            texto2 = "Acero a compresión = " + str(round(Asp*1e4,2)) + "[cm2]"
            texto3 = "Acero mínimo a tracción = " + str(round(AsRev*1e4,2)) + "[cm2]"
            texto4 = "La viga NECESITA acero a compresión. As' no fluye"

    etiqueta_resultado1.config(text=texto1)
    etiqueta_resultado2.config(text=texto2)
    etiqueta_resultado3.config(text=texto3)
    etiqueta_resultado4.config(text=texto4)


import tkinter as tk

# Crear la ventana
ventana = tk.Tk()
ventana.title("Acero a Flexión")

# Crear las etiquetas y los campos de entrada
label1 = tk.Label(ventana, text="b [m]:") 
label1.pack()
entry1 = tk.Entry(ventana)
entry1.pack()

label2 = tk.Label(ventana, text="h [m]:") 
label2.pack()
entry2 = tk.Entry(ventana)
entry2.pack()

label3 = tk.Label(ventana, text="recub. al eje[m]:") 
label3.pack()
entry3 = tk.Entry(ventana)
entry3.pack()

label4 = tk.Label(ventana, text="fp' [MPa]:") 
label4.pack()
entry4 = tk.Entry(ventana)
entry4.pack()

label5 = tk.Label(ventana, text="fy [MPa]:") 
label5.pack()
entry5 = tk.Entry(ventana)
entry5.pack()

label6 = tk.Label(ventana, text="Mu [KN-m]:") 
label6.pack()
entry6 = tk.Entry(ventana)
entry6.pack()

# Crear el botón para calcular la suma
boton_sumar = tk.Button(ventana, text="Calcular Acero", command=calculoFlexion)
boton_sumar.pack()

# Crear la etiqueta para mostrar el resultado
etiqueta_resultado1 = tk.Label(ventana, text="")
etiqueta_resultado1.pack()
etiqueta_resultado2 = tk.Label(ventana, text="")
etiqueta_resultado2.pack()
etiqueta_resultado3 = tk.Label(ventana, text="")
etiqueta_resultado3.pack()
etiqueta_resultado4 = tk.Label(ventana, text="")
etiqueta_resultado4.pack()

# Ejecutar la ventana
ventana.mainloop()
