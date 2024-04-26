import forth_grammar as forth_grammar
import forth_parser as forth_parser
import sys


def main():
    forth_lexer = forth_parser.ForthLexer()
    forth_lexer.build()

    lines = sys.stdin.readlines()
    for line in lines:
        data = line.strip()
        text = forth_lexer.test(data)
        forthGrammar = forth_grammar.ForthGrammar()
        values = forth_grammar.create_grammar(forth_lexer, text, forthGrammar)
        for value in values:
            print(value)


if __name__ == "__main__":
    main()
