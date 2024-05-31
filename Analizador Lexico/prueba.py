import flet as ft
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
        tokens.append({'Type': 'Error', 'Value': str(e), 'Start': '', 'End': '', 'Line': ''})
    except SyntaxError as e:
        tokens.append({'Type': 'Error', 'Value': str(e), 'Start': '', 'End': '', 'Line': ''})
    except Exception as e:
        tokens.append({'Type': 'Error', 'Value': str(e), 'Start': '', 'End': '', 'Line': ''})
    
    return tokens

def tokens_to_string(tokens):
    result = f"{'Type':<15} {'Value':<15} {'Start':<10} {'End':<10} {'Line'}\n"
    result += "-" * 60 + "\n"
    for token in tokens:
        result += f"{token['Type']:<15} {token['Value']:<15} {str(token['Start']):<10} {str(token['End']):<10} {token['Line']}\n"
    return result

def main(page: ft.Page):
    page.title = "Analizador Léxico de Python"
    
    # Campo de texto para introducir código
    code_input = ft.TextField(
        label="Código Python",
        multiline=True,
        width=500,
        height=300,
    )
    
    # Campo de texto para mostrar la tabla de tokens
    output_field = ft.TextField(
        label="Tokens Generados",
        multiline=True,
        width=500,
        height=300,
        read_only=True,
    )
    
    # Botón para generar la tabla
    def generar_tabla(e):
        codigo = code_input.value
        tokens = analizar_codigo_python(codigo)
        output_text = tokens_to_string(tokens)
        output_field.value = output_text
        page.update()
    
    generar_button = ft.ElevatedButton(
        text="Generar Tabla",
        on_click=generar_tabla
    )
    
    # Añadir componentes a la página
    page.add(
        ft.Row([code_input, output_field]),
        generar_button
    )

ft.app(target=main)
