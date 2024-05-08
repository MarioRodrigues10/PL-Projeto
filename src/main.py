import forth_grammar as forth_grammar
import forth_syntax as forth_syntax
import forth_lexer as forth_lex
import utils as utils
import sys


def main():
    forth_l = forth_lex.ForthLexer()
    forthGrammar = forth_grammar.ForthGrammar()
    forthParser = forth_syntax.ForthSyntax()
    forth_l.build()

    lines = utils.treat_inputs(sys.stdin.readlines())
    for line in lines:
        data = line.strip()
        text = forth_l.test(data)

        # print("Data: ", data)
        # print("Text: ", text)
        result = forthParser.parser.parse(data)
        # print("Result: ", result)
        if result == None:
            print("Syntax error in the input")
        else:
            gramatica = forth_grammar.create_grammar(
                forth_l, text, forthGrammar)
            for value in gramatica:
                print(value)


if __name__ == "__main__":
    main()
