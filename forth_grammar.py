import re
import forth_parser
class ForthGrammar:
    def __init__(self) -> None:
        pass

    def forth_push(self, value):
        return f'pushi {value}'

    def forth_add(self):
        return 'add'

    def forth_sub(self):
        return 'sub'

    def forth_pop(self):
        return 'writei'

    def forth_mul(self):
        return 'mul'

    def forth_equals(self):
        return 'eq'

    def forth_div(self):
        return 'div'
    
    def forth_function(self, forth_lexer, value):
        match = re.match(r'\:\s([A-Za-z]+)\s\((\s[A-Za-z]+\s[A-Za-z]\s--\s([A-Za-z]+)\s\))\s(.+)\;$', value)
        print(match.group(3))
        if match:
            text = forth_lexer.test(match.group(4))
            create_grammar(forth_lexer, text)
        return value
    
    def forth_char(self, value):
        return f'pushi {ord(value)}'


def create_grammar(forth_lexer, text):
    forthGrammar = ForthGrammar()
    for i in text:
        if i.type == 'NUMBER':
            value = forthGrammar.forth_push(i.value)
            print(value)
        elif i.type == 'PLUS':
            value = forthGrammar.forth_add()
            print(value)
        elif i.type == 'POP':
            value = forthGrammar.forth_pop()
            print(value)
        elif i.type == 'SUB':
            value = forthGrammar.forth_sub()
            print(value)
        elif i.type == 'MUL':
            value = forthGrammar.forth_mul()
            print(value)
        elif i.type == 'EQUALS':
            value = forthGrammar.forth_equals()
            print(value)
        elif i.type == 'DIV':
            value = forthGrammar.forth_div()
            print(value)
        elif i.type == 'FUNCTION':
            print(i.value)
            value = forthGrammar.forth_function(forth_lexer, i.value)
            print(value)
        elif i.type == 'CHAR':
            i.value = i.value[5:]
            value = forthGrammar.forth_char(i.value)
            print(value)
        else:
            pass
