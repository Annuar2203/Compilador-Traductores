"""
numero = 5
if numero % 2 == 0:
    print("El numero es par")
else:
    print("El numero es impar")
"""

import tokenize
import io

def analizar_codigo_python(codigo):
    buffer = io.StringIO(codigo)
    tokens = []

    try:
        for tok in tokenize.generate_tokens(buffer.readline):
            tokens.append({
                'Type': tokenize.tok_name[tok.type],
                'Value': tok.string,
                'Start': tok.start,
                'End': tok.end,
                'Line': tok.line.strip()
            })
    except tokenize.TokenError as e:
        print(f"Error de tokenización: {e}")
    except SyntaxError as e:
        print(f"Error de sintaxis: {e}")
    except Exception as e:
        print(f"Error desconocido: {e}")
    
    return tokens

def imprimir_tokens(tokens):
    print(f"{'Type':<15} {'Value':<15} {'Start':<10} {'End':<10} {'Line'}")
    print("-" * 60)
    for token in tokens:
        print(f"{token['Type']:<15} {token['Value']:<15} {str(token['Start']):<10} {str(token['End']):<10} {token['Line']}")
        if token['Type'] == "NEWLINE":
            print("")
            print("")

# Ejemplo de código Python a analizar
codigo_ejemplo = """
def suma(a, b):
    return a + b

resultado = suma(5, 3)
print(resultado)
"""

# Analizamos el código de ejemplo
tokens = analizar_codigo_python(codigo_ejemplo)

# Imprimimos los tokens generados
imprimir_tokens(tokens)
