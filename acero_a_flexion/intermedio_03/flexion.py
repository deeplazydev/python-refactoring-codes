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


from norma_ACI318_14_funciones import *
from unidades import metro2_a_centimetro2


def calcular_seccion_acero_flexion(ancho_viga, altura_viga, recubrimiento_acero, resistencia_compresion_concreto, resistencia_traccion_acero, momento_maximo):
    """Cálculo de la sección de acero a flexión para un diseño estructural de una viga

    Parámetros:
        ancho_viga: ancho de la sección rectangular [m]
        altura_viga: alto de la sección rectangular [m]
        recubrimiento_acero: recubrimiento del acero [m]
        resistencia_compresion_concreto: la resistencia a compresión del concreto [MPa]
        resistencia_traccion_acero: la resistencia a tracción del acero [MPa]
        momento_maximo: momento máximo de diseño [MN-m]

    Resultados:
        str[4]: textos de mensaje al usuario sobre los resultados del cálculo
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

    beta1 = calcular_beta1(fc)

    roMax = calcular_ro_maximo(gamma, beta1, fc, fy, eu)
    AsMax = calcular_area_maxima_acero(roMax, b, d)
    fiMmax = calcular_momento_maximo_resistente(AsMax, fc, fy, gamma, b, d)

    AsMin = calcular_area_minima_acero(fc, fy, b, d)

    if Mu < fiMmax:
        As = calcular_area_acero_traccion(Mu, fc, fy, gamma, b, d)

        texto1 = f"Acero a tracción = { metro2_a_centimetro2(As) } [cm2]"
        texto2 = f"Acero a compresión = 0 [cm2]"
        texto3 = f"Acero mínimo a tracción = { metro2_a_centimetro2(AsMin) } [cm2]"
        texto4 = "La viga no necesita acero a compresión"

    else:
        M2 = calcular_momento_adicional(Mu, fiMmax)
        As2 = calcular_area_acero_adicional(M2, fy, d, dp)
        As = AsMax + As2
        Asp = As2

        roY = calcular_cuantia_minima_acero_traccion_para_acero_compresion_fluya(Asp, fy, gamma, fc, b, d, dp, beta1, eu, Es)
        ro = calcular_cuantia_real_acero(As, b, d)

        if ro > roY:
            texto1 = f"Acero a tracción = { metro2_a_centimetro2(As) } [cm2]"
            texto2 = f"Acero a compresión = { metro2_a_centimetro2(Asp) } [cm2]"
            texto3 = f"Acero mínimo a tracción = { metro2_a_centimetro2(AsMin) } [cm2]"
            texto4 = "La viga NECESITA acero a compresión. As' fluye"
        else:
            AsRev = calcular_area_acero_revisado(As, Asp, fc, fy, gamma, beta1, b, dp, eu, Es)

            texto1 = f"Acero a tracción = { metro2_a_centimetro2(As) } [cm2]"
            texto2 = f"Acero a compresión = { metro2_a_centimetro2(Asp) } [cm2]"
            texto3 = f"Acero mínimo a tracción = { metro2_a_centimetro2(AsRev) } [cm2]"
            texto4 = "La viga NECESITA acero a compresión. As' no fluye"

    # Resultados
    return [texto1, texto2, texto3, texto4]


if __name__ == "__main__":
    # Ejecutar un caso de ejemplo
    resultados = calcular_seccion_acero_flexion(0.2, 0.4, 0.05, 20, 500, 120)

    for r in resultados:
        print(r)
    