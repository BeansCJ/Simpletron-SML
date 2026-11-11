import os
import sys
import unittest

carpeta_fuente = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "expresiones"))
sys.path.insert(0, carpeta_fuente)

from expresiones import convertir_a_postfija, evaluar_postfija


class PruebasExpresiones(unittest.TestCase):
    def test_precedencia(self):
        self.assertEqual(convertir_a_postfija("3 + 4 * 2"), "3 4 2 * +")

    def test_parentesis(self):
        self.assertEqual(convertir_a_postfija("(3 + 4) * 2"), "3 4 + 2 *")

    def test_potencia_asociativa_a_derecha(self):
        self.assertEqual(convertir_a_postfija("2 ^ 3 ^ 2"), "2 3 2 ^ ^")

    def test_evaluar_varios_digitos(self):
        postfija = convertir_a_postfija("12 + 3 * 4")
        self.assertEqual(evaluar_postfija(postfija), 24)

    def test_evaluar_variables(self):
        postfija = convertir_a_postfija("a + b * 2")
        self.assertEqual(evaluar_postfija(postfija, {"a": 3, "b": 4}), 11)

    def test_negativo_unario(self):
        postfija = convertir_a_postfija("-2 ^ 2")
        self.assertEqual(evaluar_postfija(postfija), -4)

    def test_division_entre_cero(self):
        postfija = convertir_a_postfija("5 / 0")
        with self.assertRaises(ValueError):
            evaluar_postfija(postfija)


if __name__ == "__main__":
    unittest.main()
