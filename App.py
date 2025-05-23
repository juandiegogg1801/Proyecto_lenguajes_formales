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
                continue

            if estado_actual == "q9" and nuevo_estado not in {"q9", "q10", "q11"}:
                lexer("q9", lexema_actual)
                lexema_actual = ""
                estado_actual = estado_inicial
                continue

            if estado_actual == "q11" and nuevo_estado not in {"q11"}:
                lexer("q9", lexema_actual)
                lexema_actual = ""
                estado_actual = estado_inicial
                continue

            estado_actual = nuevo_estado
            lexema_actual += simbolo
            i += 1

            if estado_actual in estados_finales and estado_actual not in {"q3", "q9", "q11"}:
                lexer(estado_actual, lexema_actual)
                estado_actual = estado_inicial
                lexema_actual = ""

        else:
            # Aquí detectas si estabas en medio de una palabra o número antes de cambiar de tipo
            if estado_actual == "q3" and lexema_actual:
                lexer("q4", lexema_actual)
            elif estado_actual in {"q9", "q11"} and lexema_actual:
                lexer("q9", lexema_actual)
            elif estado_actual in estados_finales and lexema_actual:
                lexer(estado_actual, lexema_actual)
            else:
                print(f"ERROR: Símbolo inválido '{simbolo}'")
            estado_actual = estado_inicial
            lexema_actual = ""
            # OJO: No pierdas el símbolo actual, vuelve a analizarlo
            continue

    # Al final, procesa el último lexema si quedó pendiente
    if estado_actual == "q3" and lexema_actual:
        lexer("q4", lexema_actual)
    elif estado_actual in {"q9", "q11"} and lexema_actual:
        lexer("q9", lexema_actual)
    elif estado_actual in estados_finales and lexema_actual:
        lexer(estado_actual, lexema_actual)

    print("Fin de archivo.")

def lexer(estado_final, lexema):
    if estado_final == "q1":
        print(f"LEXEMA: '{lexema}' → Tipo: TAG_OPEN")
    elif estado_final == "q2":
        print(f"LEXEMA: '{lexema}' → Tipo: PREGUNTA")
    elif estado_final == "q4":
        print(f"LEXEMA: '{lexema}' → Tipo: ALFANUMERICO")
    elif estado_final == "q5":
        print(f"LEXEMA: '{lexema}' → Tipo: EXCLAMACION")
    elif estado_final == "q6":
        print(f"LEXEMA: ' ' → Tipo: ESPACIO")
    elif estado_final == "q7":
        print(f"LEXEMA: '\\t' → Tipo: TABULACION")
    elif estado_final == "q8":
        print(f"LEXEMA: '\\n' → Tipo: SALTO_LINEA")
    elif estado_final == "q9":
        print(f"LEXEMA: '{lexema}' → Tipo: NUMERO")
    elif estado_final == "q12":
        print(f"LEXEMA: '{lexema}' → Tipo: COMILLA")
    elif estado_final == "q13":
        print(f"LEXEMA: '{lexema}' → Tipo: IGUAL")
    elif estado_final == "q14":
        print(f"LEXEMA: '{lexema}' → Tipo: GUION")
    elif estado_final == "q15":
        print(f"LEXEMA: '{lexema}' → Tipo: TAG_CLOSE")
    elif estado_final == "q16":
        print(f"LEXEMA: '{lexema}' → Tipo: SLASH")
    elif estado_final == "q17":
        print(f"LEXEMA: '{lexema}' → Tipo: DOS_PUNTOS")
    elif estado_final == "q18":
        print(f"LEXEMA: '{lexema}' → Tipo: PUNTO")
    elif estado_final == "q19":
        print(f"LEXEMA: '{lexema}' → Tipo: COMILLA_SIMPLE")
    else:
        print(f"LEXEMA: '{lexema}' → Tipo: ERROR")

# Autómata
estados = {"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "q14", "q15", "q16", "q17", "q18", "q19"}
letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚüÜñÑ"
numeros = "0123456789"
transiciones = {}

# Letras → q3
for letra in letras:
    transiciones[("q0", letra)] = "q3"
    transiciones[("q3", letra)] = "q3"

# Permitir letras + números (identificadores alfanuméricos)
for numero in numeros:
    transiciones[("q3", numero)] = "q3"

# Números → q9 (enteros)
for numero in numeros:
    transiciones[("q0", numero)] = "q9"
    transiciones[("q9", numero)] = "q9"
    transiciones[("q11", numero)] = "q11"

# Punto decimal
transiciones[("q9", ".")] = "q10"
# Números después del punto
for numero in numeros:
    transiciones[("q10", numero)] = "q11"

# Caracteres especiales
transiciones[("q0", "<")] = "q1"
transiciones[("q0", "?")] = "q2"
transiciones[("q0", "!")] = "q5"
transiciones[("q0", " ")] = "q6"
transiciones[("q0", "\t")] = "q7"
transiciones[("q0", "\n")] = "q8"
transiciones[("q0", '"')] = "q12"
transiciones[("q0", "=")] = "q13"
transiciones[("q0", "-")] = "q14"
transiciones[("q0", ">")] = "q15"
transiciones[("q0", "/")] = "q16"
transiciones[("q0", ":")] = "q17"
transiciones[("q0", ".")] = "q18"
transiciones[("q0", "'")] = "q19"

estado_inicial = "q0"
estados_finales = {"q1", "q2", "q4", "q5", "q6", "q7", "q8", "q9", "q11", "q12", "q13", "q14", "q15", "q16", "q17", "q18"}

# Leer entrada
with open("entrada.txt", "r", encoding="utf-8") as archivo:
    contenido = archivo.read()
    print(f"Procesando: {repr(contenido)}")
    procesar_cadena(contenido)
