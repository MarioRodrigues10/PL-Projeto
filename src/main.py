import forth_grammar as forth_grammar
import forth_syntax as forth_syntax
import forth_lexer as forth_lex
import sys

def extract_text(lines):
    extracted_text = ""
    list = []
    bool = False
    for line in lines:
        if (line.startswith(":") or bool == True) and not ";" in line:
            extracted_text += line
            print(extracted_text)
            bool = True
        elif ";" in line and bool == True:
            extracted_text += line
            bool = False
            new_text = extracted_text
            list.append(new_text)
            extracted_text = ""
            
        else:
            list.append(line) 
            
    return list
   
def main():
    forth_l = forth_lex.ForthLexer()
    forthGrammar = forth_grammar.ForthGrammar()
    forthParser = forth_syntax.ForthSyntax()
    forth_l.build()

    lines = sys.stdin.readlines()
    lines = extract_text(lines)
    for line in lines:
        data = line.strip()
        print("Data: ", data)
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
