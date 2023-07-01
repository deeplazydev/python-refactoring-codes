#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Funciones útiles para el diseño de acero a flexión según Norma ACI 318-14
"""

def calcular_beta1(resistencia_compresion_concreto):
    """
    Calcular los valores de Beta1 para la distribución rectangular 
    equivalente de esfuerzos en el concreto

    Ver: Tabla 22.2.2.4.3 en sitio web
    """
    if resistencia_compresion_concreto <= 28:
        return 0.85
    elif resistencia_compresion_concreto >= 55:
        return 0.65
    else:
        return 0.85 - 0.05 * (resistencia_compresion_concreto - 28) / 7

def calcular_ro_maximo(factor_gamma, beta1, resistencia_compresion_concreto, resistencia_traccion_acero, deformacion_unitaria):
    """
    Calcula el valor máximo de la relación de refuerzo (roMax) utilizando fc, fy y las constantes gamma, beta1 y eu
    """
    return factor_gamma * beta1 * resistencia_compresion_concreto / resistencia_traccion_acero * deformacion_unitaria / (deformacion_unitaria + 0.005)

def calcular_area_maxima_acero(ro_maximo, ancho_viga, profundidad_efectiva):
    """
    Calcula el área máxima de acero a flexión (AsMax) utilizando roMax, b y d
    """
    return ro_maximo * ancho_viga * profundidad_efectiva

def calcular_momento_maximo_resistente(area_maxima_acero, resistencia_compresion_concreto, resistencia_traccion_acero, factor_gamma, ancho_viga, profundidad_efectiva):
    """
    Calcula el momento máximo resistente (fiMmax) utilizando AsMax, fc, fy, gamma, b y d
    """
    return 0.9 * area_maxima_acero * resistencia_traccion_acero * (profundidad_efectiva - area_maxima_acero * resistencia_traccion_acero / (2 * factor_gamma * resistencia_compresion_concreto * ancho_viga))

def calcular_area_minima_acero(resistencia_compresion_concreto, resistencia_traccion_acero, ancho_viga, profundidad_efectiva):
    """
    Calcula el área mínima de acero a tracción (AsMin) utilizando fórmulas basadas en fc y fy
    """
    area_minima_1 = resistencia_compresion_concreto ** 0.5 / (4 * resistencia_traccion_acero) * ancho_viga * profundidad_efectiva
    area_minima_2 = 1.4 * ancho_viga * profundidad_efectiva / resistencia_traccion_acero
    return max(area_minima_1, area_minima_2)

def calcular_area_acero_traccion(momento_maximo, resistencia_compresion_concreto, resistencia_traccion_acero, factor_gamma, ancho_viga, profundidad_efectiva):
    """
    Calcula el área de acero a tracción (As) utilizando una fórmula específica
    """
    gamma_fc_b = factor_gamma * resistencia_compresion_concreto * ancho_viga
    numerador = 0.9 * profundidad_efectiva - (0.81 * profundidad_efectiva ** 2 - 1.8 * momento_maximo / (gamma_fc_b)) ** 0.5
    denominador = 0.9 * resistencia_traccion_acero / (gamma_fc_b)    
    return numerador / denominador

def calcular_area_acero_adicional(momento_adicional, resistencia_traccion_acero, profundidad_efectiva, profundidad_acero):
    """
    Calcular acero adicional (As2) más allá del máximo momento resistente
    """
    return momento_adicional / (resistencia_traccion_acero * (profundidad_efectiva - profundidad_acero))

def calcular_cuantia_minima_acero_traccion_para_acero_compresion_fluya(area_acero_adicional, resistencia_traccion_acero, factor_gamma, resistencia_compresion_concreto, ancho_viga, profundidad_efectiva, profundidad_acero, beta1, deformacion_unitaria, modulo_elasticidad_acero):
    """
    Calcular cuantía correspondiente a la mínima cantidad de acero a tracción necesaria para que el acero a compresión fluya
    """
    a = factor_gamma * resistencia_compresion_concreto / resistencia_traccion_acero * beta1
    b = deformacion_unitaria / (deformacion_unitaria - resistencia_traccion_acero / modulo_elasticidad_acero)
    c = profundidad_acero / profundidad_efectiva
    d = area_acero_adicional * ancho_viga * profundidad_acero

    return a * b * c + d

def calcular_cuantia_real_acero(area_acero, ancho_viga, profundidad_efectiva):
    """
    Calcular la cuantía real de acero
    """
    return  area_acero/(ancho_viga * profundidad_efectiva)

def calcular_area_acero_revisado(area_acero_traccion, area_acero_compresion, resistencia_compresion_concreto, resistencia_traccion_acero, factor_gamma, beta1, ancho_viga, profundidad_efectiva, deformacion_unitaria, modulo_elasticidad_acero):
    """
    Calcular el área del acero revisado
    """
    a = (area_acero_traccion - area_acero_compresion) * resistencia_traccion_acero / (factor_gamma * resistencia_compresion_concreto * ancho_viga)
    c = a / beta1
    fsp = deformacion_unitaria * modulo_elasticidad_acero * (c - profundidad_efectiva) / c

    return area_acero_compresion * resistencia_traccion_acero / fsp
