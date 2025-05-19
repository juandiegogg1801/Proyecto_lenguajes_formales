def procesar_cadena(cadena):
    estado_actual = estado_inicial
    lexema_actual = ""
    i = 0
    while i < len(cadena):
        simbolo = cadena[i]

        if (estado_actual, simbolo) in transiciones:
            nuevo_estado = transiciones[(estado_actual, simbolo)]

            if estado_actual == "q3" and nuevo_estado != "q3":
                lexer("q4", lexema_actual)
                lexema_actual = ""
                estado_actual = estado_inicial
                continue  # Reanaliza el mismo símbolo

            estado_actual = nuevo_estado
            lexema_actual += simbolo
            i += 1

            if estado_actual in estados_finales and estado_actual not in {"q3"}:
                lexer(estado_actual, lexema_actual)
                estado_actual = estado_inicial
                lexema_actual = ""
        else:
            if estado_actual == "q3" and lexema_actual:
                lexer("q4", lexema_actual)
                estado_actual = estado_inicial
                lexema_actual = ""
                continue
            else:
                print(f"ERROR: Símbolo inválido '{simbolo}'")
                estado_actual = estado_inicial
                i += 1

    if estado_actual == "q3" and lexema_actual:
        lexer("q4", lexema_actual)

    print("Fin de archivo.")

def lexer(estado_final, lexema):
    if estado_final == "q1":
        print(f"LEXEMA: '{lexema}' → Tipo: TAG_OPEN")
    elif estado_final == "q2":
        print(f"LEXEMA: '{lexema}' → Tipo: PREGUNTA")
    elif estado_final == "q4":
        print(f"LEXEMA: '{lexema}' → Tipo: PALABRA")
    elif estado_final == "q5":
        print(f"LEXEMA: '{lexema}' → Tipo: EXCLAMACION")
    elif estado_final == "q6":
        print(f"LEXEMA: ' ' → Tipo: ESPACIO")
    elif estado_final == "q7":
        print(f"LEXEMA: '\\t' → Tipo: TABULACION")
    elif estado_final == "q8":
        print(f"LEXEMA: '\\n' → Tipo: SALTO_LINEA")
    else:
        print(f"LEXEMA: '{lexema}' → Tipo: ERROR")


# Autómata
estados = {"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8"}
letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
transiciones = {}

# Letras → q3
for letra in letras:
    transiciones[("q0", letra)] = "q3"
    transiciones[("q3", letra)] = "q3"

# Caracteres especiales únicos
transiciones[("q0", "<")] = "q1"
transiciones[("q0", "?")] = "q2"
transiciones[("q0", "!")] = "q5"
transiciones[("q0", " ")] = "q6"
transiciones[("q0", "\t")] = "q7"
transiciones[("q0", "\n")] = "q8"

estado_inicial = "q0"
estados_finales = {"q1", "q2", "q4", "q5", "q6", "q7", "q8"}

# Leer entrada
with open("entrada.txt", "r", encoding="utf-8") as archivo:
    contenido = archivo.read()
    print(f"Procesando: {repr(contenido)}")  # repr para visualizar \n, \t
    procesar_cadena(contenido)
