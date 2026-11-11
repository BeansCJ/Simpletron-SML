# Carlo Emilio Caballero Robles - 3515208

"""
Programa para evaluar la profundidad de anidamiento de expresiones.
Verifica que los parentesis, corchetes y llaves esten bien balanceados.
"""

def verificar_anidamiento(expresion):
    pila = []
    # Diccionario para mapear los cierres con sus aperturas
    pares = {')': '(', ']': '[', '}': '{'}
    
    for symb in expresion:
        # 2.2. Si lo que hay en symb es ( o { o [
        if symb in ['(', '[', '{']:
            pila.append(symb) # 2.2.1 push(symb)
            
        # 2.3. Si lo que hay en symb es ) o } o ]
        elif symb in [')', ']', '}']:
            # 2.3.1. Si isEmpty()
            if not pila: 
                return False
                
            # 2.3.2.1 temp = pop()
            temp = pila.pop()
            
            # 2.3.2.2 Si el caracter en symb no es equivalente al caracter en temp
            if temp != pares[symb]:
                return False
                
    # 3. Si not isEmpty()
    if pila: 
        return False
        
    # 4. return verdadero
    return True

def main():
    print("*** Evaluador de Profundidad de Anidamiento ***")
    cadena = input("Ingresa la expresion a evaluar: ")
    
    if verificar_anidamiento(cadena):
        print("Verdadero (1) - La expresion esta correcta")
    else:
        print("falso (0) - La expresion no es correcta")

if __name__ == "__main__":
    main()