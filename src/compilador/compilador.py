import os
import re
import sys

carpeta_expresiones = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "expresiones"))
sys.path.insert(0, carpeta_expresiones)

from expresiones import convertir_a_postfija


CODIGOS = {
    "input": 10,
    "print": 11,
    "load": 20,
    "store": 21,
    "+": 30,
    "-": 31,
    "/": 32,
    "*": 33,
    "^": 35,
    "branch": 40,
    "branchneg": 41,
    "branchzero": 42,
    "halt": 43,
}


class Compilador:
    def __init__(self):
        self.instrucciones = []
        self.datos = {}
        self.lineas_codigo = {}
        self.numero_temporal = 0
        self.tabla_simbolos = {"lineas": {}, "variables": set(), "constantes": set()}

    def _analizar_fuente(self, texto):
        instrucciones = []
        numero_anterior = -1

        for numero_fisico, texto_linea in enumerate(texto.splitlines(), start=1):
            texto_linea = texto_linea.strip()
            if texto_linea == "":
                continue

            partes = texto_linea.split(None, 1)
            if len(partes) != 2 or not partes[0].isdigit():
                raise ValueError(f"Linea {numero_fisico}: se esperaba un numero de linea y un comando")

            numero = int(partes[0])
            comando = partes[1].strip()
            if numero <= numero_anterior:
                raise ValueError(f"Linea {numero_fisico}: los numeros de linea deben ir en orden ascendente")
            numero_anterior = numero
            self.tabla_simbolos["lineas"][numero] = None

            if comando.startswith("rem"):
                instrucciones.append({"linea": numero, "tipo": "rem"})
            elif comando.startswith("input "):
                variable = comando[6:].strip()
                self._validar_variable(variable, numero)
                self.tabla_simbolos["variables"].add(variable)
                instrucciones.append({"linea": numero, "tipo": "input", "variable": variable})
            elif comando.startswith("print "):
                expresion = comando[6:].strip()
                instrucciones.append({"linea": numero, "tipo": "print", "expresion": expresion})
                self._registrar_expresion(expresion, numero)
            elif comando.startswith("let "):
                coincidencia = re.fullmatch(r"let\s+([a-z])\s*=\s*(.+)", comando)
                if not coincidencia:
                    raise ValueError(f"Linea {numero}: usa el formato let a = expresion")
                variable = coincidencia.group(1)
                expresion = coincidencia.group(2)
                self.tabla_simbolos["variables"].add(variable)
                instrucciones.append({"linea": numero, "tipo": "let", "variable": variable, "expresion": expresion})
                self._registrar_expresion(expresion, numero)
            elif comando.startswith("goto "):
                destino = comando[5:].strip()
                if not destino.isdigit():
                    raise ValueError(f"Linea {numero}: goto necesita un numero de linea")
                instrucciones.append({"linea": numero, "tipo": "goto", "destino": int(destino)})
            elif comando.startswith("if "):
                coincidencia = re.fullmatch(r"if\s+(.+?)\s*(<=|>=|==|!=|<|>)\s*(.+?)\s+goto\s+(\d+)", comando)
                if not coincidencia:
                    raise ValueError(f"Linea {numero}: usa if expresion operador expresion goto linea")
                izquierda, operador, derecha, destino = coincidencia.groups()
                self._registrar_expresion(izquierda, numero)
                self._registrar_expresion(derecha, numero)
                instrucciones.append({
                    "linea": numero,
                    "tipo": "if",
                    "izquierda": izquierda,
                    "operador": operador,
                    "derecha": derecha,
                    "destino": int(destino),
                })
            elif comando == "end":
                instrucciones.append({"linea": numero, "tipo": "end"})
            else:
                raise ValueError(f"Linea {numero}: comando no reconocido")

        if not instrucciones:
            raise ValueError("El programa Simple esta vacio")

        return instrucciones

    def _validar_variable(self, variable, numero_linea):
        if not re.fullmatch(r"[a-z]", variable):
            raise ValueError(f"Linea {numero_linea}: las variables deben ser una letra minuscula")

    def _registrar_expresion(self, expresion, numero_linea):
        try:
            postfija = convertir_a_postfija(expresion)
        except ValueError as error:
            raise ValueError(f"Linea {numero_linea}: {error}")

        for token in postfija.split():
            if token.isdigit():
                valor = int(token)
                if valor < -9999 or valor > 9999:
                    raise ValueError(f"Linea {numero_linea}: constante fuera de rango")
                self.tabla_simbolos["constantes"].add(valor)
            elif len(token) == 1 and token.isalpha():
                self.tabla_simbolos["variables"].add(token)

    def _agregar_dato(self, tipo, valor, inicial=0):
        nombre = f"{tipo}:{valor}"
        if nombre not in self.datos:
            self.datos[nombre] = inicial
        return nombre

    def _nuevo_temporal(self):
        nombre = self._agregar_dato("temporal", self.numero_temporal)
        self.numero_temporal += 1
        return nombre

    def _emitir(self, codigo, operando=0):
        self.instrucciones.append([codigo, operando])

    def _compilar_expresion(self, expresion):
        postfija = convertir_a_postfija(expresion).split()
        pila = []

        for token in postfija:
            if token.isdigit():
                dato = self._agregar_dato("constante", token, int(token))
                temporal = self._nuevo_temporal()
                self._emitir(CODIGOS["load"], dato)
                self._emitir(CODIGOS["store"], temporal)
                pila.append(temporal)
            elif len(token) == 1 and token.isalpha():
                dato = self._agregar_dato("variable", token)
                temporal = self._nuevo_temporal()
                self._emitir(CODIGOS["load"], dato)
                self._emitir(CODIGOS["store"], temporal)
                pila.append(temporal)
            elif token == "NEG":
                if len(pila) < 1:
                    raise ValueError("Falta un operando en la expresion")
                dato = pila.pop()
                menos_uno = self._agregar_dato("constante", "-1", -1)
                self._emitir(CODIGOS["load"], dato)
                self._emitir(CODIGOS["*"], menos_uno)
                self._emitir(CODIGOS["store"], dato)
                pila.append(dato)
            else:
                if len(pila) < 2:
                    raise ValueError("Faltan operandos en la expresion")
                derecha = pila.pop()
                izquierda = pila.pop()
                self._emitir(CODIGOS["load"], izquierda)
                self._emitir(CODIGOS[token], derecha)
                self._emitir(CODIGOS["store"], izquierda)
                pila.append(izquierda)

        if len(pila) != 1:
            raise ValueError("La expresion no esta completa")
        return pila.pop()

    def _compilar_condicion(self, instruccion):
        izquierda = self._compilar_expresion(instruccion["izquierda"])
        derecha = self._compilar_expresion(instruccion["derecha"])
        operador = instruccion["operador"]
        destino = ("linea", instruccion["destino"])

        if operador in [">", ">="]:
            izquierda, derecha = derecha, izquierda

        self._emitir(CODIGOS["load"], izquierda)
        self._emitir(CODIGOS["-"], derecha)

        if operador == "<" or operador == ">":
            self._emitir(CODIGOS["branchneg"], destino)
        elif operador == "<=" or operador == ">=":
            self._emitir(CODIGOS["branchneg"], destino)
            self._emitir(CODIGOS["branchzero"], destino)
        elif operador == "==":
            self._emitir(CODIGOS["branchzero"], destino)
        elif operador == "!=":
            self._emitir(CODIGOS["branchneg"], destino)
            direccion_siguiente = len(self.instrucciones) + 2
            self._emitir(CODIGOS["branchzero"], ("direccion", direccion_siguiente))
            self._emitir(CODIGOS["branch"], destino)

    def _segunda_pasada(self, instrucciones_fuente):
        for instruccion in instrucciones_fuente:
            numero = instruccion["linea"]
            self.lineas_codigo[numero] = len(self.instrucciones)
            tipo = instruccion["tipo"]

            if tipo == "rem":
                continue
            if tipo == "input":
                variable = self._agregar_dato("variable", instruccion["variable"])
                self._emitir(CODIGOS["input"], variable)
            elif tipo == "print":
                resultado = self._compilar_expresion(instruccion["expresion"])
                self._emitir(CODIGOS["print"], resultado)
            elif tipo == "let":
                resultado = self._compilar_expresion(instruccion["expresion"])
                variable = self._agregar_dato("variable", instruccion["variable"])
                self._emitir(CODIGOS["load"], resultado)
                self._emitir(CODIGOS["store"], variable)
            elif tipo == "goto":
                self._emitir(CODIGOS["branch"], ("linea", instruccion["destino"]))
            elif tipo == "if":
                self._compilar_condicion(instruccion)
            elif tipo == "end":
                self._emitir(CODIGOS["halt"])

        if instrucciones_fuente[-1]["tipo"] != "end":
            self._emitir(CODIGOS["halt"])

    def compilar(self, texto):
        self.instrucciones = []
        self.datos = {}
        self.lineas_codigo = {}
        self.numero_temporal = 0
        self.tabla_simbolos = {"lineas": {}, "variables": set(), "constantes": set()}

        instrucciones_fuente = self._analizar_fuente(texto)
        self._segunda_pasada(instrucciones_fuente)

        inicio_datos = len(self.instrucciones)
        direcciones_datos = {}
        for posicion, nombre in enumerate(self.datos):
            direcciones_datos[nombre] = inicio_datos + posicion

        if inicio_datos + len(self.datos) > 100:
            raise ValueError("El programa y sus datos exceden las 100 posiciones de memoria")

        for numero in self.lineas_codigo:
            self.tabla_simbolos["lineas"][numero] = self.lineas_codigo[numero]

        palabras = []
        for codigo, operando in self.instrucciones:
            if isinstance(operando, tuple) and operando[0] == "linea":
                if operando[1] not in self.lineas_codigo:
                    raise ValueError(f"La linea de destino {operando[1]} no existe")
                direccion = self.lineas_codigo[operando[1]]
            elif isinstance(operando, tuple) and operando[0] == "direccion":
                direccion = operando[1]
            elif isinstance(operando, str):
                direccion = direcciones_datos[operando]
            else:
                direccion = operando
            palabras.append(codigo * 100 + direccion)

        for nombre in self.datos:
            palabras.append(self.datos[nombre])

        return palabras


def compilar_archivo(ruta_entrada, ruta_salida):
    with open(ruta_entrada, "r", encoding="utf-8") as archivo:
        texto = archivo.read()

    compilador = Compilador()
    palabras = compilador.compilar(texto)
    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        for palabra in palabras:
            archivo.write(f"{palabra}\n")
    return compilador.tabla_simbolos


def main():
    if len(sys.argv) < 3:
        print("Uso: python compilador.py programa.simple programa.sml")
        return

    try:
        tabla = compilar_archivo(sys.argv[1], sys.argv[2])
        print(f"Programa compilado en: {sys.argv[2]}")
        print("Tabla de simbolos:")
        print(f"Lineas: {tabla['lineas']}")
        print(f"Variables: {sorted(tabla['variables'])}")
        print(f"Constantes: {sorted(tabla['constantes'])}")
    except (OSError, ValueError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
