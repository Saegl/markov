from lark.visitors import Interpreter
import liatypes as lt


class FuncMatcher:
    def __init__(self, params) -> None:
        self.params = params


class LiaInterpreter(Interpreter):
    IDENT = str
    NUMBER = int

    def __init__(self):
        self.mem = {
            'print': lt.BuiltInFunction(print)
        }

    def start(self, tree):
        for stmt in tree.children:
            self.visit(stmt)
    
    def name(self, tree):
        return str(tree.children[0])
    
    def funcdef(self, tree):
        name, params, body = tree.children
        name = self.visit(name)
        params = self.visit(params)

        if name not in self.mem:
            self.mem[name] = lt.LiaMultiFunction()
        
        self.mem[name].add_impl(tuple(params), body)
    
    def params(self, tree):
        return [self.visit(param) for param in tree.children]

    def assign(self, tree):
        name, expr = [self.visit(x) for x in tree.children]
        self.mem[name] = expr
        return expr
    
    def args(self, tree):
        return [self.visit(param) for param in tree.children]
    

    ############ BINDEF
    def bindef(self, tree):
        lhs, op, rhs, expr = tree.children
        lhs, op, rhs = [self.visit(x) for x in [lhs, op, rhs]]
        print("BINDEF", lhs, op, rhs)
    
    def binop(self, tree):
        return str(tree.children[0])
    
    def func_match(self, tree):
        name, params = [self.visit(x) for x in tree.children]
        print('fm', name, params)
        return 0

    ############ TYPEDEF
    def typedef(self, tree):
        name, top_type_tree = [self.visit(x) for x in tree.children]
        top_type_tree.set_name(name)
        self.mem[name] = top_type_tree
    
    def product_type(self, tree):
        assert len(tree.children) == 1
        params = self.visit(tree.children[0])
        return lt.ProductType(params)

    def sum_type(self, tree):
        assert len(tree.children) == 1
        params = self.visit(tree.children[0])
        return lt.SumType(params)
    
    def separated(self, tree):
        return [self.visit(x) for x in tree.children]

    ############ EXPR
    def funccall(self, tree):
        name, args = [self.visit(x) for x in tree.children]
        func = self.mem[name]
        return func.call(self, args)

    def add(self, tree):
        a, b = [self.visit(x) for x in tree.children]
        return a + b
    
    def sub(self, tree):
        a, b = [self.visit(x) for x in tree.children]
        return a - b
    
    def mul(self, tree):
        a, b = [self.visit(x) for x in tree.children]
        return a * b
    
    def div(self, tree):
        a, b = [self.visit(x) for x in tree.children]
        return a // b

    def number(self, tree):
        return int(tree.children[0])

    def string(self, tree):
        escaped_string = tree.children[0]
        inner_string = escaped_string[1:-1]
        return inner_string
    
    def namecall(self, tree):
        varname = str(tree.children[0])
        return self.mem[varname]

    def set(self, tree):
        values = self.visit(tree.children[0])
        return set(values)
