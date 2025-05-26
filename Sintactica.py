import re

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"{self.tipo}({self.valor})"

def lexer(texto):
    tokens = []
    pos = 0
    longitud = len(texto)
    dentro_etiqueta = False

    while pos < longitud:
        c = texto[pos]

        if not dentro_etiqueta:
            if c == '<':
                if texto.startswith('<!--', pos):
                    fin_coment = texto.find('-->', pos + 4)
                    if fin_coment == -1:
                        raise SyntaxError("Comentario no cerrado")
                    comentario = texto[pos:fin_coment+3]
                    tokens.append(Token("COMENTARIO", comentario))
                    pos = fin_coment + 3
                    continue
                elif texto.startswith('<?', pos):
                    fin_instr = texto.find('?>', pos + 2)
                    if fin_instr == -1:
                        raise SyntaxError("Instrucción XML no cerrada")
                    instruccion = texto[pos:fin_instr+2]
                    tokens.append(Token("INSTRUCCION", instruccion))
                    pos = fin_instr + 2
                    continue
                elif texto.startswith('<!', pos):
                    fin_decl = texto.find('>', pos + 2)
                    if fin_decl == -1:
                        raise SyntaxError("Declaración <! no cerrada")
                    declaracion = texto[pos:fin_decl+1]
                    tokens.append(Token("DECLARACION", declaracion))
                    pos = fin_decl + 1
                    continue
                else:
                    tokens.append(Token("MENOR", "<"))
                    pos += 1
                    dentro_etiqueta = True
            else:
                inicio = pos
                while pos < longitud and texto[pos] != '<':
                    pos += 1
                valor = texto[inicio:pos]
                if valor.strip() != "":
                    tokens.append(Token("TEXTO", valor))
        else:
            # Dentro de etiqueta
            if c.isspace():
                pos += 1
                continue
            if c == '>':
                tokens.append(Token("MAYOR", ">"))
                pos += 1
                dentro_etiqueta = False
            elif c == '/':
                tokens.append(Token("SLASH", "/"))
                pos += 1
            elif c == '=':
                tokens.append(Token("IGUAL", "="))
                pos += 1
            elif c == '"':
                # Capturar todo el valor del atributo hasta la siguiente comilla
                pos += 1
                inicio_valor = pos
                fin_valor = texto.find('"', inicio_valor)
                if fin_valor == -1:
                    raise SyntaxError("Valor de atributo sin cerrar con comilla")
                valor = texto[inicio_valor:fin_valor]
                tokens.append(Token("VALOR", valor))
                pos = fin_valor + 1
            else:
                inicio = pos
                while pos < longitud and re.match(r'[a-zA-Z0-9_:.-]', texto[pos]):
                    pos += 1
                valor = texto[inicio:pos]
                if valor == "":
                    raise SyntaxError(f"Token inesperado: '{texto[pos]}'")
                tokens.append(Token("NOMBRE", valor))
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.preanalisis = self.tokens[0] if self.tokens else Token("EOF", "")

    def avanzar(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.preanalisis = self.tokens[self.pos]
        else:
            self.preanalisis = Token("EOF", "")

    def comer(self, tipo_esperado):
        # Saltar TEXTO con solo espacios
        while self.preanalisis.tipo == "TEXTO" and self.preanalisis.valor.strip() == "":
            self.avanzar()
        if self.preanalisis.tipo == tipo_esperado:
            valor = self.preanalisis.valor
            self.avanzar()
            return Token(tipo_esperado, valor)
        raise SyntaxError(f"Se esperaba {tipo_esperado}, pero se encontró {self.preanalisis.tipo} ('{self.preanalisis.valor}')")

    def parsear_documento(self):
        print("Tokens:", self.tokens)
        print("Validando documento...")
        while self.preanalisis.tipo != "EOF":
            # Ignorar tokens no estructurales
            if self.preanalisis.tipo in ("INSTRUCCION", "COMENTARIO", "DECLARACION"):
                self.avanzar()
            else:
                self.parsear_elemento()
        print("Documento XML válido.")

    def parsear_elemento(self):
        self.comer('MENOR')
        nombre_etiqueta = self.comer('NOMBRE').valor
        self.parsear_atributos()
        if self.preanalisis.tipo == 'SLASH':
            self.comer('SLASH')
            self.comer('MAYOR')
            return
        self.comer('MAYOR')

        while True:
            # Ignorar comentarios, instrucciones y declaraciones dentro del contenido
            while self.preanalisis.tipo in ("COMENTARIO", "INSTRUCCION", "DECLARACION"):
                self.avanzar()

            if self.preanalisis.tipo == 'TEXTO' and self.preanalisis.valor.strip() == '':
                self.avanzar()
                continue

            if self.preanalisis.tipo == 'MENOR':
                if self.analizar_posible_cierre(nombre_etiqueta):
                    break
                else:
                    self.parsear_elemento()
            elif self.preanalisis.tipo == 'TEXTO':
                self.comer('TEXTO')
            else:
                break

        self.comer('MENOR')
        self.comer('SLASH')
        nombre_cierre = self.comer('NOMBRE').valor
        if nombre_cierre != nombre_etiqueta:
            raise SyntaxError(f"Etiqueta de cierre incorrecta: esperaba </{nombre_etiqueta}> pero se encontró </{nombre_cierre}>")
        self.comer('MAYOR')


    def analizar_posible_cierre(self, etiqueta_abierta):
        if (self.preanalisis.tipo == 'MENOR' and
            self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].tipo == 'SLASH' and
            self.pos + 2 < len(self.tokens) and self.tokens[self.pos + 2].tipo == 'NOMBRE' and
            self.tokens[self.pos + 2].valor == etiqueta_abierta):
            return True
        return False

    def parsear_atributos(self):
        while self.preanalisis.tipo == "NOMBRE":
            self.comer("NOMBRE")
            self.comer("IGUAL")
            valor = self.comer("VALOR")  # ahora esperamos VALOR completo, no NOMBRE o TEXTO


if __name__ == "__main__":
    try:
        with open("entrada.txt", "r", encoding="utf-8") as f:
            texto = f.read()
        if texto.strip() == "":
            print("El archivo está vacío o contiene solo espacios en blanco. No hay texto para analizar.")
        else:
            tokens = lexer(texto)
            parser = Parser(tokens)
            try:
                parser.parsear_documento()
            except SyntaxError as e:
                print(f"ERROR SINTÁCTICO: {e}")
    except FileNotFoundError:
        print("El archivo 'entrada.txt' no fue encontrado.")
