# Carlo Emilio Caballero Robles - 3515208

"""
 Simulador de simpletron
 Proyecto de Simulador de una comuptadora virtual Simpletron (SML).
"""

TAM_MEMORIA = 100

# Codigos de operacion SML
LEER = 10
ESCRIBIR = 11
CARGAR = 20
ALMACENAR = 21
SUMAR = 30
RESTAR = 31
DIVIDIR = 32
MULTIPLICAR = 33
BIFURCAR = 40
BIFURCAR_NEGATIVO = 41
BIFURCAR_CERO = 42
DETENER = 43


class Simpletron:
    def __init__(self):
        self.memoria = [0] * TAM_MEMORIA
        self.acumulador = 0
        self.contador_instrucciones = 0
        self.registro_instruccion = 0
        self.codigo_operacion = 0
        self.operando = 0
        self.en_ejecucion = True

    def cargar_programa(self):
        """Solicita al usuario las instrucciones y datos."""
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

            if -9999 <= valor <= 9998:
                self.memoria[direccion] = valor
                direccion += 1
            else:
                print("*** Error: la instruccion debe estar entre -9999 y +9998 ***")

    def volcado_memoria(self):
        """Muestra el estado acutual de registros y memoria completa."""
        print("\nREGISTROS:")
        print(f"acumulador            {self._formato(self.acumulador):>7}")
        print(f"contador_instrucciones{self.contador_instrucciones:>7}")
        print(f"registro_instruccion  {self._formato(self.registro_instruccion):>7}")
        print(f"codigo_operacion      {self.codigo_operacion:>7}")
        print(f"operando              {self.operando:>7}")

        print("\nMEMORIA:")
        print("     ", end="")
        for i in range(10):
            print(f"{i:5d}", end="")
        print()

        for i in range(0, TAM_MEMORIA, 10):
            print(f"{i:2d}   ", end="")
            for j in range(10):
                print(f"{self._formato(self.memoria[i + j]):>5}", end="")
            print()

    def _formato(self, valor):
        signo = "+" if valor >= 0 else "-"
        return f"{signo}{abs(valor):04d}"

    def ejecutar(self):
        """Ciclo prinicpal de ejecucion fetch-decode-execute."""
        print("\n*** Inicio de la ejecucion del prgrama ***")
        while self.en_ejecucion and 0 <= self.contador_instrucciones < TAM_MEMORIA:
            # Fetch: recuperamos instruccion de memoria
            self.registro_instruccion = self.memoria[self.contador_instrucciones]

            # Decode: decodificamos codigo y operando
            self.codigo_operacion = self.registro_instruccion // 100
            self.operando = self.registro_instruccion % 100

            # Execute: ejecutamos instruccion
            self._ejecutar_instruccion()

    def _ejecutar_instruccion(self):
        op = self.codigo_operacion

        if op == LEER:
            try:
                valor = int(input("Ingrese un entero: "))
                self.memoria[self.operando] = valor
                self.contador_instrucciones += 1
            except ValueError:
                self._error_fatal("Entrada no es un entero valido")
        elif op == ESCRIBIR:
            print(self.memoria[self.operando])
            self.contador_instrucciones += 1
        elif op == CARGAR:
            self.acumulador = self.memoria[self.operando]
            self.contador_instrucciones += 1
        elif op == ALMACENAR:
            self.memoria[self.operando] = self.acumulador
            self.contador_instrucciones += 1
        elif op == SUMAR:
            self.acumulador += self.memoria[self.operando]
            if self._verificar_desbordamiento():
                self.contador_instrucciones += 1
        elif op == RESTAR:
            self.acumulador -= self.memoria[self.operando]
            if self._verificar_desbordamiento():
                self.contador_instrucciones += 1
        elif op == MULTIPLICAR:
            self.acumulador *= self.memoria[self.operando]
            if self._verificar_desbordamiento():
                self.contador_instrucciones += 1
        elif op == DIVIDIR:
            divisor = self.memoria[self.operando]
            if divisor == 0:
                self._error_fatal("Intento de division entre cero")
            else:
                self.acumulador //= divisor
                self.contador_instrucciones += 1
        elif op == BIFURCAR:
            self.contador_instrucciones = self.operando
        elif op == BIFURCAR_NEGATIVO:
            if self.acumulador < 0:
                self.contador_instrucciones = self.operando
            else:
                self.contador_instrucciones += 1
        elif op == BIFURCAR_CERO:
            if self.acumulador == 0:
                self.contador_instrucciones = self.operando
            else:
                self.contador_instrucciones += 1
        elif op == DETENER:
            print("*** Ejecucion detendia por Simpletron ***")
            self.en_ejecucion = False
        else:
            self._error_fatal(f"Codigo de operacion invalido: {op}")

    def _verificar_desbordamiento(self):
        if not (-9999 <= self.acumulador <= 9998):
            self._error_fatal("Desbordamiento del acumulador")
            return False
        return True

    def _error_fatal(self, mensaje):
        print(f"\n*** Error fatal: {mensaje} ***")
        print("*** Simpletron terminando la ejecucion ***")
        self.en_ejecucion = False


def main():
    simulador = Simpletron()
    simulador.cargar_programa()
    simulador.ejecutar()
    simulador.volcado_memoria()


if __name__ == "__main__":
    main() 