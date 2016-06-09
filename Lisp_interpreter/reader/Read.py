import DirPaths
from sys import stdin, stdout
from Parser import parse
from ParserError import ParserError
from Global_Scope import foo
from Reader import Reader
from retic import Void, Bool, List, String, Dyn
# from reader.p_expr import P_Expr


#If this class is in a different file, there'd be a bug.
class P_Expr:
    """
    Represents a union type p-expr
    """
    def __init__(self, expr):
        """
        :param p_expr: List of string or None
        :return: None
        """
        self.expr = expr

class No_Expr(P_Expr):
    def __init__(self, expr:Void):
        super().__init__(expr)

class False_Expr(P_Expr):
    def __init__(self, expr:Bool):
        super().__init__(expr)

class Expr(P_Expr):
    def __init__(self, expr:List(String)):
        super().__init__(expr)



class Line:
    """
    To represent the read line or False if no line was read
    """
    def __init__(self, line):
        """
        :param line: [String, ...] or False
        """
        self.line = line



def read_eval_print_loop()->Void:
    """
    read S-expression, parse and evaluate, print, REPEAT
    :return: None
    """
    global_s = foo

    while True:

        try:
            p_expr = read().expr
            if p_expr == False:
                break
            elif not p_expr:
                continue
            ast = parse(p_expr)
            [the_value, s] = ast.eval(global_s.getter())
            global_s.setter(s)
            if the_value:
                print (str(the_value))
        except ParserError:
            print('bla bla bla')


def read()->P_Expr:
    """
    Reads a line from the IP and instantiates a Reader using the IP
    and returns the resulting p-expression
    :return: p_expr
    """
    try:
        ip = read_lines().line
        if not ip:
            return False_Expr(False)
        r = Reader(ip)
        p_expr = r.reader()
        return Expr(p_expr)

    except:
        return No_Expr(None)


def read_lines()->Dyn:
    """
    Reads lines from std input
    :return: List containing input seperated by space
    """
    input_list = []
    stdout.write("> ")
    stdout.flush()

    while True:
        try:
            userinput = input()
            input_list.append(userinput)
            all_input = ' '.join(input_list)
            if has_equal_parens(all_input):
                return Line(all_input)

        except (EOFError):
            return Line(None)


def has_equal_parens(line:String)->Bool:
    """
    Returns True if number of right parens is equal to the number of left parens, and returns False otherwise
    :param line: String
    :return: Bool
    """
    left = 0
    right = 0
    for char in line:
        if char == '(':
            left +=1
        elif char == ')':
            right +=1

    return right == left

print("Zeina's BSL intepreter, v.06\n")
read_eval_print_loop()
