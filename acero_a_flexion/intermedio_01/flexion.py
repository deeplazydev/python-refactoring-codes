#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Diseño de acero a flexión - Norma ACI 318-14

Este código fue extraído de lo expuesto por Marcelo Pardo (marcelopardo.com)
con el objetivo de mostrar cómo a través de un proceso de refactoring
puede mejorarse la calidad del código.

Para más información consulte el sitio: https://github.com/deeplazydev/python-refactoring-codes
"""

__author__ = "Deep Lazy Dev"
__credits__ = ["Marcelo Pardo"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Deep Lazy Dev"
__email__ = "deeplazydev@gmail.com"
__status__ = "Development"

def calcular_seccion_acero_flexion(ancho_viga, altura_viga, recubrimiento_acero, resistencia_compresion_concreto, resistencia_traccion_acero, momento_maximo):
    """Cálculo de la sección de acero a flexión para un diseño estructural de una viga

    Parámetros:
        ancho_viga: ancho de la sección rectangular [m]
        altura_viga: alto de la sección rectangular [m]
        recubrimiento_acero: recubrimiento del acero [m]
        resistencia_compresion_concreto: la resistencia a compresión del concreto [MPa]
        resistencia_traccion_acero: la resistencia a tracción del acero [MPa]
        momento_maximo: momento máximo de diseño [MN-m]
    """

    # Datos de entrada (dejaré los nombres de variable originales)
    b = ancho_viga
    h = altura_viga
    recub = recubrimiento_acero
    fc = resistencia_compresion_concreto
    fy = resistencia_traccion_acero
    Mu = momento_maximo

    # Cálculo
    Mu = Mu/1000
    d = h - recub
    dp = recub
    gamma = 0.85
    eu = 0.003
    Es = 200e3

    if fc <= 28:
        beta1 = 0.85
    elif fc >= 55:
        beta1 = 0.65
    else:
        beta1 = 0.85 - 0.05*(fc - 28)/7

    roMax = gamma*beta1*fc/fy*eu/(eu + 0.005)
    AsMax = roMax*b*d
    fiMmax = 0.9*AsMax*fy*(d - AsMax*fy/(2*gamma*fc*b))

    AsMin1 = fc**0.5/(4*fy)*b*d
    AsMin2 = 1.4*b*d/fy

    AsMin = max(AsMin1, AsMin2)

    if Mu < fiMmax:
        numerador = 0.9*d - (0.81*d**2 - 1.8*Mu/(gamma*fc*b))**0.5
        denominador = 0.9*fy/(gamma*fc*b)
        As = numerador/denominador

        texto1 = "Acero a tracción = " + str(round(As*1e4,2)) + "[cm2]"
        texto2 = "Acero a compresión = 0[cm2]"
        texto3 = "Acero mínimo a tracción = " + str(round(AsMin*1e4,2)) + "[cm2]"
        texto4 = "La viga no necesita acero a compresión"

    else:
        M2 = (Mu - fiMmax)/0.9
        As2 = M2/(fy*(d - dp))
        As = AsMax + As2
        Asp = As2

        roY = gamma*fc/fy*beta1*eu/(eu - fy/Es)*dp/d + Asp*(b*d)
        ro = As/(b*d)
        if ro > roY:
            texto1 = "Acero a tracción = " + str(round(As*1e4,2)) + "[cm2]"
            texto2 = "Acero a compresión = " + str(round(Asp*1e4,2)) + "[cm2]"
            texto3 = "Acero mínimo a tracción = " + str(round(AsMin*1e4,2)) + "[cm2]"
            texto4 = "La viga NECESITA acero a compresión. As' fluye"
        else:
            a = (As-Asp)*fy/(gamma*fc*b)
            c = a/beta1
            fsp = eu*Es*(c - dp)/c
            AsRev = Asp*fy/fsp
            texto1 = "Acero a tracción = " + str(round(As*1e4,2)) + "[cm2]"
            texto2 = "Acero a compresión = " + str(round(Asp*1e4,2)) + "[cm2]"
            texto3 = "Acero mínimo a tracción = " + str(round(AsRev*1e4,2)) + "[cm2]"
            texto4 = "La viga NECESITA acero a compresión. As' no fluye"

    # Resultados
    print(texto1)
    print(texto2)
    print(texto3)
    print(texto4)


if __name__ == "__main__":
    # Ejecutar un caso de ejemplo
    calcular_seccion_acero_flexion(0.2, 0.4, 0.05, 20, 500, 120)
    