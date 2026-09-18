#Carlo Emilio Cballero Robles - 3515208

"""
 Simulador de simpletron
 Proyecto de Simulador de una comuptadora virtual Simpletron (SML).
"""


TAM_MEMORIA = 100

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

def main():
    simulador = Simpletron()
    simulador.cargar_programa()

if __name__ == "__main__":
    main()