import ply.lex as lex


class ForthLexer:
    # List of token names
    tokens = (
        'NUMBER',
        'PLUS',
        'POP',
        'SUB',
        'MUL',
        'DIV',
        'EQUALS'
    )

    t_PLUS = r'\+'
    t_POP = r'\.'
    t_SUB = r'\-'
    t_MUL = r'\*'
    t_DIV = r'\/'
    t_EQUALS = r'\='

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    t_ignore = ' \t\n'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.lexer.input(data)
        list_toks = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            list_toks.append(tok)
        return list_toks
