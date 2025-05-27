#Obtiene el ultimo caracter de una cadena
def obtener_ultimo_caracter(cadena):
    if cadena:  # Verifica que la cadena no esté vacía
        return cadena[-1]
    else:
        return None  # O puedes lanzar una excepción si prefieres

#Obtiene el penultimo caracter de una cadena
def obtener_penultimo_caracter(cadena):
    if len(cadena) >= 2:
        return cadena[-2]
    else:
        return None  # O lanzar una excepción si prefieres

#Separa los últimos dos caracteres de una cadena
def separar_ultimos_dos(cadena):
    if len(cadena) >= 2:
        parte_principal = cadena[:-2]  # Todo menos los últimos dos
        return parte_principal
    else:
        return "", cadena  # Si la cadena tiene menos de 2 caracteres

#Separa el último caracter de una cadena
def separar_ultimo(cadena):
    if len(cadena) >= 2:
        parte_principal = cadena[:-1]  # Todo menos los últimos dos
        return parte_principal
    else:
        return "", cadena  # Si la cadena tiene menos de 2 caracteres

#Se procesa el archivo completo
def procesar_cadena(cadena):
    estado_actual = estado_inicial
    lexema_actual = ""
    i = 0
    while i < len(cadena):
        simbolo = cadena[i]
        #Si existe una transición
        if (estado_actual, simbolo) in transiciones:
            nuevo_estado = transiciones[(estado_actual, simbolo)]
            estado_actual = nuevo_estado
            lexema_actual += simbolo
            i += 1
            if estado_actual in estados_finales and estado_actual not in {"q3", "q9", "q11"}:
                lexer(estado_actual, lexema_actual)
                estado_actual = estado_inicial
                lexema_actual = ""

        #Si no existe transición
        else:
            if estado_actual == "q3":
                lexer("q4", lexema_actual)
            elif estado_actual == "q9":
                lexema_actual = lexema_actual + simbolo
                penultimo_caracter = obtener_penultimo_caracter(lexema_actual)
                if penultimo_caracter == ".":
                    primera_parte = separar_ultimos_dos(lexema_actual)
                    lexer("q9", primera_parte)
                    lexer("q18", penultimo_caracter)
                else:
                    primera_parte = separar_ultimo(lexema_actual)
                    lexer("q9", primera_parte)
            elif estado_actual == "q10":
                lexema_actual = lexema_actual + simbolo
                penultimo_caracter = obtener_penultimo_caracter(lexema_actual)
                primera_parte = separar_ultimos_dos(lexema_actual)
                lexer("q9", primera_parte)
                lexer("q18", penultimo_caracter)
            elif estado_actual == "q11":
                lexema_actual = lexema_actual + simbolo
                primera_parte = separar_ultimo(lexema_actual)
                lexer("q9", primera_parte)
            else:
                print(f"ERROR: Símbolo inválido '{simbolo}'")
                i += 1
            estado_actual = estado_inicial
            lexema_actual = ""
            continue

    # Al final, procesa el último lexema si quedó pendiente
    if estado_actual == "q3":
        lexer("q4", lexema_actual)
    elif estado_actual == "q9":
        lexema_actual = lexema_actual + simbolo
        penultimo_caracter = obtener_penultimo_caracter(lexema_actual)
        if penultimo_caracter == ".":
            primera_parte = separar_ultimos_dos(lexema_actual)
            lexer("q9", primera_parte)
            lexer("q18", penultimo_caracter)
        else:
            primera_parte = separar_ultimo(lexema_actual)
            lexer("q9", primera_parte)
    elif estado_actual == "q10":
        ultimo_caracter = obtener_ultimo_caracter(lexema_actual)
        primera_parte = separar_ultimo(lexema_actual)
        lexer("q9", primera_parte)
        lexer("q18", ultimo_caracter)
    elif estado_actual == "q11":
        lexema_actual = lexema_actual + simbolo
        primera_parte = separar_ultimo(lexema_actual)
        lexer("q9", primera_parte)
    print("Fin de archivo.")

# Se muestra el lexer y el tipo
def lexer(estado_final, lexema):
    if estado_final == "q1":
        print(f"LEXEMA: '{lexema}' → Tipo: MENOR_QUE")
    elif estado_final == "q2":
        print(f"LEXEMA: '{lexema}' → Tipo: PREGUNTA_FIN")
    elif estado_final == "q4":
        print(f"LEXEMA: '{lexema}' → Tipo: PALABRA")
    elif estado_final == "q5":
        print(f"LEXEMA: '{lexema}' → Tipo: EXCLAMACION_FIN")
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
        print(f"LEXEMA: '{lexema}' → Tipo: MAYOR_QUE")
    elif estado_final == "q16":
        print(f"LEXEMA: '{lexema}' → Tipo: SLASH")
    elif estado_final == "q17":
        print(f"LEXEMA: '{lexema}' → Tipo: DOS_PUNTOS")
    elif estado_final == "q18":
        print(f"LEXEMA: '{lexema}' → Tipo: PUNTO")
    elif estado_final == "q19":
        print(f"LEXEMA: '{lexema}' → Tipo: COMILLA_SIMPLE")
    elif estado_final == "q20":
        print(f"LEXEMA: '{lexema}' → Tipo: CORCHETE_INICIO")
    elif estado_final == "q21":
        print(f"LEXEMA: '{lexema}' → Tipo: PUNTO_COMA")
    elif estado_final == "q22":
        print(f"LEXEMA: '{lexema}' → Tipo: COMA")
    elif estado_final == "q23":
        print(f"LEXEMA: '{lexema}' → Tipo: CORCHETE_FIN")
    elif estado_final == "q24":
        print(f"LEXEMA: '{lexema}' → Tipo: NUMERAL")
    elif estado_final == "q25":
        print(f"LEXEMA: '{lexema}' → Tipo: AMPERSAND")
    elif estado_final == "q26":
        print(f"LEXEMA: '{lexema}' → Tipo: PORCENTAJE")
    elif estado_final == "q27":
        print(f"LEXEMA: '{lexema}' → Tipo: MAS")
    elif estado_final == "q28":
        print(f"LEXEMA: '{lexema}' → Tipo: ARROBA")
    elif estado_final == "q29":
        print(f"LEXEMA: '{lexema}' → Tipo: PIPE")
    elif estado_final == "q30":
        print(f"LEXEMA: '{lexema}' → Tipo: BACKSLASH")
    elif estado_final == "q31":
        print(f"LEXEMA: '{lexema}' → Tipo: CIRCUNFLEJO")
    elif estado_final == "q32":
        print(f"LEXEMA: '{lexema}' → Tipo: TILDE")
    elif estado_final == "q33":
        print(f"LEXEMA: '{lexema}' → Tipo: DOLAR")
    elif estado_final == "q34":
        print(f"LEXEMA: '{lexema}' → Tipo: PARENTESIS_INICIO")
    elif estado_final == "q35":
        print(f"LEXEMA: '{lexema}' → Tipo: PARENTESIS_FIN")
    elif estado_final == "q36":
        print(f"LEXEMA: '{lexema}' → Tipo: CORCHETE_RECT_INICIO")
    elif estado_final == "q37":
        print(f"LEXEMA: '{lexema}' → Tipo: CORCHETE_RECT_FIN")
    elif estado_final == "q38":
        print(f"LEXEMA: '{lexema}' → Tipo: GUION_BAJO")
    elif estado_final == "q39":
        print(f"LEXEMA: '{lexema}' → Tipo: ASTERISCO")
    elif estado_final == "q40":
        print(f"LEXEMA: '{lexema}' → Tipo: PREGUNTA_INICIO")
    elif estado_final == "q41":
        print(f"LEXEMA: '{lexema}' → Tipo: EXCLAMACION_INICIO")
    else:
        print(f"LEXEMA: '{lexema}' → Tipo: ERROR")

# Autómata
estados = {"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9",
           "q10", "q11", "q12", "q13", "q14", "q15", "q16", "q17", "q18",
           "q19", "q20", "q21", "q22", "q23", "q24", "q25", "q26", "q27",
           "q28", "q29", "q30","q31", "q32", "q33", "q34", "q35", "q36",
           "q37", "q38", "q39", "q40", "q41"}
letras = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚ"
          "üÜñÑ")
numeros = "0123456789"
transiciones = {}

# Letras → q3
for letra in letras:
    transiciones[("q0", letra)] = "q3"
    transiciones[("q3", letra)] = "q3"

# Números
for numero in numeros:
    transiciones[("q0", numero)] = "q9"
    transiciones[("q9", numero)] = "q9"
    transiciones[("q10", numero)] = "q11"
    transiciones[("q11", numero)] = "q11"

# Punto decimal
transiciones[("q9", ".")] = "q10"

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
transiciones[("q0", "{")] = "q20"
transiciones[("q0", ";")] = "q21"
transiciones[("q0", ",")] = "q22"
transiciones[("q0", "}")] = "q23"
transiciones[("q0", "#")] = "q24"
transiciones[("q0", "&")] = "q25"
transiciones[("q0", "%")] = "q26"
transiciones[("q0", "+")] = "q27"
transiciones[("q0", "@")] = "q28"
transiciones[("q0", "|")] = "q29"
transiciones[("q0", "\\")] = "q30"
transiciones[("q0", "^")] = "q31"
transiciones[("q0", "´")] = "q32"
transiciones[("q0", "$")] = "q33"
transiciones[("q0", "(")] = "q34"
transiciones[("q0", ")")] = "q35"
transiciones[("q0", "[")] = "q36"
transiciones[("q0", "]")] = "q37"
transiciones[("q0", "_")] = "q38"
transiciones[("q0", "*")] = "q39"
transiciones[("q0", "¿")] = "q40"
transiciones[("q0", "¡")] = "q41"

estado_inicial = "q0"
estados_finales = {"q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9",
                   "q11", "q12", "q13", "q14", "q15", "q16", "q17", "q18",
                   "q19", "q20", "q21", "q22", "q23", "q24", "q25", "q26",
                   "q27", "q28", "q29", "q30","q31", "q32", "q33", "q34",
                   "q35", "q36", "q37", "q38", "q39", "q40", "q41"}

# Leer archivo
with open("entrada.txt", "r", encoding="utf-8") as archivo:
    contenido = archivo.read()
    print(f"Procesando: {repr(contenido)}")
    procesar_cadena(contenido)