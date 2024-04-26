import forth_parser

reservedFunctions = {}
reservedWords = {}


class ForthGrammar:
    def __init__(self) -> None:
        self.reservedFunctions = {}
        pass

    def forth_push(self, value):
        return f'pushi {value}'

    def forth_add(self):
        return 'add'

    def forth_sub(self):
        return 'sub'

    def forth_pop(self):
        return 'pop 1'

    def forth_mul(self):
        return 'mul'

    def forth_equals(self):
        return 'eq'

    def forth_div(self):
        return 'div'

    def forth_function(self, value):
        operations = []
        name = ""
        for i in value:
            if i.type == 'FUNCTION':
                name = i.value
            else:
                operations.append(create_grammar(
                    forth_parser.ForthLexer(), [i], self))
        operations = [item for sublist in operations for item in sublist]
        operations = operations[2:]
        self.reservedFunctions = self.reservedFunctions.update(
            {name: operations})
        return {name: operations}

    def forth_string(self, value):
        string = ""
        flag = False
        name = value[0].value
        for i in value:
            if flag:
                string += i.value
            if i.type == 'POP':
                flag = True
        return {name: string}

    def forth_char(self, value):
        return f'pushi {ord(value)}'

    def forth_cr(self):
        return 'pushs "\\n"'

    def forth_space(self):
        return 'pushs " "'

    def forth_nspaces(self, value):
        return f'pushs {" " * int(value)}'

    def forth_dup(self):
        return 'dup 1'

    def forth_emit(self):
        return 'writechr'


def create_grammar(forth_lexer, text, forthGrammar=ForthGrammar()):
    values = []
    if (len(text) == 0):
        return values
    if text[0].type == 'FUNCTION' and len(text) > 1 and text[1].type != 'POP':
        value = forthGrammar.forth_function(text)
        reservedFunctions.update(value)
    elif text[0].type == 'FUNCTION' and len(text) > 1 and text[1].type == 'POP':
        value = forthGrammar.forth_string(text)
        reservedWords.update(value)
    else:
        for i in text:
            if i.type == 'NUMBER':
                value = forthGrammar.forth_push(i.value)
                values.append(value)
            elif i.type == 'WORD':
                if i.value in reservedFunctions:
                    value = reservedFunctions.get(i.value)
                    for i in value:
                        values.append(i)
                elif i.value in reservedWords:
                    value = reservedWords.get(i.value)
                    string = f'pushs "{value}"'
                    values.append(string)
            elif i.type == 'PLUS':
                value = forthGrammar.forth_add()
                values.append(value)
            elif i.type == 'POP':
                value = forthGrammar.forth_pop()
                values.append(value)
            elif i.type == 'SUB':
                value = forthGrammar.forth_sub()
                values.append(value)
            elif i.type == 'MUL':
                value = forthGrammar.forth_mul()
                values.append(value)
            elif i.type == 'EQUALS':
                value = forthGrammar.forth_equals()
                values.append(value)
            elif i.type == 'DIV':
                value = forthGrammar.forth_div()
                values.append(value)
            elif i.type == 'FUNCTION':
                value = forthGrammar.forth_function(forth_lexer, i.value)
                values.append(value)
            elif i.type == 'CHAR':
                i.value = i.value[5:]
                value = forthGrammar.forth_char(i.value)
                values.append(value)
            elif i.type == 'SPECIAL_FUNCTION':
                valuesdefault = i.value.split()
                for j in valuesdefault:
                    text2 = forth_lexer.test(j)
                    text.append(create_grammar(forth_lexer, text2))
            elif i.type == 'CR':
                value = forthGrammar.forth_cr()
                values.append(value)
            elif i.type == 'SPACE':
                value = forthGrammar.forth_space()
                values.append(value)
            elif i.type == 'NSPACES':
                value = forthGrammar.forth_nspaces(i.value[7:])
                values.append(value)
            elif i.type == 'DUP':
                value = forthGrammar.forth_dup()
                values.append(value)
            elif i.type == 'EMIT':
                value = forthGrammar.forth_emit()
                values.append(value)
            else:
                pass
    return values
