import forth_lexer as forth_lexer

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
        for i in value:
            value = create_grammar(forth_lexer.ForthLexer(), [i], self)
            operations.append(value)
        operations = [item for sublist in operations for item in sublist]
        return operations

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

    def forth_2dup(self):
        return "pushsp", "load -1"


def create_grammar(forth_lexer, text, forthGrammar=ForthGrammar()):
    values = []
    if_statement = False
    if len(text) == 0:
        return values
    if text[0].type == 'FUNCTION' and len(text) > 1 and text[1].type != 'POP':
        function_name = text[0].value
        r_paren_pos = -1
        for i in range(len(text)):
            if text[i].type == 'R_PAREN':
                r_paren_pos = i
                break
            elif text[i].type == 'IF':
                if_statement = True
        text = text[r_paren_pos+1:]
        value = forthGrammar.forth_function(text)
        if if_statement:
            pos = 0
            value.append('endif0:')
            while value[pos] != 'jz endif0':
                value.append(value[pos])
                pos += 1
        reservedFunctions.update({function_name: value})
    elif text[0].type == 'FUNCTION' and len(text) > 1 and text[1].type == 'POP':
        value = forthGrammar.forth_string(text)
        reservedWords.update(value)
    else:
        for i in text:
            match i.type:
                case 'NUMBER':
                    value = forthGrammar.forth_push(i.value)
                    values.append(value)
                case 'WORD':
                    if i.value in reservedFunctions:
                        value = reservedFunctions.get(i.value)
                        for i in value:
                            values.append(i)
                    elif i.value in reservedWords:
                        value = reservedWords.get(i.value)
                        string = f'pushs {value}'
                        values.append(string)
                case 'ADD':
                    value = forthGrammar.forth_add()
                    values.append(value)
                case 'POP':
                    value = forthGrammar.forth_pop()
                    values.append(value)
                case 'SUB':
                    value = forthGrammar.forth_sub()
                    values.append(value)
                case 'MUL':
                    value = forthGrammar.forth_mul()
                    values.append(value)
                case 'EQUALS':
                    value = forthGrammar.forth_equals()
                    values.append(value)
                case 'DIV':
                    value = forthGrammar.forth_div()
                    values.append(value)
                case 'CHAR':
                    i.value = i.value[5:]
                    value = forthGrammar.forth_char(i.value)
                    values.append(value)
                case 'CR':
                    value = forthGrammar.forth_cr()
                    values.append(value)
                case 'SPACE':
                    value = forthGrammar.forth_space()
                    values.append(value)
                case 'NSPACES':
                    value = forthGrammar.forth_nspaces(i.value[7:])
                    values.append(value)
                case 'DUP':
                    value = forthGrammar.forth_dup()
                    values.append(value)
                case 'EMIT':
                    value = forthGrammar.forth_emit()
                    values.append(value)
                case '2DUP':
                    (value1, value2) = forthGrammar.forth_2dup()
                    values.append(value1)
                    values.append(value2)
                    values.append(value1)
                    values.append(value2)
                case 'SWAP':
                    values.append("swap")
                case 'INF':
                    values.append("inf")
                case 'SUP':
                    values.append("sup")
                case 'IF':
                    values.append("jz endif0")
                case _:
                    pass
    return values


# input (forth) -> analisador léxico -> analisador sintático -> (output)
