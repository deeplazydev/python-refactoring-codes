#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Diseño de acero a flexión - Norma ACI 318-14

Interfaz gráfica para el cálculo de la sección de acero a flexión 
para un diseño estructural de una viga de concreto.

Este código fue extraído de lo expuesto por Marcelo Pardo (marcelopardo.com)
con el objetivo de mostrar cómo a través de un proceso de refactoring
puede mejorarse la calidad del código.
"""

__author__ = "Deep Lazy Dev"
__credits__ = ["Marcelo Pardo"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Deep Lazy Dev"
__email__ = "deeplazydev@gmail.com"
__status__ = "Development"


import tkinter as tk
from flexion import calcular_seccion_acero_flexion, crear_mensajes_al_usuario


def calculoFlexion():
    """
    Funcion que toma los datos ingresados, llama a la función que hace los cálculos y actualiza la interfaz con los resultados.
    """
    resultados = calcular_seccion_acero_flexion(float(entry1.get()),
                                                float(entry2.get()),
                                                float(entry3.get()),
                                                float(entry4.get()),
                                                float(entry5.get()),
                                                float(entry6.get()))
    
    textos = crear_mensajes_al_usuario(*resultados)

    # Actualizar la interfaz gráfica
    for i in range(len(textos)):
        etiqueta_resultados[i].config(text=textos[i])


def tk_crear_campo_entrada(parent, etiqueta):
    """
    Crear Label/Entry para los datos de entrada del algoritmo
    """
    label = tk.Label(parent, text=etiqueta) 
    label.pack()
    entry = tk.Entry(parent)
    entry.pack()

    return entry

def tk_crear_campo_resultado(parent, texto=""):
    """
    Crear Label para alojar un resultado
    """
    label = tk.Label(parent, text=texto) 
    label.pack()

    return label
    

# Crear la ventana
ventana = tk.Tk()
ventana.title("Acero a Flexión")
ventana.geometry("300x400")

# Crear las etiquetas y los campos de entrada
entry1 = tk_crear_campo_entrada(ventana, "b [m]:")
entry2 = tk_crear_campo_entrada(ventana, "h [m]:")
entry3 = tk_crear_campo_entrada(ventana, "recub. al eje[m]:")
entry4 = tk_crear_campo_entrada(ventana, "fp' [MPa]:")
entry5 = tk_crear_campo_entrada(ventana, "fy [MPa]:")
entry6 = tk_crear_campo_entrada(ventana, "Mu [KN-m]:")

# Crear el botón para calcular
boton_sumar = tk.Button(ventana, text="Calcular Acero", command=calculoFlexion)
boton_sumar.pack()

# Crear las 4 etiqueta para mostrar el resultado
etiqueta_resultados = [tk_crear_campo_resultado(ventana) for i in range(4)]

# Ejecutar la ventana
ventana.mainloop()
