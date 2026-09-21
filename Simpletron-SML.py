# Carlo Emilio Caballero Robles - 3515208

"""
 Simulador de simpletron
 Proyecto de Simulador de una comuptadora virtual Simpletron (SML).
"""

TAM_MEMORIA = 100

# Codigos de operacion
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
        """Solicita al usuario las instrucciones."""
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

    def ejecutar(self):
        """Ciclo prinicpal de ejecucion fetch-decode-execute."""
        print("\n*** Inicio de la ejecucion del prgrama ***")
        # Ciclo que seguira mientras el progarma no se detenga
        while self.en_ejecucion and 0 <= self.contador_instrucciones < TAM_MEMORIA:
            
            self.registro_instruccion = self.memoria[self.contador_instrucciones]

            # 
            self.codigo_operacion = self.registro_instruccion // 100
            self.operando = self.registro_instruccion % 100

            
            self._ejecutar_instruccion()

    def _ejecutar_instruccion(self):
        op = self.codigo_operacion

        # Evluamos que operacion se va a realizar
        if op == LEER:
            valor = int(input(f"Ingrese un entero: "))
            self.memoria[self.operando] = valor
            self.contador_instrucciones += 1
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
            self.contador_instrucciones += 1
        elif op == RESTAR:
            self.acumulador -= self.memoria[self.operando]
            self.contador_instrucciones += 1
        elif op == MULTIPLICAR:
            self.acumulador *= self.memoria[self.operando]
            self.contador_instrucciones += 1
        elif op == DIVIDIR:
            self.acumulador //= self.memoria[self.operando]
            self.contador_instrucciones += 1
        elif op == BIFURCAR:
            # Ssalto incondisional a la memoria dictada
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
            print(f"*** Operacion desconocdia: {op} ***")
            self.en_ejecucion = False

def main():
    simulador = Simpletron()
    simulador.cargar_programa()
    simulador.ejecutar()

if __name__ == "__main__":
    main()