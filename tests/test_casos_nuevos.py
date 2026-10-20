"""Pruebas nuevas: casos normales, fronterizos, invalidos y asociatividad."""

import pytest

from mini_interprete.cli import interpretar
from mini_interprete.errores import ErrorDeEvaluacion, ErrorDeSintaxis


def test_multiplicacion_antes_de_la_suma_a_la_izquierda():
    assert interpretar("2 * 3 + 4") == 10


def test_parentesis_anidados():
    assert interpretar("((1 + 2) * (3 + 4))") == 21


def test_ceros_a_la_izquierda():
    assert interpretar("007") == 7


def test_division_es_real():
    assert interpretar("10 / 4") == 2.5


def test_division_exacta_regresa_flotante():
    resultado = interpretar("10 / 2")
    assert resultado == 5.0
    assert isinstance(resultado, float)


def test_espacios_en_cualquier_cantidad():
    assert interpretar("   3     +   4   ") == 7


def test_division_entre_cero():
    with pytest.raises(ErrorDeEvaluacion):
        interpretar("10 / 0")


def test_division_entre_cero_disfrazada():
    with pytest.raises(ErrorDeEvaluacion):
        interpretar("1 / (2 - 2)")


def test_resta_encadenada():
    assert interpretar("10 - 3 - 2") == 5


def test_division_encadenada():
    assert interpretar("8 / 4 / 2") == 1.0


def test_multiplicacion_y_division_encadenadas():
    assert interpretar("12 / 3 * 2") == 8.0


def test_operador_sin_operando_derecho():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("3 +")


def test_parentesis_sin_cerrar():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("(3 + 4")


def test_parentesis_de_mas_al_final():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("3 + 4)")


def test_dos_numeros_seguidos():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("3 4")


def test_entrada_vacia():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("")


def test_menos_unario_no_se_soporta():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("-3")


def test_caracter_desconocido():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("3 $ 4")


def test_el_error_indica_la_posicion():
    with pytest.raises(ErrorDeSintaxis) as info:
        interpretar("3 + * 4")
    assert info.value.posicion == 4
