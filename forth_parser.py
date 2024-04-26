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
        'EQUALS',
        'FUNCTION',
        'CHAR',
        'DUP',
        'CR',
        'SPACE',
        'NSPACES',
        'EMIT',
        'WORD'
    )

    t_PLUS = r'\+'
    t_POP = r'\.'
    t_SUB = r'\-'
    t_MUL = r'\*'
    t_DIV = r'\/'
    t_EQUALS = r'\='
    t_CHAR = r'CHAR\s.'
    t_DUP = r'DUP'
    t_EMIT = r'EMIT'
    t_CR = r'CR'
    t_SPACE = r'SPACE'
    t_NSPACES = r'SPACES \d+'

    def t_WORD(self, t):
        r'(?!(?:\bEMIT\b|\bCHAR\b|\bDUP\b))[A-Za-z]+'
        return t
    states = (
        ('funcname', 'exclusive'),
    )

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_FUNCTION(self, t):
        r'\:\s+'
        t.lexer.begin('funcname')

    def t_funcname_NAME(self, t):
        r'[A-Za-z]+'
        t.type = 'FUNCTION'
        t.lexer.begin('INITIAL')
        return t

    def t_funcname_LPAREN(self, t):
        r'\('
        return t

    def t_funcname_RPAREN(self, t):
        r'\)'
        return t

    def t_funcname_CODE(self, t):
        r'--'
        return t

    def t_funcname_SEMICOLON(self, t):
        r';'
        return t

    def t_funcname_WORD(self, t):
        r'\".\"'
        return t

    t_ignore = ' \t\n'

    # Error handling rule
    def t_error(self, t):
        # print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def t_funcname_error(self, t):
        t.lexer.skip(1)

    t_funcname_ignore = ' \t\n'

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
