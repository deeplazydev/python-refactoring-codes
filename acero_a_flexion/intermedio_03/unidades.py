#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Colección de funciones relacionadas a las unidades físicas
"""

def metro2_a_centimetro2(valor, digitos=2):
    """
    Convertir de metro cuadrado a centímetro cuadrado, redondeando decimales.

    Parámetros:
    valor: magnitud [m2]
    digitos: cantidad de digitos decimales a mantener
    """
    return round(valor*1e4, digitos)

