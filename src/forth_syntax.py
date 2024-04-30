import ply.yacc as yacc
import forth_state as state


class ForthSyntax:
    def __init__(self):
        self.tokens = (
            'NUMBER',
            'ADD',
            'SUB',
            'MUL',
            'EQUALS',
            'DIV',
            'L_PAREN',
            'R_PAREN',
            'DUP',
            'SWAP',
            'POP',
            'WORD',
            'FUNCTION',
            'EMIT',
            'CR',
            'SPACE',
            'NSPACES',
            'CHAR',
            'ENDLINE',
            'COMMENT'
        )
        self.parser = yacc.yacc(module=self)
        self.forth_state = state.ForthState()

    def p_statement(self, p):
        """
        statement : expression
                  | function_definition
        """
        p[0] = p[1]

    def p_expression(self, p):
        """
        expression : NUMBER
                | expression NUMBER
                | expression operator
                | expression FUNCTION
                | expression WORD
                | expression char_definition
        """
        if isinstance(p[1], int) or (isinstance(p[1], tuple) and p[1][0] == 'expression' and isinstance(p[1][1], int)):
            self.forth_state.elementsStack += 1
        p[0] = ('expression', *p[1:])

    def p_operator(self, p):
        """
        operator : ADD
                 | SUB
                 | MUL
                 | DIV
                 | EQUALS
                 | POP
                 | DUP
                 | EMIT
                 | CR
                 | SPACE
                 | NSPACES
                 | L_PAREN
                 | R_PAREN
                 | SWAP
        """
        if p[1] == '(':
            self.forth_state.parentes += 1
        elif p[1] == ')':
            if self.forth_state.parentes == 0:
                raise SyntaxError("Unmatched right parenthesis")
            else:
                self.forth_state.parentes -= 1

        if p[1] in ['+', '-', '*', '/', '=', 'SWAP'] and self.forth_state.elementsStack < 2:
            raise SyntaxError(
                "Not enough elements in the stack for the operation")
        elif p[1] in ['DUP', 'EMIT'] and self.forth_state.elementsStack < 1:
            raise SyntaxError(
                "Not enough elements in the stack for the operation")
        else:
            p[0] = ('operator', p[1])

    def p_char(self, p):
        """
        char_definition : CHAR char_op
        """
        p[0] = ('CHAR', p[2])

    def p_char_op(self, p):
        """
        char_op : operator
                | operator char_op
        """
        p[0] = p[1]

    def p_function_definition(self, p):
        """
        function_definition : FUNCTION L_PAREN function_args COMMENT WORD R_PAREN function_expression ENDLINE
        """
        p[0] = ('function_definition', p[3], p[6])

    def p_function_args(self, p):
        """
        function_args : WORD
                      | function_args WORD 
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_function_expression(self, p):
        """
        function_expression : function_operator
                            | NUMBER
                            | function_expression function_operator
                            | function_expression NUMBER
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1]

    def p_function_operator(self, p):
        """
        function_operator : ADD
                            | SUB
                            | MUL
                            | DIV
                            | EQUALS
                            | POP
                            | DUP
                            | EMIT
                            | CR
                            | SPACE
                            | NSPACES
                            | L_PAREN
                            | R_PAREN
                            | SWAP
        """
        p[0] = p[1]

    def p_error(self, p):
        raise SyntaxError("Syntax error")

    def parse(self, data):
        try:
            return self.parser.parse(data)
        except SyntaxError:
            return None
