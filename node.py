from ast import literal_eval

class AST:
    def __init__(self, node_start, node_end, lineno=None):
        self.node_start = node_start
        self.node_end = node_end
        self.lineno = lineno

    def addChildren(self, *nodes):
      if nodes:
          for node in nodes:
              if node:
                  node.parent = self

class Block(AST):
    def __init__(self, stmts, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.stmts = stmts
        self._fields = ["stmts"]

class Assign(AST):
    def __init__(self, target, value, node_start, node_end):
        AST.__init__(self,node_start, node_end)
        self.target = target
        self.value = value
        self.addChildren(target)
        self.addChildren(value)
        self._fields = ["target", "value"]

class Name(AST):
    def __init__(self, name, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.id = name
        self._fields = ["id"]


class Num(AST):
    def __init__(self, n, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.n = literal_eval(n)
        self._fields = ["n"]

class Op(AST):
    def __init__(self, name, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.name = name
        self._fields = ["name"]

class BinOp(AST):
    def __init__(self, op, left, right, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.op = op
        self.right = right
        self.left = left
        self.addChildren(left, right)
        self._fields = ["op", "right", "left"]

class Str(AST):
    def __init__(self, s, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.s = s
        self._fields = ["s"]

class Module(AST):
    def __init__(self, name, body, docstring, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.name = name
        self.body = body
        self.docstring = docstring
        self.addChildren(name, body)

class Void(AST):
    def __init__(self, node_start, node_end):
        AST.__init__(self, node_start, node_end)

class For(AST):
    def __init__(self, target, iterator, body, orelse, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.target = target
        self.iterator = iterator
        self.body = body
        self.orelse = orelse
        self.addChildren(target, iterator, body, orelse)

class Call(AST):
    def __init__(self, func, args, keywords, kwargs, starargs, blockarg, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.func = func
        self.args = args
        self.keywords = keywords
        self.kwargs = kwargs
        self.starargs = starargs
        self.blockarg = blockarg
        self.addChildren(func, kwargs, starargs, blockarg)
        self.addChildren(args)
        self.addChildren(keywords)

class Return(AST):
    def __init__(self, value, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.value = value
        self.addChildren(value)

class Array(AST):
    def __init__(self, elts, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.elts = elts
        for e in elts:
            self.addChildren(e)

class If(AST):
    def __init__(self,test, body,orelse, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.test = test
        self.body = body
        self.orelse = orelse
        self.addChildren(test, body, orelse)

class Symbol(AST):
    def __init__(self, value, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.value = value

class Dict(AST):
    def __init__(self, entries, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.entries = entries
        for entry in entries:
            self.addChildren(entry)

class Assoc(AST):
    def __init__(self, key, value, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.key = key
        self.value = value
        self.addChildren(key, value)

class While(AST):
    def __init__(self, test, body, orelse, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.test = test
        self.body = body
        self.orelse = orelse
        self.addChildren(test, body, orelse)

class ClassDef(AST):
    def __init__(self, name, base, body, docstring, isStatic, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.name = name
        self.base = base
        self.body = body
        self.docstring = docstring
        self.isStatic = isStatic
        self.addChildren(name, base, body, docstring)

class FunctionDef(AST):
    def __init__(self, name, args, body, defaults, vararg, kwarg, afterRest, blockarg, docstring, node_start, node_end):
        AST.__init__(self, node_start, node_end)
        self.name = name
        self.args = args
        self.body = body
        self.defaults = defaults
        self.vararg = vararg
        self.kwarg = kwarg
        self.afterRest = afterRest
        self.blockarg = blockarg
        self.docstring = docstring
        self.addChildren(args)
        self.addChildren(defaults)
        self.addChildren(afterRest)
        self.addChildren(name, body, vararg, kwarg, blockarg)

class Attribute(AST):
    pass

class Import(AST):
    pass


class ImportFrom(AST):
    pass


class Expr(AST):
    pass
