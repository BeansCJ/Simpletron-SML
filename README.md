# Proyecto Simpletron, SML y lenguaje Simple

**Autor:** Carlo Emilio Caballero Robles - 3515208

## Descripcion

Este proyecto contiene un simulador de Simpletron que ejecuta programas SML, herramientas para convertir y evaluar expresiones, y un compilador de programas Simple a SML. El simulador usa una memoria de 100 posiciones e incluye instrucciones aritmeticas, saltos, carga desde archivo y entrada y salida de cadenas.

## Requisitos

- Python 3.10 o posterior
- No se necesitan librerias externas

## Estructura

```text
README.md
docs/
  requerimientos.md
  diseno.md
src/
  simpletron/simpletron.py
  expresiones/anidamiento.py
  expresiones/expresiones.py
  compilador/compilador.py
programas/
  sml/
  simple/
pruebas/
evidencias/
```

## Ejecutar Simpletron

Para cargar un programa desde un archivo:

```bash
python src/simpletron/simpletron.py programas/sml/modulo.sml
```

Tambien se puede ejecutar sin archivo y escribir las instrucciones cuando el programa las solicite:

```bash
python src/simpletron/simpletron.py
```

En el modo interactivo, escribe `9999` para terminar de cargar instrucciones y comenzar la ejecucion.

Los archivos SML contienen una palabra numerica por linea. Se permiten lineas vacias y comentarios que comiencen despues de `;`.

### Instrucciones SML

| Codigo | Operacion |
|---:|---|
| 10 | Leer entero |
| 11 | Escribir entero |
| 12 | Salto de linea |
| 13 | Escribir cadena |
| 14 | Leer cadena |
| 20 | Cargar en el acumulador |
| 21 | Guardar el acumulador |
| 30 | Sumar |
| 31 | Restar |
| 32 | Dividir |
| 33 | Multiplicar |
| 34 | Residuo o modulo |
| 35 | Potencia |
| 40 | Salto incondicional |
| 41 | Salto si es negativo |
| 42 | Salto si es cero |
| 43 | Detener |

Los programas de ejemplo estan en `programas/sml/`.

## Expresiones

Ejecuta la herramienta interactiva:

```bash
python src/expresiones/expresiones.py
```

Convierte expresiones infijas a postfijas y evalua numeros enteros, variables, parentesis y los operadores `+`, `-`, `*`, `/` y `^`. La funcion de balanceo de parentesis, corchetes y llaves se conserva en `anidamiento.py`.

## Lenguaje Simple y compilador

El compilador recibe un archivo Simple y genera un archivo SML:

```bash
python src/compilador/compilador.py programas/simple/suma.simple programas/sml/compilados/suma.sml
```

Ejecuta el resultado en Simpletron:

```bash
python src/simpletron/simpletron.py programas/sml/compilados/suma.sml
```

El programa de suma pide dos enteros. Por ejemplo, con `8` y `9`, imprime `17`.

Comandos disponibles en Simple:

```text
10 input a
20 input b
30 let c = a + b
40 print c
50 end
```

El compilador reconoce `rem`, `input`, `let`, `print`, `goto`, `if ... goto` y `end`. Las variables son letras minusculas individuales; los numeros de linea deben ir en orden ascendente.

## Pruebas

Desde la carpeta principal del proyecto:

```bash
python -B -m unittest discover -s pruebas -v
```

## Documentacion y evidencias

- `docs/requerimientos.md`: resumen de los requisitos y componentes.
- `docs/diseno.md`: decisiones de diseño y limites conocidos.
- `evidencias/ejecuciones/`: capturas de ejecucion.
- `evidencias/git-branch/`: capturas de ramas e historial Git.
