import ply.lex as lex


class ForthLexer:
    tokens = (
        'NUMBER',
        'ADD',
        'SUB',
        'MUL',
        'DIV',
        'L_PAREN',
        'R_PAREN',
        'DUP',
        'DROP',
        'SWAP',
        'OVER',
        'COLON',
        'POP',
        'WORD',
        'FUNCTION',
        'EMIT',
        'CR',
        'SPACE',
        'NSPACES',
        'CHAR',
        'ENDLINE',
        'COMMENT',
        'CHARACTER',
        "QUOTES",
        "SUP",
        "INF",
        "IF",
        "THEN",
        "ELSE",
        "2DUP",
        "LETTER",
     )

    t_ADD = r'\+'
    t_SUB = r'\-'
    t_MUL = r'\*'
    t_DIV = r'\/'
    t_L_PAREN = r'\('
    t_R_PAREN = r'\)'
    t_DROP = r'DROP'
    t_OVER = r'OVER'
    t_COLON = r'\:'
    t_ENDLINE = r'\;'
    t_POP = r'\.'
    t_CR = r'CR'
    t_SPACE = r'SPACE'
    t_NSPACES = r'SPACES \d+'
    t_QUOTES = r'\"'
    t_SUP = r'>'
    t_INF = r'<'

    def t_EMIT(self, t):
        r'EMIT'
        return t

    def t_SWAP(self, t):
        r'(SWAP|swap)'
        return t

    def t_2DUP(self, t):
        r'2dup'
        return t

    def t_DUP(self, t):
        r'DUP'
        return t

    def t_IF(self, t):
        r'if'
        return t

    def t_THEN(self, t):
        r'then'
        return t

    def t_ELSE(self, t):
        r'else'
        return t

    def t_CHAR(self, t):
        "CHAR ."
        return t

    def t_COMMENT(self, t):
        r'--'
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_WORD(self, t):
        r'(?!(?:\bEMIT\b|\bCHAR\b|\bif\b|\bthen\b|\belse\b|\bSWAP\b|\bswap\b))[A-Za-z0-9]{2,}'
        return t

    def t_LETTER(self, t):
        r' [A-Za-z] '
        return t

    def t_CHARACTER(self, t):
        r'[^\w;:."+\-*/()<>]'
        return t

    states = (
        ('funcname', 'exclusive'),
    )

    def t_funcname_LPAREN(self, t):
        r'\('
        return t

    def t_funcname_RPAREN(self, t):
        r'\)'
        return t

    def t_FUNCTION(self, t):
        r'\:\s+'
        t.lexer.begin('funcname')

    def t_funcname_NAME(self, t):
        r'[A-Za-z0-9]+'
        t.type = 'FUNCTION'
        t.lexer.begin('INITIAL')
        return t

    def t_funcname_CODE(self, t):
        r'--'
        return t

    def t_funcname_WORD(self, t):
        r'\".\"'
        return

    t_funcname_ignore = ' \t'

    def t_funcname_error(self, t):
        t.lexer.skip(1)

    t_ignore = ' \t'

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


# analisdor léxico -> para identificar os tokens
# analisador sintático -> para identificar a estrutura do código
