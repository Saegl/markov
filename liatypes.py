class LiaVal:
    pass


class ProductVal(LiaVal):
    def __init__(self, type_, vals):
        self.type_ = type_
        self.vals = vals

    def __repr__(self) -> str:
        vals = ", ".join(str(val) for val in self.vals)
        return f"{self.type_.name}({vals})"

class LiaType:
    def __init__(self) -> None:
        pass


class ProductType(LiaType):
    def __init__(self, params) -> None:
        self.params = params
        self.name = 'Unnamed'
    
    def set_name(self, name):
        self.name = name
    
    def __repr__(self) -> str:
        params = ", ".join([str(param) for param in self.params])
        return f"({params})"
    
    def call(self, interp, args):
        assert len(args) == len(self.params)
        return ProductVal(self, args)


class SumType(LiaType):
    def __init__(self, params) -> None:
        self.params = params
        self.name = 'Unnamed'

    def set_name(self, name):
        self.name = name
    
    def __repr__(self) -> str:
        params = ", ".join([str(param) for param in self.params])
        return "{" + f"{params}" + "}"
    
    def call(self, interp, args):
        return args


class BuiltInFunction:
    def __init__(self, fn):
        self.fn = fn

    def call(self, interp, args):
        self.fn(*args)

class LiaMultiFunction:
    def __init__(self):
        self.data = {} # params: body

    def is_match(self, params, args):
        for param, arg in zip(params, args):
            if isinstance(param, str):
                continue
            else:
                if param != arg:
                    return False
        
        return True
    
    def get_impl(self, args):
        for params, body in self.data.items():
            if self.is_match(params, args):
                namespace = dict(zip(params, args))
                return namespace, body
        raise ValueError("Change this exception")

    def add_impl(self, params, body):
        self.data[params] = body
    
    def call(self, interp, args):
        namespace, body = self.get_impl(args)

        LiaInterpreter = type(interp)
        subinterpreter = LiaInterpreter()
        subinterpreter.mem = interp.mem | namespace
        return subinterpreter.visit(body)
    
    def __repr__(self):
        output = []
        for params, body in self.data.items():
            output.append(f"{params} <=> (something)")
        return "\n".join(output)
