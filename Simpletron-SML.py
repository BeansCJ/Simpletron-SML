#Carlo Emilio Cballero Robles - 3515208

"""
 Simulador de simpletron
 Proyecto de Simulador de una comuptadora virtual Simpletron (SML).
"""


TAM_MEMORIA = 100

class Simpletron:
    def __init__(self):
        # Inicializamos la memoria y los registros requeridos por la rúbrica
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
        
    
def main():
    simulador = Simpletron()
    simulador.cargar_programa()

if __name__ == "__main__":
    main()
    
    # En el Día 2 agregaremos la lógica para capturar los datos a traves de la terminal
    