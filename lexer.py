def encontrar_indice(simbolo):
    i = 0
    for alf in alfabeto:
        if simbolo == alf:
            return i
        else:
            i += 1
    return None  # Muy importante

def lexer(cadena):
    i = 0
    while i < len(cadena):
        simbolo = cadena[i]
        #Si la entrada tiene una salida
        if (estado_inicial, simbolo) in funcion_salida:
            indice = encontrar_indice(simbolo)
            if indice is not None:
                print(f"LEXEMA: {alfabeto[indice]} -> TOKEN: {tokens[indice]}")
            else:
                #Buscar en letras y numeros
                print(f"LEXEMA: {simbolo} -> TOKEN: {funcion_salida[(estado_inicial, simbolo)]}")
        else:
            print(f"ERROR: Símbolo inválido '{simbolo}'")
        i += 1

letras = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚ"
          "üÜñÑ")
numeros = "0123456789"
alfabeto = ("<", "?", "!", " ", "\t", "\n", '"', "=", "-", ">",
            "/", ":", ".", "'", "{", ";", ",", "}", "#", "&", "%", "+", "@", "|",
            "\\", "^", "´", "$", "(", ")", "[", "]", "_", "*", "¿", "¡")
tokens = ("MENOR_QUE", "PREGUNTA_FIN", "EXCLAMACION_FIN",
          "ESPACIO", "TABULACION", "SALTO_LINEA", "COMILLA_DOBLE", "IGUAL",
          "GUION", "MAYOR_QUE", "SLASH", "DOS_PUNTOS", "PUNTO", "COMILLA_SIMPLE",
          "CORCHETE_INICIO", "PUNTO_COMA", "COMA", "CORCHETE_FIN", "NUMERAL",
          "AMPERSAND", "PORCENTAJE", "MAS", "ARROBA", "PIPE", "BACKSLASH",
          "POTENCIA", "TILDE", "DOLAR", "PARENTESIS_INICIO", "PARENTESIS_FIN",
          "CORCHETE_RECT_INICIO", "CORCHETE_RECT_FIN", "GUION_BAJO", "ASTERISCO",
          "PREGUNTA_INICIO", "EXCLAMACION_INICIO", "ERROR")
funcion_salida = {}
estado_inicial = "q0"

for letra in letras:
    funcion_salida[(estado_inicial, letra)] = "PALABRA"

for numero in numeros:
    funcion_salida[(estado_inicial, numero)] = "NUMERO"

i = 0
for alf in alfabeto:
    funcion_salida[(estado_inicial, alf)] = tokens[i]
    i += 1

# Leer archivo
with open("entrada.txt", "r", encoding="utf-8") as archivo:
    contenido = archivo.read()
    print(f"Procesando: {repr(contenido)}")
    lexer(contenido)