# Simulador Simpletron (SML) y Profundidad de Anidamienfo
**Autor:** Carlo Emilio Caballero Robles - 3515208

## Descripcion
Proyecto de la materia de Programación Avanzada. Incluye un simulador funcional de la computadora virtual Simpletron (SML) capaz de ejecutar las 12 operaciones básicas, y un programa adicional que evalúa la profundidad de anidamiento en expresiones matemáticas mediante una pila.

## Archivos del Proyecto
1. "Simpletron-SML.py": Simulador principal (memoria de 100 posiciones, ciclo fetch-decode-execute).
2. "Anidamiento.py": Evaluador de expresiones usando pila.

## Instrucciones de Ejecución:
### Para el Simpletron:

Ejecutar en la terminal:
"python Simpletron-SML.py"
Ingresar las instrucciones SML línea por línea. Escribir `9999` para finalizar la carga y comenzar la ejecución. El programa detecta automáticamente desbordamientos, operaciones inválidas y divisiones entre cero, generando un volcado de memoria al finalizar.

### Para el Evaluador de Anidamiento:

Ejecutar en la terminal:
"python Anidamiento.py"
Ingresar una expresión (ej. '{a + [b * (c - d)]}'). El programa devolverá Verdadero (1) si está balanceada o Falso (0) si no lo está. De igual forma si no hay nada que valancear devolvera Verdadero