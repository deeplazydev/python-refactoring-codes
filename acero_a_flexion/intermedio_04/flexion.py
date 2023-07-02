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


from enum import Enum
from norma_ACI318_14_funciones import *
from unidades import metro2_a_centimetro2


class VigaConcretoAceroFlexionResultado(Enum):
    NO_NECESITA_ACERO = 1
    NECESITA_ACERO_FLUYE = 2
    NECESITA_ACERO_NO_FLUYE = 3


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
        return [As, 0.0, AsMin, VigaConcretoAceroFlexionResultado.NO_NECESITA_ACERO]
    else:
        M2 = calcular_momento_adicional(Mu, fiMmax)
        As2 = calcular_area_acero_adicional(M2, fy, d, dp)
        As = AsMax + As2
        Asp = As2

        roY = calcular_cuantia_minima_acero_traccion_para_acero_compresion_fluya(Asp, fy, gamma, fc, b, d, dp, beta1, eu, Es)
        ro = calcular_cuantia_real_acero(As, b, d)

        if ro > roY:
            return [As, Asp, AsMin, VigaConcretoAceroFlexionResultado.NECESITA_ACERO_FLUYE]
        else:
            AsRev = calcular_area_acero_revisado(As, Asp, fc, fy, gamma, beta1, b, dp, eu, Es)
            return [As, Asp, AsRev, VigaConcretoAceroFlexionResultado.NECESITA_ACERO_NO_FLUYE]


def crear_mensajes_al_usuario(acero_traccion, acero_compresion, acero_minimo_traccion, resultado):
    """
    Compaginar los valores resultantes del algoritmo de flexión en textos descriptivos
    """
    return ["Acero a tracción = {:.2f} [cm2]".format(metro2_a_centimetro2(acero_traccion)),
            "Acero a compresión = {:.2f} [cm2]".format(metro2_a_centimetro2(acero_compresion)),
            "Acero mínimo a tracción = {:.2f} [cm2]".format(metro2_a_centimetro2(acero_minimo_traccion)),
            create_mensaje_resultado(resultado)]


def create_mensaje_resultado(valor: VigaConcretoAceroFlexionResultado):
    match valor:
        case VigaConcretoAceroFlexionResultado.NO_NECESITA_ACERO:
            return "La viga no necesita acero a compresión"
        case VigaConcretoAceroFlexionResultado.NECESITA_ACERO_FLUYE:
            return "La viga NECESITA acero a compresión -> As' fluye"
        case VigaConcretoAceroFlexionResultado.NECESITA_ACERO_NO_FLUYE:
            return "La viga NECESITA acero a compresión -> As' no fluye"
        case default:
            return "Resultado no esperado: " + str(valor)


if __name__ == "__main__":
    # Ejecutar un caso de ejemplo
    resultados = calcular_seccion_acero_flexion(0.2, 0.4, 0.05, 20, 500, 120)

    for r in crear_mensajes_al_usuario(*resultados):
        print(r)
    