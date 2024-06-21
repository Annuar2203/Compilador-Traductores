import flet as ft #frameor utilizado para hacer la interfaz grafica
import tokenize #utilizada para trabajar con tokens
import io #trabaja con datos de entrada y salida

def analizar_codigo_python(codigo):
    codigo_python = io.StringIO(codigo) #Utilizado para extraer el texto de un archivo y retornar linea por linea
    tokens = [] #usado para guardar tokens

    try:
        for tok in tokenize.generate_tokens(codigo_python.readline):
            tokens.append({ #diccionario que guarda cada token analizando cada linea del codigo
                'Tipo': tokenize.tok_name[tok.type],
                'Caracter': tok.string,
                'Empieza': tok.start,
                'Termina': tok.end,
                'Linea': tok.line.strip()
            })
    except tokenize.TokenError as e:
        tokens.append({'Tipo': 'Error', 'Carácter': str(e), 'Empieza': '', 'Termina': '', 'Linea': ''})
    except SyntaxError as e:
        tokens.append({'Tipo': 'Error', 'Carácter': str(e), 'Empieza': '', 'Termina': '', 'Linea': ''})
    except Exception as e:
        tokens.append({'Tipo': 'Error', 'Carácter': str(e), 'Empieza': '', 'Termina': '', 'Linea': ''})
    
    return tokens

def tokens_string(tokens):
    resultado = ( #cabecera de la salida
        f"{'Tipo':^15} {'Carácter':<15} {'Empieza':^10} {'Termina':^10} {'Linea':<50}\n"
        f"{'-' * 85}\n"
    )
    for token in tokens:
        resultado += ( #analisis y extraccion de tokens del codigo
            f"{token['Tipo']:^15} {token['Caracter']:<15} {str(token['Empieza']):^10} {str(token['Termina']):^10} {token['Linea']:<50}\n"
        )
    return resultado

def main(page: ft.Page):
    
    page.window_maximized = True

    page.title = "Analizador Léxico de Python"

    # Campo de texto para mostrar el contenido del archivo
    codigo_contenido = ft.TextField(
        label="Contenido del Archivo",
        multiline=True,
        width=500,
        height=300,
        read_only=True,
    )
    
    # Campo de texto para mostrar la tabla de tokens
    campo_salida = ft.TextField(
        label="Tokens Generados",
        multiline=True,
        width=800,
        height=300,
        read_only=True,
    )
    
    # Función para manejar la carga del archivo
    def manejar_archivo(e):
        if e.files:
            # Leer el contenido del archivo subido
            ruta_archivo = e.files[0].path
            with open(ruta_archivo, "r") as file:
                codigo = file.read()
            
            # Mostrar el contenido del archivo en codigo_contenido
            codigo_contenido.value = codigo
            
            # Generar tokens y mostrarlos en output_field
            tokens = analizar_codigo_python(codigo)
            texto_salida = tokens_string(tokens)
            campo_salida.value = texto_salida
            
            # Actualizar la página para reflejar los cambios
            page.update()
    
    # Campo para subir archivos
    file_picker = ft.FilePicker(on_result=manejar_archivo)
    
    # Asegurarse de que el file_picker esté en el overlay, es decir, para que este disponible y visible
    page.overlay.append(file_picker)
    
    # Botón para activar el diálogo de carga de archivos
    subir_archivo_button = ft.ElevatedButton( #widget de boton que crea un evento
        text="Subir Archivo Python",
        on_click=lambda _: file_picker.pick_files( #devuelve un solo archivo
            allow_multiple=False,
            allowed_extensions=["py"] # Solo permite archivos python
        )
    )
    
    # Añadir componentes a la página
    page.add(
        subir_archivo_button,
        ft.Row([codigo_contenido, campo_salida])
    )

ft.app(target=main)