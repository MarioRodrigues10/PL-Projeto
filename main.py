import forth_grammar as forth_grammar
import forth_parser as forth_parser
import sys


def main():
    forth_lexer = forth_parser.ForthLexer()
    forthGrammar = forth_grammar.ForthGrammar()
    forth_lexer.build()

    lines = sys.stdin.readlines()
    for line in lines:
        data = line.strip()
        abc = forth_lexer.test(data)
        for i in abc:
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


if __name__ == "__main__":
    main()
