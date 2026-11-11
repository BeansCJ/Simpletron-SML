# Carlo Emilio Caballero Robles - 3515208

"""
Simulador de simpletron
Proyecto de Simulador de una computadora virtual Simpletron (SML).
"""

import sys

TAM_MEMORIA = 100
MIN_VALOR = -9999
MAX_VALOR = 9999

# Codigos de operacion SML
LEER = 10
ESCRIBIR = 11
SALTO_LINEA = 12
ESCRIBIR_CADENA = 13
LEER_CADENA = 14
CARGAR = 20
ALMACENAR = 21
SUMAR = 30
RESTAR = 31
DIVIDIR = 32
MULTIPLICAR = 33
MODULO = 34
POTENCIA = 35
BIFURCAR = 40
BIFURCAR_NEGATIVO = 41
BIFURCAR_CERO = 42
DETENER = 43


class Simpletron:
    def __init__(self):
        self.memoria = [0] * TAM_MEMORIA
        self.accumulator = 0
        self.instructionCounter = 0
        self.instructionRegister = 0
        self.operationCode = 0
        self.operand = 0
        self.en_ejecucion = True

    def cargar_programa(self):
#SOLICITA AL USUARIO LAS INTRUCIONES Y DATOSS

        print("*** Bienvenido al simulador Simpletron ***")
        print("*** Ingrese su programa. Cada instruccion o dato en SML ***")
        print("*** se introduce en la ubicacion de memoria adecuada.   ***")
        print("*** Escriba 9999 para detener la entrada.               ***\n")

        direccion = 0
        while direccion < TAM_MEMORIA:
            entrada = input(f"{direccion:02d} ? ")
            try:
                valor = int(entrada)
            except ValueError:
                print("*** Entrada invalida, intente de nuevo ***")
                continue

            if valor == 9999:
                break

            if MIN_VALOR <= valor <= MAX_VALOR - 1:
                self.memoria[direccion] = valor
                direccion += 1
            else:
                print("*** Error: la instruccion debe estar entre -9999 y +9998 ***")

    def cargar_archivo(self, ruta):
        try:
            archivo = open(ruta, "r", encoding="utf-8")
            lineas = archivo.readlines()
            archivo.close()
        except FileNotFoundError:
            print(f"*** Error: el archivo '{ruta}' no existe ***")
            return False

        direccion = 0
        numero_linea = 0
        for linea in lineas:
            numero_linea += 1
            texto = linea.split(";")[0].strip()

            if texto == "":
                continue

            try:
                valor = int(texto)
            except ValueError:
                print(f"*** Error en la linea {numero_linea}: '{texto}' no es un valor valido ***")
                return False

            if valor < MIN_VALOR or valor > MAX_VALOR:
                print(f"*** Error en la linea {numero_linea}: valor fuera de rango ***")
                return False

            if direccion >= TAM_MEMORIA:
                print("*** Error: el programa excede la memoria ***")
                return False

            self.memoria[direccion] = valor
            direccion += 1

        return True

    def volcado_memoria(self):
        """Muestra el estado actual de registros y memoria completa."""
        print("\nREGISTROS:")
        print(f"accumulator            {self._formato(self.accumulator):>7}")
        print(f"instructionCounter     {self.instructionCounter:>7}")
        print(f"instructionRegister    {self._formato(self.instructionRegister):>7}")
        print(f"operationCode          {self.operationCode:>7}")
        print(f"operand                {self.operand:>7}")

        print("\nMEMORIA:")
        print("     ", end="")
        for i in range(10):
            print(f"{i:6d}", end="")
        print()

        for i in range(0, TAM_MEMORIA, 10):
            print(f"{i:2d}   ", end="")
            for j in range(10):
                print(f"{self._formato(self.memoria[i + j]):>6}", end="")
            print()

    def _formato(self, valor):
        signo = "+" if valor >= 0 else "-"
        return f"{signo}{abs(valor):04d}"

    def ejecutar(self):
        """Ciclo principal de ejecucion fetch-decode-execute."""
        print("\n*** Inicio de la ejecucion del programa ***")
        while self.en_ejecucion:
    # Verificamos que el contador apunte a una direccion valida
            if self.instructionCounter < 0 or self.instructionCounter >= TAM_MEMORIA:
                self._error_fatal("Direccion de instruccion invalida")
                break

      # Fetch: recuperamos instruccion de memoria
            self.instructionRegister = self.memoria[self.instructionCounter]

       # Una instruccion negativa no es valida
            if self.instructionRegister < 0:
                self._error_fatal("Instruccion invalida (negativa)")
                break

 # Decode: decodificamos codigo y operando
            self.operationCode = self.instructionRegister // 100
            self.operand = self.instructionRegister % 100

       # El contador avanza a la siguiente instruccion
          # (las bifurcaciones lo cambian despues)
            self.instructionCounter += 1

      
       # Execute: ejecutamos instruccion
            self._ejecutar_instruccion()

    def _ejecutar_instruccion(self):
        op = self.operationCode
        operando = self.operand

        if op == LEER:
            try:
                valor = int(input("Ingrese un entero: "))
            except ValueError:
                self._error_fatal("La entrada no es un entero valido")
                return
            if valor < MIN_VALOR or valor > MAX_VALOR:
                self._error_fatal("Valor fuera de rango (-9999 a 9999)")
            else:
                self.memoria[operando] = valor
        elif op == ESCRIBIR:
            print(self.memoria[operando])
        elif op == CARGAR:
            self.accumulator = self.memoria[operando]
        elif op == ALMACENAR:
            self.memoria[operando] = self.accumulator
        elif op == SUMAR:
            self.accumulator += self.memoria[operando]
            self._verificar_desbordamiento()
        elif op == RESTAR:
            self.accumulator -= self.memoria[operando]
            self._verificar_desbordamiento()
        elif op == MULTIPLICAR:
            self.accumulator *= self.memoria[operando]
            self._verificar_desbordamiento()
        elif op == DIVIDIR:
            divisor = self.memoria[operando]
            if divisor == 0:
                self._error_fatal("Intento de division entre cero")
            else:
            # int() trunca hacia cero
                self.accumulator = int(self.accumulator / divisor)
        elif op == BIFURCAR:
            self.instructionCounter = operando
        elif op == BIFURCAR_NEGATIVO:
            if self.accumulator < 0:
                self.instructionCounter = operando
        elif op == BIFURCAR_CERO:
            if self.accumulator == 0:
                self.instructionCounter = operando
        elif op == SALTO_LINEA:
            print()
        elif op == MODULO:
            divisor = self.memoria[operando]
            if divisor == 0:
                self._error_fatal("Intento de modulo entre cero")
            else:
                self.accumulator = self.accumulator - int(self.accumulator / divisor) * divisor
        elif op == POTENCIA:
            exponente = self.memoria[operando]
            if exponente < 0:
                self._error_fatal("Exponente negativo")
            elif abs(self.accumulator) > 1 and exponente > 14:
                self._error_fatal("Desbordamiento del acumulador")
            else:
                self.accumulator = self.accumulator ** exponente
                self._verificar_desbordamiento()
        elif op == ESCRIBIR_CADENA:
            self._escribir_cadena()
        elif op == LEER_CADENA:
            self._leer_cadena()
        elif op == DETENER:
            print("*** Ejecucion detenida por Simpletron ***")
            self.en_ejecucion = False
        else:
            self._error_fatal(f"Codigo de operacion invalido: {op}")

    def _verificar_desbordamiento(self):
        if self.accumulator < MIN_VALOR or self.accumulator > MAX_VALOR:
            self._error_fatal("Desbordamiento del acumulador")

    def _escribir_cadena(self):
        inicio = self.operand
        longitud = self.memoria[inicio]
        if longitud < 0 or inicio + longitud >= TAM_MEMORIA:
            self._error_fatal("Cadena invalida en memoria")
            return

        texto = ""
        for posicion in range(inicio + 1, inicio + longitud + 1):
            codigo = self.memoria[posicion]
            if codigo < 0:
                self._error_fatal("Caracter invalido en la cadena")
                return
            texto += chr(codigo)

        print(texto, end="")

    def _leer_cadena(self):
        texto = input("Ingrese una cadena: ")
        inicio = self.operand
        if inicio + len(texto) >= TAM_MEMORIA:
            self._error_fatal("La cadena no cabe en la memoria")
            return

        for letra in texto:
            if ord(letra) > MAX_VALOR:
                self._error_fatal("Caracter fuera de rango")
                return

        self.memoria[inicio] = len(texto)
        posicion = inicio + 1
        for letra in texto:
            self.memoria[posicion] = ord(letra)
            posicion += 1

    def _error_fatal(self, mensaje):
        print(f"\n*** Error fatal: {mensaje} ***")
        print("*** Simpletron terminando la ejecucion ***")
        self.en_ejecucion = False




#_______________________________________________________#
def main():
    simulador = Simpletron()
    if len(sys.argv) > 1:
        if not simulador.cargar_archivo(sys.argv[1]):
            return
    else:
        simulador.cargar_programa()
    simulador.ejecutar()
    simulador.volcado_memoria()


if __name__ == "__main__":
    main()
