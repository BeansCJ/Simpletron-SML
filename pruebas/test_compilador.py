import os
import subprocess
import sys
import tempfile
import unittest

carpeta_proyecto = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(carpeta_proyecto, "src", "compilador"))

from compilador import Compilador


class PruebasCompilador(unittest.TestCase):
    def ejecutar_simple(self, texto, entrada=""):
        palabras = Compilador().compilar(texto)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, suffix=".sml") as archivo:
            for palabra in palabras:
                archivo.write(f"{palabra}\n")
            ruta = archivo.name

        try:
            simulador = os.path.join(carpeta_proyecto, "src", "simpletron", "simpletron.py")
            resultado = subprocess.run(
                [sys.executable, "-B", simulador, ruta],
                input=entrada,
                capture_output=True,
                text=True,
            )
            return resultado.stdout
        finally:
            os.remove(ruta)

    def test_let_con_precedencia(self):
        texto = "10 let a = 12 + 3 * 4\n20 print a\n30 end"
        salida = self.ejecutar_simple(texto)
        self.assertIn("\n24\n", salida)

    def test_input_y_suma(self):
        with open(os.path.join(carpeta_proyecto, "programas", "simple", "suma.simple"), encoding="utf-8") as archivo:
            texto = archivo.read()
        salida = self.ejecutar_simple(texto, "8\n9\n")
        self.assertIn("Ingrese un entero: Ingrese un entero: 17\n*** Ejecucion detenida", salida)

    def test_if_con_referencia_hacia_adelante(self):
        texto = "10 input a\n20 if a == 7 goto 40\n30 print 0\n35 goto 50\n40 print a\n50 end"
        salida = self.ejecutar_simple(texto, "7\n")
        self.assertIn("Ingrese un entero: 7\n*** Ejecucion detenida", salida)

    def test_operadores_relacionales(self):
        casos = [
            ("<", 7, 8, True),
            ("<=", 8, 8, True),
            (">", 9, 8, True),
            (">=", 8, 8, True),
            ("==", 8, 8, True),
            ("!=", 7, 8, True),
            ("<", 9, 8, False),
            (">", 7, 8, False),
            ("==", 7, 8, False),
            ("!=", 8, 8, False),
        ]

        for operador, entrada, limite, verdadero in casos:
            with self.subTest(operador=operador, entrada=entrada, limite=limite):
                texto = (
                    f"10 input a\n20 if a {operador} {limite} goto 40\n"
                    "30 print 0\n35 goto 50\n40 print 1\n50 end"
                )
                salida = self.ejecutar_simple(texto, f"{entrada}\n")
                esperado = 1 if verdadero else 0
                self.assertIn(f"Ingrese un entero: {esperado}\n*** Ejecucion detenida", salida)

    def test_programa_mayor(self):
        ruta = os.path.join(carpeta_proyecto, "programas", "simple", "mayor.simple")
        with open(ruta, encoding="utf-8") as archivo:
            salida = self.ejecutar_simple(archivo.read(), "7\n5\n")
        self.assertIn("Ingrese un entero: Ingrese un entero: 7\n*** Ejecucion detenida", salida)

    def test_programa_factorial(self):
        ruta = os.path.join(carpeta_proyecto, "programas", "simple", "factorial.simple")
        with open(ruta, encoding="utf-8") as archivo:
            salida = self.ejecutar_simple(archivo.read(), "5\n")
        self.assertIn("Ingrese un entero: 120\n*** Ejecucion detenida", salida)

    def test_lineas_fuera_de_orden(self):
        texto = "20 end\n10 end"
        with self.assertRaises(ValueError):
            Compilador().compilar(texto)

    def test_destino_inexistente(self):
        texto = "10 goto 99\n20 end"
        with self.assertRaises(ValueError):
            Compilador().compilar(texto)


if __name__ == "__main__":
    unittest.main()
