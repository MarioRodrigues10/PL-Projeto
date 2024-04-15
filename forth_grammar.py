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
