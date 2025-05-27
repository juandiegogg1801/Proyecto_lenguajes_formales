import re

def encontrar_indice(simbolo):
    i = 0
    for alf in alfabeto:
        if simbolo == alf:
            return i
        else:
            i += 1
    return None  # Muy importante

def buscar_punto(lexema_actual):
    for lex in lexema_actual:
        if lex == '.':
            return True
    return False

def es_decimal(cadena):
    try:
        float(cadena)
        return True
    except ValueError:
        return False

#Separa el último caracter de una cadena
def separar_ultimo(cadena):
    if len(cadena) >= 2:
        parte_principal = cadena[:-1]  # Todo menos los últimos dos
        return parte_principal
    else:
        return "", cadena  # Si la cadena tiene menos de 2 caracteres

def obtener_ultimo_caracter(cadena):
    if cadena:  # Verifica que la cadena no esté vacía
        return cadena[-1]
    else:
        return None  # O puedes lanzar una excepción si prefieres

def lexer(cadena):
    i = 0
    lexema_actual = ""
    while i < len(cadena):
        simbolo = cadena[i]
        #Si la entrada tiene una salida
        if (estado_inicial, simbolo) in funcion_salida:
            indice = encontrar_indice(simbolo)
            if indice is not None and lexema_actual=="": #si esta en el alfabeto
                print(f"LEXEMA: {alfabeto[indice]} -> TOKEN: {tokens[indice]}")
                i += 1
            else:
                #Buscar en letras y numeros
                #simbolo y lexema actual letra o vacio
                if simbolo.isalpha() and (lexema_actual == "" or lexema_actual.isalpha()):
                    lexema_actual += simbolo
                    i += 1
                #simbolo y lexema actual numero  o vacio
                elif simbolo.isdigit() and (lexema_actual == "" or es_decimal(lexema_actual)):
                    lexema_actual += simbolo
                    i += 1
                # lexema actual letra y simbolo no es letra
                elif lexema_actual.isalpha() and not simbolo.isalpha():
                    print(f"LEXEMA: {lexema_actual} -> TOKEN: PALABRA")
                    lexema_actual = ""
                #lexema actual numero y simbolo no es numero
                else:
                    # si lexema actual punto
                    if simbolo == "." and buscar_punto(lexema_actual)==False:
                        lexema_actual += simbolo
                        i += 1
                    #si no
                    else:
                        ultimo = obtener_ultimo_caracter(lexema_actual)
                        if ultimo == ".":
                            principal = separar_ultimo(lexema_actual)
                            print(f"LEXEMA: {principal} -> TOKEN: NUMERO")
                            print(f"LEXEMA: . -> TOKEN: PUNTO")
                            lexema_actual = ""
                        else:
                            print(f"LEXEMA: {lexema_actual} -> TOKEN: NUMERO")
                            lexema_actual = ""
        else:
            #si habia antes un numero o una letra:
            if es_decimal(lexema_actual):
                ultimo = obtener_ultimo_caracter(lexema_actual)
                if ultimo == ".":
                    principal = separar_ultimo(lexema_actual)
                    print(f"LEXEMA: {principal} -> TOKEN: NUMERO")
                    print(f"LEXEMA: . -> TOKEN: PUNTO")
                    lexema_actual = ""
                else:
                    print(f"LEXEMA: {lexema_actual} -> TOKEN: NUMERO")
                    lexema_actual = ""
            elif lexema_actual.isalpha():
                print(f"LEXEMA: {lexema_actual} -> TOKEN: PALABRA")
                lexema_actual = ""
            print(f"ERROR: Símbolo inválido '{simbolo}'")
            i += 1
    if es_decimal(lexema_actual):
        ultimo = obtener_ultimo_caracter(lexema_actual)
        if ultimo == ".":
            principal = separar_ultimo(lexema_actual)
            print(f"LEXEMA: {principal} -> TOKEN: NUMERO")
            print(f"LEXEMA: . -> TOKEN: PUNTO")
            lexema_actual = ""
        else:
            print(f"LEXEMA: {lexema_actual} -> TOKEN: NUMERO")
            lexema_actual = ""
    elif lexema_actual.isalpha():
        print(f"LEXEMA: {lexema_actual} -> TOKEN: PALABRA")
        lexema_actual = ""


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