from anidamiento import verificar_anidamiento


def _separar_tokens(expresion):
    tokens = []
    posicion = 0

    while posicion < len(expresion):
        caracter = expresion[posicion]

        if caracter.isspace():
            posicion += 1
        elif caracter.isdigit():
            numero = caracter
            posicion += 1
            while posicion < len(expresion) and expresion[posicion].isdigit():
                numero += expresion[posicion]
                posicion += 1
            tokens.append(numero)
        elif caracter.isalpha() and caracter.islower():
            tokens.append(caracter)
            posicion += 1
        elif caracter in "+-*/^()":
            if caracter == "-" and (not tokens or tokens[-1] in ["+", "-", "*", "/", "^", "(", "NEG"]):
                tokens.append("NEG")
            else:
                tokens.append(caracter)
            posicion += 1
        else:
            raise ValueError(f"Caracter no valido: {caracter}")

    return tokens


def convertir_a_postfija(expresion):
    if not verificar_anidamiento(expresion):
        raise ValueError("Los parentesis no estan balanceados")

    tokens = _separar_tokens(expresion)
    salida = []
    operadores = []
    prioridad = {"+": 1, "-": 1, "*": 2, "/": 2, "NEG": 3, "^": 4}
    asociativos_derecha = ["^", "NEG"]

    for token in tokens:
        if token.isdigit() or (len(token) == 1 and token.isalpha()):
            salida.append(token)
        elif token == "(":
            operadores.append(token)
        elif token == ")":
            while operadores and operadores[-1] != "(":
                salida.append(operadores.pop())
            if not operadores:
                raise ValueError("Falta un parentesis de apertura")
            operadores.pop()
        else:
            while operadores and operadores[-1] != "(":
                ultimo = operadores[-1]
                if prioridad[ultimo] > prioridad[token]:
                    salida.append(operadores.pop())
                elif prioridad[ultimo] == prioridad[token] and token not in asociativos_derecha:
                    salida.append(operadores.pop())
                else:
                    break
            operadores.append(token)

    while operadores:
        token = operadores.pop()
        if token == "(":
            raise ValueError("Falta un parentesis de cierre")
        salida.append(token)

    return " ".join(salida)


def evaluar_postfija(postfija, variables=None):
    if variables is None:
        variables = {}

    pila = []
    tokens = postfija.split()

    for token in tokens:
        if token.isdigit():
            pila.append(int(token))
        elif len(token) == 1 and token.isalpha():
            if token not in variables:
                raise ValueError(f"Falta un valor para la variable {token}")
            pila.append(variables[token])
        elif token == "NEG":
            if len(pila) < 1:
                raise ValueError("Falta un operando")
            pila.append(-pila.pop())
        else:
            if len(pila) < 2:
                raise ValueError("Faltan operandos")
            segundo = pila.pop()
            primero = pila.pop()

            if token == "+":
                pila.append(primero + segundo)
            elif token == "-":
                pila.append(primero - segundo)
            elif token == "*":
                pila.append(primero * segundo)
            elif token == "/":
                if segundo == 0:
                    raise ValueError("No se puede dividir entre cero")
                pila.append(primero / segundo)
            elif token == "^":
                pila.append(primero ** segundo)
            else:
                raise ValueError(f"Operador no valido: {token}")

    if len(pila) != 1:
        raise ValueError("La expresion no esta completa")

    return pila[0]


def main():
    expresion = input("Escribe una expresion: ")
    try:
        postfija = convertir_a_postfija(expresion)
        print(f"Postfija: {postfija}")
        try:
            resultado = evaluar_postfija(postfija)
            print(f"Resultado: {resultado}")
        except ValueError as error:
            print(f"No se pudo evaluar: {error}")
    except ValueError as error:
        print(f"Expresion invalida: {error}")


if __name__ == "__main__":
    main()
