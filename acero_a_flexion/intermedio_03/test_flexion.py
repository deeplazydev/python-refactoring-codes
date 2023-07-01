""" Pruebas unitarias para el diseño de acero a flexión en vigas

Los casos de prueba fueron extraídos de las comprobaciones que hizo
el ingeniero Marcelo Pardo mientras probaba la interfaz gráfica.

Nota: más casos de prueba pueden ser agregados, pero como requiere
el estudio del algoritmo y eso escapa al propósito de este refactoring,
se lo dejo al interesado.
"""

from flexion import calcular_seccion_acero_flexion

def test_calcular_flexion_no_necesita_acero() -> None:
    res = calcular_seccion_acero_flexion(0.2, 0.4, 0.05, 20, 500, 70)

    assert res[0] == "Acero a tracción = 4.96 [cm2]"
    assert res[1] == "Acero a compresión = 0 [cm2]"
    assert res[2] == "Acero mínimo a tracción = 1.96 [cm2]"
    assert res[3] == "La viga no necesita acero a compresión"

def test_calcular_flexion_necesita_acero_no_fluye() -> None:
    res = calcular_seccion_acero_flexion(0.2, 0.4, 0.05, 20, 500, 120)

    assert res[0] == "Acero a tracción = 9.04 [cm2]"
    assert res[1] == "Acero a compresión = 1.45 [cm2]"
    assert res[2] == "Acero mínimo a tracción = 1.95 [cm2]"
    assert res[3] == "La viga NECESITA acero a compresión. As' no fluye"

def test_calcular_flexion_necesita_acero_fluye() -> None:
    res = calcular_seccion_acero_flexion(0.3, 0.6, 0.05, 30, 410, 600)

    assert res[0] == "Acero a tracción = 34.85 [cm2]"
    assert res[1] == "Acero a compresión = 2.69 [cm2]"
    assert res[2] == "Acero mínimo a tracción = 5.63 [cm2]"
    assert res[3] == "La viga NECESITA acero a compresión. As' fluye"

