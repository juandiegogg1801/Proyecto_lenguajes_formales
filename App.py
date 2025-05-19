def procesar_cadena(cadena):
    estado_actual = estado_inicial
    lexema_actual = ""
    i = 0
    while i < len(cadena):
        simbolo = cadena[i]

        if (estado_actual, simbolo) in transiciones:
            nuevo_estado = transiciones[(estado_actual, simbolo)]

            # Si pasamos de q3 a un estado final por un símbolo NO letra, debemos procesar palabra antes
            if estado_actual == "q3" and nuevo_estado != "q3":
                lexer("q4", lexema_actual)
                lexema_actual = ""
                estado_actual = estado_inicial
                # No consumas el símbolo aún, vuelve a analizarlo
                continue

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
                continue  # no avanzamos i, se reanaliza el mismo símbolo
            else:
                if lexema_actual:
                    print(f"ERROR: Secuencia inválida '{lexema_actual + simbolo}'")
                    lexema_actual = ""
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
    else:
        print(f"LEXEMA: '{lexema}' → Tipo: ERROR")


# Autómata
estados = {"q0", "q1", "q2", "q3", "q4", "q5"}
letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
transiciones = {}

# Letras → q3
for letra in letras:
    transiciones[("q0", letra)] = "q3"
    transiciones[("q3", letra)] = "q3"

# Simbolos individuales
transiciones[("q0", "<")] = "q1"
transiciones[("q0", "?")] = "q2"
transiciones[("q0", "!")] = "q5"

estado_inicial = "q0"
estados_finales = {"q1", "q2", "q4", "q5"}

# Leer entrada
with open("entrada.txt", "r", encoding="utf-8") as archivo:
    contenido = archivo.read().strip()
    print(f"Procesando: {contenido}")
    procesar_cadena(contenido)
