


# Diseno del proyecto (CORERGIDO CON IA)
## Simulador
Simpletron guarda las instrucciones y los datos en una lista de 100 posiciones. Cada instruccion se separa en codigo de operacion y operando. El ciclo de ejecucion actualiza el contador de instrucciones y ejecuta la operacion correspondiente.

Los archivos SML contienen un valor entero por linea. Las lineas vacias se ignoran y el texto despues de `;` se trata como comentario. Para una cadena, la primera posicion guarda su longitud y las siguientes posiciones guardan los codigos de sus caracteres.

## Expresiones
La conversion a postfija usa una pila de operadores. La evaluacion postfija usa una pila de operandos. Los parentesis determinan el orden de agrupacion y la potencia se asocia de derecha a izquierda.

## Compilador Simple
La primera pasada valida el orden de las lineas y registra lineas, variables y constantes. La segunda genera instrucciones SML simbolicas. Al final se asignan direcciones a variables, constantes y temporales; tambien se resuelven las referencias a lineas, incluidas las referencias hacia adelante.

Las expresiones se convierten a postfija y se traducen a operaciones de carga, almacenamiento y aritmetica. Las condiciones se convierten en restas y bifurcaciones condicionales.

## Limites conocidos
- Tanto el programa generado como sus datos deben caber en las 100 posiciones de memoria.
- Las palabras y datos se mantienen dentro del rango SML de -9999 a 9999.
- Una resta usada para evaluar una condicion con valores extremos puede desbordar el acumulador; por eso los operandos de una comparacion deben mantenerse dentro del rango que permita la resta.
- La entrada de cadenas solo acepta caracteres con codigo numerico de hasta 9999.
