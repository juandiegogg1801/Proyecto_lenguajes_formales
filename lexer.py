def encontrar_indice(simbolo):
    i = 0
    for alf in alfabeto:
        if simbolo == alf:
            return i
        else:
            i += 1
    return None  # Muy importante

def bucar_punto(lexema_actual):
    for lex in lexema_actual:
        if lex == '.':
            return True
        else:
            return False

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
                elif simbolo.isdigit() and (lexema_actual == "" or lexema_actual.isdigit()):
                    lexema_actual += simbolo
                    i += 1
                # lexema actual letra y simbolo no es letra
                elif lexema_actual.isalpha() and not simbolo.isalpha():
                    print(f"LEXEMA: {lexema_actual} -> TOKEN: PALABRA")
                    lexema_actual = ""
                #lexema actual numero y simbolo no es numero
                else:
                    # si lexema actual punto
                    if simbolo == "." and bucar_punto(lexema_actual)==False:
                        lexema_actual += simbolo
                        i += 1
                    #si no
                    else:
                        print(f"LEXEMA: {lexema_actual} -> TOKEN: NUMERO")
                        lexema_actual = ""
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